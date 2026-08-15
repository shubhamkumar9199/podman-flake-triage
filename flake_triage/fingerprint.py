"""Stage 4 — failure fingerprinting and clustering.

Approach: Kubernetes test-infra triage-style normalization, with a key design
split learned from prototyping against real Podman logs:

    CLUSTER on a tight signature (one normalized error line),
    PAY the LLM only for a wide window of the cluster REPRESENTATIVE.

Window-size sensitivity measured on 58 real failures: a 3-5 line window keeps
~75% dedup; a 40-line window collapses to ~45%. Volatile tokens (PIDs,
container IDs, timestamps, ports) must be normalized or identical failures
fragment into phantom clusters.

Three failure modes this code explicitly guards against (all observed live):
1. lima teardown noise: hack/ci/ci.sh traps EXIT with `limactl delete`, so
   naive "lines before the error" extraction clusters on `Deleted "podman-ci"`.
2. unstripped ANSI codes splitting identical curl failures into two clusters.
3. bare PIDs (`... host agent process 2904`) fragmenting one flake into many
   — the upstream k8s regex set has no bare-PID rule; we add one.
"""

from __future__ import annotations

import logging
import re
from datetime import UTC, datetime

log = logging.getLogger(__name__)

ANSI_RE = re.compile(r"\x1b\[[0-9;]*[A-Za-z]|\x1b\][^\x07]*\x07")

# Harness/meta noise — never diagnostic, always near failures:
# - lima VM teardown (ci.sh traps EXIT with `limactl delete`)
# - the CI summary step's own traceback when a job died before producing logs
#   (github_log_summary.py on an unexpanded 'hack/ci/logs/*.html' glob)
# - GHA's positional "Process completed with exit code N" (1 per failing job,
#   ~150k lines deep; carries zero information about the failure)
NOISE_RE = re.compile(
    r"(limactl (delete|stop)|Deleted \"[\w-]+\"|Sending SIGKILL to hostagent|"
    r"\[hostagent\] .*(exiting|terminat)|"
    r"hack/ci/logs/\*\.html|github_log_summary|Traceback \(most recent call|"
    r"##\[error\]Process completed with exit code)",
    re.IGNORECASE,
)

# Cascade errors: once one of these fires, everything after it in the same job
# is fallout rather than an independent failure, so the cascade error IS the
# flake and the rest is noise.
#
# Ported from edsantiago/containertools (Apache-2.0), whose cirrus-flake-assign
# carried a --nuke flag: "delete all other flakes in the given task. Used for
# the unlinkat/EBUSY and unmount/EINVAL flakes, where everything else is hosed
# after that error." That was a human decision there; here it is automatic.
CASCADE_RE = re.compile(
    r"(unlinkat\b.*(EBUSY|device or resource busy|directory not empty)|"
    r"unmount\b.*(EINVAL|invalid argument))",
    re.IGNORECASE,
)

# Teardown failures are secondary: a test that already failed often fails to
# clean up after itself, which is expected and is not a separate flake.
# Also from edsantiago/containertools: "Do not count teardown_suite as a flake
# if there are other failures. That just means a failed test did not clean up
# after itself, which is expected."
TEARDOWN_FAIL_RE = re.compile(
    r"(teardown_suite|basic_teardown|`[a-z_]*teardown[a-z_]*'\s+failed)",
    re.IGNORECASE,
)

# error-line priority: the most diagnostically specific pattern wins.
# generic test-name lines (not ok / [FAILED]) rank BELOW concrete errors so
# the cluster key is the error, not the test that happened to hit it.
_PRIORITY: list[tuple[int, re.Pattern]] = [
    (100, re.compile(r"curl: \(\d+\)")),
    (95, re.compile(r"panic: ")),
    # \b so 'FileNotFoundError:' and friends do not match as 'Error:'
    (90, re.compile(r"\bError: \S")),
    (85, re.compile(r"`[^`]*' failed")),          # bats assert failure line
    (80, re.compile(r"Sending SIGKILL to the host agent process", re.IGNORECASE)),
    (75, re.compile(r"make: \*\*\*")),
    (70, re.compile(r"level=(error|fatal)")),
    (65, re.compile(r"##\[error\]Failed to run")),  # runner-provisioning failures
    (60, re.compile(r"\[(FAILED|TIMEDOUT|PANICKED)\]")),
    (50, re.compile(r"^not ok \d+")),
    (40, re.compile(r"FAIL!")),
]

_NORMALIZERS: list[tuple[re.Pattern, str]] = [
    # bats sequence numbers vary per run; the |NNN| file id is stable
    (re.compile(r"\bnot ok \d+ "), "not ok N "),
    (re.compile(r"\[\+\d+s\]"), ""),                                  # logformatter offsets
    (re.compile(r"\d{2}/\d{2}/\d{2,4}"), "DATE"),
    (re.compile(r"\d{4}-\d{2}-\d{2}"), "DATE"),
    (re.compile(r"\d{2}:\d{2}:\d{2}(\.\d+)?"), "TIME"),
    (re.compile(r"\b[0-9a-f]{12,64}\b"), "HEX"),                      # container/commit ids
    (re.compile(r"\b(process|pid)[ =]\d+", re.IGNORECASE), r"\1 PROC"),        # bare-PID rule (added)
    (re.compile(r"\bgoroutine \d+"), "goroutine N"),
    (re.compile(r"\.(go|bats|sh|py):\d+"), r".\1:N"),
    (re.compile(r"podman-e2e-\S+"), "podman-e2e-X"),                  # tmpdirs
    (re.compile(r"\b\d+(\.\d+)?(ms|s|m)\b"), "DUR"),
    (re.compile(r"localhost:\d+"), "localhost:PORT"),
    (re.compile(r"\b\d{4,}\b"), "NUM"),
    (re.compile(r"\s+"), " "),
]


