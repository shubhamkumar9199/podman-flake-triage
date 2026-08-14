"""Stage 1 — discover workflow runs.

Lists runs of the blocking workflow (ci.yml) over a time window and upserts
them into SQLite. Two rules, both load-bearing:

1. NEVER filter with `?status=failure`. The runs API reports only the latest
   attempt's conclusion, so a run that failed and was re-run to green shows
   `success` and is absent from a failure listing — hiding exactly the flakes
   this tool exists to find. We list everything and diff attempts instead.

2. Drop `action_required` runs (fork PRs awaiting approval). They never ran
   tests; ~25% of raw run volume is this noise.

KNOWN LIMITATION: discovery filters on `created >= window`. A run that gets
re-run AFTER it ages out of the window is never re-listed, so its new attempt
(and any FAIL->PASS transition in it) is missed. In practice re-runs happen
within hours; use a window comfortably larger than realistic re-run latency.
A fix (poll runs individually by updated_at, cheap with ETag 304s) is planned
work, deliberately not prototype scope.
"""

from __future__ import annotations

import logging
from datetime import UTC, datetime, timedelta

from .config import Config
from .gh import GitHub

log = logging.getLogger(__name__)


def discover(cfg: Config, gh: GitHub, conn, days: int = 7) -> dict[str, int]:
    since = (datetime.now(UTC) - timedelta(days=days)).strftime("%Y-%m-%dT%H:%M:%SZ")
    path = f"/repos/{cfg.repo}/actions/workflows/{cfg.workflow}/runs"
    stats = {"seen": 0, "kept": 0, "skipped_event": 0, "skipped_conclusion": 0}

    for run in gh.paginate(path, {"created": f">={since}"}, item_key="workflow_runs"):
        stats["seen"] += 1
        if run["event"] not in cfg.events:
            stats["skipped_event"] += 1
            continue
        if run["conclusion"] in cfg.excluded_conclusions:
            stats["skipped_conclusion"] += 1
            continue
        conn.execute(
            """INSERT INTO runs(id, run_number, event, status, conclusion, run_attempt,
                                head_sha, head_branch, created_at, updated_at)
               VALUES(?,?,?,?,?,?,?,?,?,?)
               ON CONFLICT(id) DO UPDATE SET
                 status=excluded.status, conclusion=excluded.conclusion,
                 run_attempt=excluded.run_attempt, updated_at=excluded.updated_at,
                 -- a new attempt means the jobs snapshot is stale: resync
                 jobs_synced=CASE WHEN runs.run_attempt != excluded.run_attempt
                                  THEN 0 ELSE runs.jobs_synced END""",
            (
                run["id"],
                run["run_number"],
                run["event"],
                run["status"],
                run["conclusion"],
                run["run_attempt"],
                run["head_sha"],
                run["head_branch"],
                run["created_at"],
                run["updated_at"],
            ),
        )
        stats["kept"] += 1
    conn.commit()
    log.info("discover: %s", stats)
    return stats
