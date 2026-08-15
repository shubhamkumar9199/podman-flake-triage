"""Stage 4b — merge near-duplicate clusters.

Exact-key clustering leaves obvious duplicates apart: two failures that differ
by one path component, one hostname, or a couple of words are the same problem
to a human and two problems to a string comparison. Every extra cluster is
another thing a maintainer reads and another model call paid for.

The approach is the one Kubernetes uses in test-infra/triage:

  1. cheap prefilter first. Represent each signature as counts of 4-grams
     hashed into a fixed number of buckets. The bucket-count difference,
     halved, is a lower bound on the real edit distance, so if that bound
     already exceeds the threshold the pair can be rejected without ever
     running the expensive comparison.
  2. exact edit distance only on survivors, bounded so it can give up early.
  3. threshold scaled to length: two signatures match if their edit distance
     is under 10% of their mean length. Short strings get no fuzz at all,
     because at that length a few characters is a real difference.

The merge is deliberately conservative. Over-merging is worse than
under-merging here: two distinct failures reported as one hides a bug, while
two clusters that should be one only costs a little duplicated reading.
"""

from __future__ import annotations

import logging
from collections import Counter

log = logging.getLogger(__name__)

NGRAM = 4
BUCKETS = 64
THRESHOLD_RATIO = 0.10
MIN_LEN = 24  # below this, only exact matches merge


def ngram_profile(s: str) -> Counter:
    """Counts of 4-grams hashed into a fixed number of buckets."""
    return Counter(hash(s[i:i + NGRAM]) % BUCKETS for i in range(max(0, len(s) - NGRAM + 1)))


def profile_lower_bound(a: Counter, b: Counter) -> float:
    """Lower bound on edit distance from bucketed n-gram counts.

    One character edit changes at most NGRAM n-grams, so the total count
    difference divided by NGRAM can never exceed the true distance.
    """
    keys = set(a) | set(b)
    return sum(abs(a.get(k, 0) - b.get(k, 0)) for k in keys) / NGRAM


def bounded_edit_distance(a: str, b: str, limit: int) -> int:
    """Levenshtein distance, giving up once it is known to reach `limit`.

    Returns `limit` if the true distance is >= limit, which is all the caller
    needs to reject the pair.
    """
    if a == b:
        return 0
    if abs(len(a) - len(b)) >= limit:
        return limit
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        best = cur[0]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
            best = min(best, cur[j])
        if best >= limit:
            return limit
        prev = cur
    return min(prev[-1], limit)


def should_merge(a: str, b: str) -> bool:
    """True if two signatures are near-duplicates of one another."""
    if a == b:
        return True
    if len(a) < MIN_LEN or len(b) < MIN_LEN:
        return False  # too short for fuzz to be safe
    limit = int((len(a) + len(b)) / 2.0 * THRESHOLD_RATIO)
    if limit <= 1:
        return False
    if profile_lower_bound(ngram_profile(a), ngram_profile(b)) >= limit:
        return False
    return bounded_edit_distance(a, b, limit) < limit


SCHEMA = """
ALTER TABLE fingerprints ADD COLUMN canonical_key TEXT;
"""


def _ensure_column(conn) -> None:
    cols = {r[1] for r in conn.execute("PRAGMA table_info(fingerprints)")}
    if "canonical_key" not in cols:
        conn.execute("ALTER TABLE fingerprints ADD COLUMN canonical_key TEXT")
        conn.commit()


def merge_clusters(conn) -> dict[str, int]:
    """Group near-duplicate cluster keys under one canonical key.

    The canonical key of a group is its most frequent member, so the name a
    maintainer sees is the wording that actually occurs most often.
    """
    _ensure_column(conn)
    rows = conn.execute(
        """SELECT cluster_key, COUNT(*) n FROM fingerprints
           WHERE cluster_key IS NOT NULL GROUP BY cluster_key ORDER BY n DESC, cluster_key"""
    ).fetchall()
    keys = [(r[0], r[1]) for r in rows]

    canonical: dict[str, str] = {}
    profiles: dict[str, Counter] = {}
    reps: list[str] = []  # canonical keys, most frequent first

    for key, _n in keys:
        profiles[key] = ngram_profile(key)
        hit = None
        for rep in reps:
            # cheap bound before the expensive comparison
            if len(key) < MIN_LEN or len(rep) < MIN_LEN:
                continue
            limit = int((len(key) + len(rep)) / 2.0 * THRESHOLD_RATIO)
            if limit <= 1:
                continue
            if profile_lower_bound(profiles[key], profiles[rep]) >= limit:
                continue
            if bounded_edit_distance(key, rep, limit) < limit:
                hit = rep
                break
        if hit is None:
            reps.append(key)
            canonical[key] = key
        else:
            canonical[key] = hit

    for key, canon in canonical.items():
        conn.execute(
            "UPDATE fingerprints SET canonical_key = ? WHERE cluster_key = ?", (canon, key)
        )
    conn.commit()

    merged = sum(1 for k, c in canonical.items() if k != c)
    stats = {"clusters_in": len(keys), "clusters_out": len(reps), "merged": merged}
    log.info("merge: %s", stats)
    return stats
