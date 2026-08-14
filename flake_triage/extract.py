"""Stage 3 — evidence extraction.

Two paths, because Podman's platforms are unevenly instrumented:

ARTIFACT PATH (lima matrix jobs: sys/int/bud/bindings/...):
  Each job uploads a `<key>.logs` artifact containing logformatter HTML.
  We pipe that HTML through podman's own `hack/ci/github_log_summary.py`
  (authored by the CI maintainer, merged 2026-08-07) rather than writing a
  parser: it reduces a 26 MB log to ~3 KB of exactly the failing blocks.

  TRAP: artifacts CANNOT be attributed to a run attempt via the API —
  `/attempts/{n}/artifacts` is 404, the artifact's workflow_run object has no
  run_attempt, and names collide across attempts (a re-run uploads a second
  artifact with the same name). Fetching the wrong one silently yields zero
  failure text (the green re-run's log). The only correct join is
  `artifact.created_at` within the failing attempt's job time window.

RAW-LOG PATH (windows/macos machine jobs):
  These jobs upload NO artifacts and run no logformatter (the invocation in
  win-lib.ps1 is still gated on $Env:CIRRUS_CI, which nothing sets since the
  Cirrus deletion), so we fall back to `/actions/jobs/{id}/logs` and plain
  ginkgo failure extraction. These are also the top flake sources.
"""

from __future__ import annotations

import logging
import re
import subprocess
import sys
import zipfile
from datetime import UTC, datetime, timedelta
from pathlib import Path

from .config import Config
from .gh import GitHub

log = logging.getLogger(__name__)

# Pin the extraction script to a specific upstream commit for reproducibility.
SUMMARY_SCRIPT_REF = "main"
SUMMARY_SCRIPT_PATH = "hack/ci/github_log_summary.py"


def _iso(ts: str) -> datetime:
    return datetime.fromisoformat(ts)  # py>=3.11 accepts the trailing 'Z'


def ensure_summary_script(cfg: Config, gh: GitHub) -> Path:
    """Vendor podman's own log-summary script (with provenance) into data/tools."""
    dest = cfg.data_dir / "tools" / "github_log_summary.py"
    if dest.exists():
        return dest
    dest.parent.mkdir(parents=True, exist_ok=True)
    url = (
        f"https://raw.githubusercontent.com/{cfg.repo}/{SUMMARY_SCRIPT_REF}/{SUMMARY_SCRIPT_PATH}"
    )
    gh.download(url, str(dest))
    provenance = dest.parent / "PROVENANCE.txt"
    provenance.write_text(
        f"github_log_summary.py fetched from {cfg.repo}@{SUMMARY_SCRIPT_REF}:{SUMMARY_SCRIPT_PATH}\n"
        "Author: Podman project (Paul Holzinger), Apache-2.0. Vendored unmodified.\n"
    )
    return dest


def match_artifact(job: dict, artifacts: list[dict], slack_minutes: int = 20) -> dict | None:
    """Attribute an artifact to a specific job attempt by created_at interval.

    The artifact is uploaded at the end of the job, so created_at must fall in
    [job.started_at, job.completed_at + slack]. Name must also correspond to
    the job's matrix identity (normalized token match, since the exact
    name-mangling of empty matrix fields is not worth hardcoding).
    """
    want = re.sub(r"[^a-z0-9]+", "-", job["job_key"].lower()).strip("-")
    start = _iso(job["started_at"])
    end = _iso(job["completed_at"]) + timedelta(minutes=slack_minutes)
    candidates = []
    for a in artifacts:
        if a.get("expired"):
            continue  # listing still returns expired artifacts; downloads 410
        name = re.sub(r"[^a-z0-9]+", "-", a["name"].lower().removesuffix(".logs")).strip("-")
        if name != want:
            continue
        created = _iso(a["created_at"])
        if start <= created <= end:
            candidates.append(a)
    # if several somehow match, take the earliest inside the window
    candidates.sort(key=lambda a: a["created_at"])
    return candidates[0] if candidates else None


def summarize_artifact(cfg: Config, gh: GitHub, artifact: dict, dest_dir: Path) -> str:
    """Download artifact zip, extract logformatter HTML, run podman's summary script."""
    dest_dir.mkdir(parents=True, exist_ok=True)
    zip_path = dest_dir / f"{artifact['id']}.zip"
    if not zip_path.exists():
        gh.download(artifact["archive_download_url"], str(zip_path))
    html_files = []
    try:
        with zipfile.ZipFile(zip_path) as zf:
            for info in zf.infolist():
                if info.filename.endswith(".html"):
                    out = dest_dir / Path(info.filename).name
                    out.write_bytes(zf.read(info))
                    html_files.append(out)
    except zipfile.BadZipFile:
        zip_path.unlink(missing_ok=True)  # don't trust it next run either
        raise
    if not html_files:
        return ""
    script = ensure_summary_script(cfg, gh)
    result = subprocess.run(
        [sys.executable, str(script), *[str(f) for f in html_files]],
        capture_output=True, text=True, timeout=120, check=False,  # rc inspected below
    )
    if result.returncode != 0:
        log.warning("summary script failed for artifact %s: %s",
                    artifact["id"], result.stderr[:500])
    return result.stdout