def normalize(line: str) -> str:
    line = ANSI_RE.sub("", line)
    for pat, repl in _NORMALIZERS:
        line = pat.sub(repl, line)
    return line.strip()


_BATS_TEST_RE = re.compile(r"^not ok \d+")


def pick_key_line(summary: str) -> tuple[str, str, str | None] | None:
    """Return (key_line_original, context_window, qualifier) or None if no signal.

    qualifier disambiguates GENERIC key lines that would over-merge unrelated
    failures: bats helper asserts like `is "$output" ""' failed are identical
    across many tests, so the owning `not ok` line is attached; a bare ginkgo
    `[FAILED]` marker is qualified by the spec description that follows it.
    (Trade-off, documented: the same root cause manifesting in two different
    tests now forms two clusters — the classification tier can re-join those,
    a merge no clustering key can safely do on its own.)
    """
    lines = [ANSI_RE.sub("", ln) for ln in summary.splitlines()]

    # A cascade error outranks everything: whatever follows it in the same job
    # is fallout, so clustering on the fallout would split one root cause
    # across many keys.
    for i, line in enumerate(lines):
        if not NOISE_RE.search(line) and CASCADE_RE.search(line):
            window = "\n".join(lines[max(0, i - 2): i + 3])
            return line, window, None

    candidates: list[tuple[int, int]] = []  # (priority, index)
    for i, line in enumerate(lines):
        if NOISE_RE.search(line):
            continue
        for prio, pat in _PRIORITY:
            if pat.search(line):
                candidates.append((prio, i))
                break
    if not candidates:
        return None

    # Demote teardown failures: a test that already failed frequently fails to
    # clean up too, and that cleanup failure is not an independent flake. Only
    # keep one if nothing else failed in this job.
    non_teardown = [c for c in candidates if not TEARDOWN_FAIL_RE.search(lines[c[1]])]
    if non_teardown:
        candidates = non_teardown

    prio, i = max(candidates, key=lambda c: c[0])
    qualifier: str | None = None
    if prio == 85:  # generic bats assert — find the owning test upward
        for j in range(i - 1, max(-1, i - 40), -1):
            if _BATS_TEST_RE.match(lines[j]):
                qualifier = lines[j]
                break
    elif prio == 60 and "TIMEDOUT" not in lines[i]:
        # bare ginkgo [FAILED] marker — the spec description follows it
        for j in (i + 1, i + 2):
            if j < len(lines) and lines[j].strip():
                qualifier = lines[j].strip()
                break
    window = "\n".join(lines[max(0, i - 2): i + 3])   # tight 5-line window
    return lines[i], window, qualifier


SCHEMA = """
CREATE TABLE IF NOT EXISTS fingerprints (
    job_id      INTEGER PRIMARY KEY,
    cluster_key TEXT,      -- normalized single-line signature (NULL = no signal)
    key_line    TEXT,      -- the original evidence line, verbatim
    window      TEXT,      -- 5-line context around it
    computed_at TEXT
);
CREATE INDEX IF NOT EXISTS idx_fp_cluster ON fingerprints(cluster_key);
"""


def fingerprint(conn) -> dict[str, int]:
    conn.executescript(SCHEMA)
    rows = conn.execute(
        """SELECT e.job_id, e.summary FROM evidence e
           WHERE length(e.summary) > 0
             AND NOT EXISTS (SELECT 1 FROM fingerprints f WHERE f.job_id = e.job_id)"""
    ).fetchall()
    stats = {"jobs": 0, "signed": 0, "no_signal": 0}
    for row in rows:
        picked = pick_key_line(row["summary"])
        key_line, window, cluster_key = None, None, None
        if picked:
            key_line, window, qualifier = picked
            cluster_key = normalize(key_line)
            if qualifier:
                cluster_key = f"{normalize(qualifier)} | {cluster_key}"
            stats["signed"] += 1
        else:
            stats["no_signal"] += 1
        conn.execute(
            "INSERT OR REPLACE INTO fingerprints(job_id, cluster_key, key_line, window, computed_at)"
            " VALUES(?,?,?,?,?)",
            (row["job_id"], cluster_key, key_line, window,
             datetime.now(UTC).isoformat()),
        )
        stats["jobs"] += 1
    conn.commit()

    clusters = conn.execute(
        "SELECT COUNT(DISTINCT cluster_key) c FROM fingerprints WHERE cluster_key IS NOT NULL"
    ).fetchone()["c"]
    stats["clusters"] = clusters
    log.info("fingerprint: %s", stats)
    return stats
