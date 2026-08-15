"""Stage 5 — two-tier classification of failure clusters.

TIER 1 (regex, deterministic, free): the recurring infrastructure signatures.
Measured on real Podman logs, the top 4 signatures alone covered 78% of
failures — none of them needs (or should get) an LLM opinion.

TIER 2 (LLM, per NEW cluster representative only): everything the regex tier
does not recognize. The model sees one wide context window per cluster, must
quote a verbatim evidence line (validated), and UNKNOWN is an acceptable
verdict. Analyses are stored with model + prompt version for reproducibility.
"""

from __future__ import annotations

import logging
import re
from datetime import UTC, datetime

from . import llm

log = logging.getLogger(__name__)

# (pattern, category, note) — first match wins; patterns run on the ORIGINAL
# key line, not the normalized one, so they can be written precisely.
REGEX_RULES: list[tuple[re.Pattern, str, str]] = [
    (re.compile(r"curl: \(22\).*(503|error: 5\d\d)"), "NETWORK_INFRA",
     "external URL fetch returned a 5xx"),
    (re.compile(r"curl: \(56\)"), "NETWORK_INFRA",
     "connection died mid-transfer"),
    (re.compile(r"curl: \(\d+\)"), "NETWORK_INFRA",
     "curl failure fetching an external resource"),
    (re.compile(r"Sending SIGKILL to the host agent process", re.IGNORECASE), "VM_INFRA",
     "lima hostagent had to be SIGKILLed"),
    (re.compile(r"make: \*\*\*.*tests-included"), "HARNESS",
     "test-inclusion harness gate failed"),
    (re.compile(r"make: \*\*\*"), "HARNESS",
     "make target failed"),
    (re.compile(r"Suite Timeout Elapsed|\[TIMEDOUT\]"), "TEST_TIMEOUT",
     "suite deadline expired; the named spec is whichever was in flight, not the culprit"),
    (re.compile(r"Address already in use"), "PARALLEL_INTERFERENCE",
     "port collision under parallel execution"),
    (re.compile(r"unable to obtain cgroup stats.*no such device"), "PRODUCT_RACE",
     "cgroup removed between existence check and read (stats ENODEV race)"),
    (re.compile(r"No space left on device"), "RUNNER_INFRA",
     "runner disk exhaustion"),
    (re.compile(r"##\[error\]Failed to run:.*(HTTP response: 5\d\d|socket hang up)"),
     "RUNNER_INFRA", "runner provisioning/communication failure"),
]

SCHEMA = """
CREATE TABLE IF NOT EXISTS analyses (
    cluster_key    TEXT PRIMARY KEY,
    tier           TEXT NOT NULL,     -- 'regex' | 'llm'
    category       TEXT NOT NULL,
    confidence     REAL NOT NULL,
    evidence_line  TEXT,
    rationale      TEXT,
    model          TEXT,
    prompt_version TEXT,
    rejected_note  TEXT,              -- set when an LLM answer failed validation
    created_at     TEXT
);
"""


def _clusters(conn) -> list[dict]:
    """Distinct clusters with member count and a representative (longest summary
    = richest context for the LLM payload)."""
    return [
        dict(r)
        for r in conn.execute(
            """SELECT COALESCE(f.canonical_key, f.cluster_key) AS cluster_key,
                      COUNT(*) AS members,
                      (SELECT f2.key_line FROM fingerprints f2
                        WHERE COALESCE(f2.canonical_key,f2.cluster_key) = COALESCE(f.canonical_key,f.cluster_key) LIMIT 1) AS key_line,
                      (SELECT e.summary FROM fingerprints f3
                         JOIN evidence e ON e.job_id = f3.job_id
                        WHERE COALESCE(f3.canonical_key,f3.cluster_key) = COALESCE(f.canonical_key,f.cluster_key)
                        ORDER BY length(e.summary) DESC LIMIT 1) AS rep_summary,
                      (SELECT e.job_key FROM fingerprints f4
                         JOIN evidence e ON e.job_id = f4.job_id
                        WHERE COALESCE(f4.canonical_key,f4.cluster_key) = COALESCE(f.canonical_key,f.cluster_key) LIMIT 1) AS job_key
               FROM fingerprints f
               WHERE f.cluster_key IS NOT NULL
               GROUP BY COALESCE(f.canonical_key, f.cluster_key)"""
        )
    ]