# Plain-text fallback for jobs without artifacts (windows/macos machine, and
# lima jobs that died before producing logformatter HTML).
#
# Two marker tiers: PRIMARY are actual failure blocks (ginkgo/bats verdicts,
# infra fetch failures, runner provisioning errors). Generic `Error:`/`panic:`
# are FALLBACK only — machine-test logs are full of *expected* Error: lines
# from negative-path tests, so leading with them extracts test noise.
_PRIMARY_MARKERS = re.compile(
    r"(\[FAILED\]|\[TIMEDOUT\]|\[PANICKED\]|FAIL!|^not ok |curl: \(\d+\)|"
    r"##\[error\]Failed to run)",
    re.MULTILINE,
)
_FALLBACK_MARKERS = re.compile(r"(\bError: |panic:)", re.MULTILINE)
# The CI summary step's own traceback (job died before logs existed) — never signal.
_LOG_NOISE = re.compile(r"(hack/ci/logs/\*\.html|github_log_summary)")
_TS_PREFIX = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d+Z ?", re.MULTILINE)


def summarize_raw_log(text: str, context: int = 15, max_blocks: int = 12) -> str:
    """Extract failure-adjacent blocks from a raw job log (GHA timestamp-prefixed)."""
    text = _TS_PREFIX.sub("", text)
    lines = text.splitlines()
    keep: set[int] = set()
    for markers in (_PRIMARY_MARKERS, _FALLBACK_MARKERS):
        blocks = 0
        for i, line in enumerate(lines):
            if markers.search(line) and not _LOG_NOISE.search(line):
                keep.update(range(max(0, i - 2), min(len(lines), i + context)))
                blocks += 1
                if blocks >= max_blocks:
                    break
        if keep:
            break  # primary tier found real failure blocks; skip the fallback
    if not keep:
        return ""
    out, prev = [], None
    for i in sorted(keep):
        if prev is not None and i != prev + 1:
            out.append("...")
        out.append(lines[i])
        prev = i
    return "\n".join(out)


def extract(cfg: Config, gh: GitHub, conn, limit: int | None = None) -> dict[str, int]:
    """Extract evidence for failing jobs that have a confirmed FAIL->PASS transition,
    plus failing jobs in failed runs (for clustering breadth)."""
    rows = conn.execute(
        """SELECT j.id, j.run_id, j.job_key, j.name, j.started_at, j.completed_at
           FROM jobs j
           WHERE j.conclusion='failure'
             AND j.started_at IS NOT NULL AND j.completed_at IS NOT NULL
             AND NOT EXISTS (SELECT 1 FROM evidence e WHERE e.job_id = j.id)
           ORDER BY (SELECT 1 FROM transitions t WHERE t.fail_job_id = j.id) DESC NULLS LAST,
                    j.started_at DESC"""
        + (f" LIMIT {int(limit)}" if limit else "")
    ).fetchall()

    stats = {"jobs": 0, "artifact": 0, "raw_log": 0, "none": 0}
    artifacts_by_run: dict[int, list[dict]] = {}

    for row in rows:
        job = dict(row)
        run_id = job["run_id"]
        if run_id not in artifacts_by_run:
            artifacts_by_run[run_id] = list(
                gh.paginate(f"/repos/{cfg.repo}/actions/runs/{run_id}/artifacts",
                            item_key="artifacts")
            )
        art = match_artifact(job, artifacts_by_run[run_id])
        source, art_id, summary = "none", None, ""
        if art is not None:
            # protected: an expired/corrupt/timeout artifact must not kill the
            # stage, and an EMPTY artifact summary (job died before writing
            # logformatter HTML) must fall through to the raw log below.
            art_id = art["id"]
            try:
                text = summarize_artifact(cfg, gh, art, cfg.artifacts_dir / str(run_id))
                if text.strip():
                    source, summary = "artifact", text
            except Exception as e:
                log.warning("artifact path failed for job %s (artifact %s): %s"
                            " — falling back to raw log", job["id"], art_id, e)
        if not summary.strip():
            # raw-log path: no artifact (machine jobs), artifact empty, or
            # artifact fetch failed
            try:
                log_dest = cfg.artifacts_dir / str(run_id) / f"job-{job['id']}.log"
                log_dest.parent.mkdir(parents=True, exist_ok=True)
                if not log_dest.exists():
                    gh.download(
                        f"https://api.github.com/repos/{cfg.repo}/actions/jobs/{job['id']}/logs",
                        str(log_dest),
                    )
                text = summarize_raw_log(log_dest.read_text(errors="replace"))
                if text.strip():
                    source, summary = "raw_log", text
            except Exception as e:  # log gone (expired) or fetch failure
                log.warning("raw log fetch failed for job %s: %s", job["id"], e)
        stats[source] += 1
        conn.execute(
            """INSERT OR REPLACE INTO evidence
               (job_id, run_id, job_key, source, artifact_id, raw_bytes, summary, extracted_at)
               VALUES(?,?,?,?,?,?,?,?)""",
            (job["id"], run_id, job["job_key"], source, art_id,
             len(summary), summary, datetime.now(UTC).isoformat()),
        )
        conn.commit()
        stats["jobs"] += 1
        if stats["jobs"] % 10 == 0:
            log.info("extract: %d jobs processed...", stats["jobs"])

    log.info("extract: %s", stats)
    return stats
