"""SQLite persistence. One file, WAL mode, idempotent upserts everywhere.

Deliberately not Postgres: the whole corpus for months of Podman CI fits in a
few hundred MB, a single writer suffices, and a mentee-maintainable tool must
run with zero infrastructure. (Ed Santiago's 4.1 GB private SQLite DB worked
for years; its problem was bus factor, not the engine.)
"""

from __future__ import annotations

import sqlite3
from pathlib import Path

SCHEMA = """
CREATE TABLE IF NOT EXISTS runs (
    id            INTEGER PRIMARY KEY,
    run_number    INTEGER,
    event         TEXT,
    status        TEXT,
    conclusion    TEXT,
    run_attempt   INTEGER,        -- latest attempt number seen
    head_sha      TEXT,
    head_branch   TEXT,
    created_at    TEXT,
    updated_at    TEXT,
    jobs_synced   INTEGER NOT NULL DEFAULT 0
);

-- One row per (job id); job ids are unique per attempt, so a re-run job
-- appears as a new row with the same job_key and a higher run_attempt.
CREATE TABLE IF NOT EXISTS jobs (
    id            INTEGER PRIMARY KEY,
    run_id        INTEGER NOT NULL REFERENCES runs(id),
    run_attempt   INTEGER NOT NULL,
    name          TEXT NOT NULL,
    job_key       TEXT NOT NULL,   -- name with ' / lima' suffix stripped
    status        TEXT,
    conclusion    TEXT,
    started_at    TEXT,
    completed_at  TEXT
);
CREATE INDEX IF NOT EXISTS idx_jobs_run ON jobs(run_id, job_key, run_attempt);
CREATE INDEX IF NOT EXISTS idx_jobs_key ON jobs(job_key, conclusion);

-- Confirmed flakes: same run (same head_sha), job failed on one attempt and
-- succeeded on a later one. This is the ground-truth corpus.
CREATE TABLE IF NOT EXISTS transitions (
    run_id        INTEGER NOT NULL,
    job_key       TEXT NOT NULL,
    head_sha      TEXT,
    fail_attempt  INTEGER NOT NULL,
    pass_attempt  INTEGER NOT NULL,
    fail_job_id   INTEGER NOT NULL,  -- job row holding the failing log
    PRIMARY KEY (run_id, job_key, fail_attempt)
);

-- Extracted failure evidence for a failing job (small text, from the
-- artifact HTML piped through podman's own hack/ci/github_log_summary.py,
-- or a raw-log fallback for jobs with no artifacts: windows/macos machine).
CREATE TABLE IF NOT EXISTS evidence (
    job_id       INTEGER PRIMARY KEY,   -- the failing job
    run_id       INTEGER NOT NULL,
    job_key      TEXT,
    source       TEXT NOT NULL,          -- 'artifact' | 'raw_log' | 'none'
    artifact_id  INTEGER,
    raw_bytes    INTEGER,
    summary      TEXT,                   -- extracted failure text
    extracted_at TEXT
);

-- HTTP conditional-request cache: a 304 costs almost nothing against the
-- 5000/hr budget, so polling the same windows repeatedly is cheap.
CREATE TABLE IF NOT EXISTS http_cache (
    url        TEXT PRIMARY KEY,
    etag       TEXT,
    body       BLOB,
    fetched_at TEXT
);
"""


def connect(path: Path) -> sqlite3.Connection:
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA busy_timeout=30000")  # sync + extract may run concurrently
    conn.execute("PRAGMA foreign_keys=ON")
    conn.executescript(SCHEMA)
    return conn
