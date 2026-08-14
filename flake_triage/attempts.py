"""Stage 2 — per-attempt job diffing. This is the flake-detection primitive.

    GET /repos/{repo}/actions/runs/{id}/jobs?filter=all

returns every job across ALL run attempts, each tagged with `run_attempt`.
All attempts of a run share the same head_sha, so a job that concluded
`failure` on attempt N and `success` on attempt M>N is a same-commit,
different-outcome event: a confirmed flake, labeled for free.

Podman has no automatic retries (GINKGO_FLAKE_ATTEMPTS=0), so this attempt
layer is the ONLY place flakes are observable — rerun-based detectors from
the literature (DeFlaker, FindIt, Meta PFS) do not transfer.

Notes:
- Later attempts may contain only the re-run jobs (re-run failed only), so a
  job absent from attempt N+1 keeps its attempt-N conclusion.
- `Total Success` is the merge-gate aggregation job — always red when anything
  is red, zero diagnostic signal. Excluded.
- Job names from the reusable lima workflow carry a ' / lima' suffix; strip it
  so the 4-tuple (test, mode, priv, distro) is the stable key.
"""

from __future__ import annotations

import logging
from collections import defaultdict

from .config import Config
from .gh import GitHub

log = logging.getLogger(__name__)


def job_key(name: str) -> str:
    """Normalize a job name to its stable matrix identity."""
    return name.removesuffix(" / lima").strip()


def diff_attempts(occurrences: list[dict]) -> tuple[list[tuple[int, int, int]], int]:
    """Diff one job identity's conclusions across run attempts.

    occurrences: dicts with at least run_attempt, conclusion, id.
    Returns (transitions, persistent) where transitions is a list of
    (fail_attempt, pass_attempt, fail_job_id) — a FAIL->PASS at the same
    commit, i.e. a confirmed flake — and persistent counts failures that were
    re-run and failed again. A failure on the final attempt is neither: it was
    simply never re-run (or the re-run hasn't happened yet).

    A job absent from a later attempt keeps its earlier conclusion (re-run
    failed-jobs-only reruns just the red ones).
    """
    occurrences = sorted(occurrences, key=lambda j: j["run_attempt"])
    last_attempt = max((j["run_attempt"] for j in occurrences), default=0)
    transitions: list[tuple[int, int, int]] = []
    persistent = 0
    for fj in occurrences:
        if fj["conclusion"] != "failure":
            continue
        later_pass = [
            j for j in occurrences
            if j["run_attempt"] > fj["run_attempt"] and j["conclusion"] == "success"
        ]
        if later_pass:
            transitions.append((fj["run_attempt"], later_pass[0]["run_attempt"], fj["id"]))
        elif fj["run_attempt"] < last_attempt:
            persistent += 1
    return transitions, persistent


def sync_jobs(cfg: Config, gh: GitHub, conn, limit: int | None = None) -> dict[str, int]:
    """Fetch all-attempt job lists for completed runs not yet synced."""
    rows = conn.execute(
        "SELECT id, head_sha FROM runs WHERE status='completed' AND jobs_synced=0 "
        "ORDER BY created_at DESC" + (f" LIMIT {int(limit)}" if limit else "")
    ).fetchall()
    stats = {"runs": 0, "jobs": 0, "transitions": 0, "persistent": 0}

    for row in rows:
        run_id, head_sha = row["id"], row["head_sha"]
        jobs = list(
            gh.paginate(f"/repos/{cfg.repo}/actions/runs/{run_id}/jobs", {"filter": "all"},
                        item_key="jobs")
        )
        by_key: dict[str, list] = defaultdict(list)
        for j in jobs:
            key = job_key(j["name"])
            if key in cfg.excluded_jobs:
                continue
            conn.execute(
                """INSERT INTO jobs(id, run_id, run_attempt, name, job_key, status,
                                    conclusion, started_at, completed_at)
                   VALUES(?,?,?,?,?,?,?,?,?)
                   ON CONFLICT(id) DO UPDATE SET status=excluded.status,
                     conclusion=excluded.conclusion, completed_at=excluded.completed_at""",
                (
                    j["id"], run_id, j["run_attempt"], j["name"], key,
                    j["status"], j["conclusion"], j["started_at"], j["completed_at"],
                ),
            )
            by_key[key].append(j)
            stats["jobs"] += 1

        # diff conclusions across attempts per job identity
        for key, occurrences in by_key.items():
            transitions, persistent = diff_attempts(occurrences)
            for fail_attempt, pass_attempt, fail_job_id in transitions:
                conn.execute(
                    """INSERT OR IGNORE INTO transitions
                       (run_id, job_key, head_sha, fail_attempt, pass_attempt, fail_job_id)
                       VALUES(?,?,?,?,?,?)""",
                    (run_id, key, head_sha, fail_attempt, pass_attempt, fail_job_id),
                )
                stats["transitions"] += 1
            stats["persistent"] += persistent

        conn.execute("UPDATE runs SET jobs_synced=1 WHERE id=?", (run_id,))
        conn.commit()
        stats["runs"] += 1
        if stats["runs"] % 25 == 0:
            log.info("attempts: %d runs synced...", stats["runs"])

    log.info("attempts: %s", stats)
    return stats