def classify(conn, provider_name: str | None = None,
             max_llm_calls: int = 40, max_payload_chars: int = 16000) -> dict[str, int]:
    conn.executescript(SCHEMA)
    provider = llm.get_provider(provider_name) if provider_name else None
    stats = {"clusters": 0, "regex": 0, "llm": 0, "llm_rejected": 0, "skipped_no_llm": 0}
    llm_attempts = 0  # counts every API call made, including errored ones —
    #                   the cost cap must bound spend, not successes

    for cluster in _clusters(conn):
        key = cluster["cluster_key"]
        if conn.execute("SELECT 1 FROM analyses WHERE cluster_key=?", (key,)).fetchone():
            continue  # already analyzed; fingerprints are stable so reuse is safe
        stats["clusters"] += 1

        # ---- tier 1: regex on the original key line
        matched = False
        for pat, category, note in REGEX_RULES:
            if pat.search(cluster["key_line"]):
                conn.execute(
                    """INSERT INTO analyses(cluster_key, tier, category, confidence,
                         evidence_line, rationale, created_at)
                       VALUES(?,?,?,?,?,?,?)""",
                    (key, "regex", category, 1.0, cluster["key_line"], note,
                     datetime.now(UTC).isoformat()),
                )
                stats["regex"] += 1
                matched = True
                break
        if matched:
            continue

        # ---- tier 2: LLM on the cluster representative
        if provider is None or llm_attempts >= max_llm_calls:
            stats["skipped_no_llm"] += 1
            continue
        window = (cluster["rep_summary"] or "")[:max_payload_chars]
        payload = llm.wrap_payload(cluster["job_key"] or "?", window)
        llm_attempts += 1
        try:
            raw = provider.complete(llm.SYSTEM_PROMPT, payload)
        except Exception as e:
            log.warning("LLM call failed for cluster %.60s...: %s", key, e)
            continue
        # validate against the RAW window, never the wrapped payload — the
        # header/delimiters we add must not be quotable as "evidence"
        analysis, reason = llm.validate(raw, window)
        if analysis is None and llm_attempts < max_llm_calls:
            # one repair attempt, then reject
            llm_attempts += 1
            try:
                raw = provider.complete(
                    llm.SYSTEM_PROMPT,
                    payload + f"\n\nYour previous answer was invalid ({reason}). "
                              "Answer again following the rules exactly.",
                )
                analysis, reason = llm.validate(raw, window)
            except Exception as e:
                log.warning("LLM repair call failed: %s", e)
        if analysis is None:
            conn.execute(
                """INSERT INTO analyses(cluster_key, tier, category, confidence,
                     evidence_line, rationale, model, prompt_version, rejected_note, created_at)
                   VALUES(?,?,?,?,?,?,?,?,?,?)""",
                (key, "llm", "UNKNOWN", 0.0, None, None, provider.name,
                 llm.PROMPT_VERSION, reason, datetime.now(UTC).isoformat()),
            )
            stats["llm_rejected"] += 1
        else:
            conn.execute(
                """INSERT INTO analyses(cluster_key, tier, category, confidence,
                     evidence_line, rationale, model, prompt_version, created_at)
                   VALUES(?,?,?,?,?,?,?,?,?)""",
                (key, "llm", analysis["category"], analysis["confidence"],
                 analysis["evidence_line"], analysis["rationale"], provider.name,
                 llm.PROMPT_VERSION, datetime.now(UTC).isoformat()),
            )
            stats["llm"] += 1
        conn.commit()

    conn.commit()
    log.info("classify: %s", stats)
    return stats
