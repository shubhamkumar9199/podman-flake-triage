"""Stage 6 — reporting.

Two outputs, both files (this tool never posts to GitHub on its own — filing
issues/comments stays a human decision, which is also what the maintainers'
LLM policy and triage culture require):

1. digest.md   — a weekly markdown digest a maintainer can actually read:
                 measured volumes, confirmed FAIL->PASS flakes, clusters with
                 category + verbatim evidence line + run links.
2. known-flakes.yaml — a draft catalog in the shape proposed in podman issue
                 #28870 (flake detection for the /retrigger command), so the
                 output plugs into the integration point the maintainers
                 already designed.
"""

from __future__ import annotations

import logging
from datetime import UTC, datetime
from pathlib import Path

from .config import Config

log = logging.getLogger(__name__)


def _yaml_quote(s: str) -> str:
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'


def cluster_gates(confirmed: int, branches: str | None) -> dict:
    """Decide what the re-run record and branch spread say about a cluster.

    Kept separate from report() so the rules can be tested without a database,
    because getting them wrong puts a hard breakage into a catalogue that other
    automation trusts.
    """
    seen = {b for b in (branches or "").split(",") if b}
    unconfirmed = confirmed == 0
    return {
        "unconfirmed": unconfirmed,
        "branch_concentrated": unconfirmed and "main" not in seen,
        "branches_seen": sorted(seen),
        # a catalogue entry claims "retrying this is worthwhile", which is only
        # true of something that has actually been seen to pass on a retry
        "catalogue_eligible": not unconfirmed,
    }


def report(cfg: Config, conn, out_dir: Path | None = None) -> dict[str, Path]:
    out_dir = out_dir or (cfg.data_dir / "reports")
    out_dir.mkdir(parents=True, exist_ok=True)
    now = datetime.now(UTC)

    total = conn.execute("SELECT COUNT(*) c FROM runs WHERE jobs_synced=1").fetchone()["c"]
    multi = conn.execute(
        "SELECT COUNT(*) c FROM runs WHERE jobs_synced=1 AND run_attempt>1").fetchone()["c"]
    trans = conn.execute("SELECT COUNT(*) c FROM transitions").fetchone()["c"]
    window = conn.execute(
        "SELECT MIN(created_at) lo, MAX(created_at) hi FROM runs WHERE jobs_synced=1"
    ).fetchone()

    clusters = [
        dict(r)
        for r in conn.execute(
            """SELECT COALESCE(f.canonical_key, f.cluster_key) AS cluster_key, COUNT(*) members,
                      MIN(r.created_at) first_seen, MAX(r.created_at) last_seen,
                      a.category, a.confidence, a.tier, a.evidence_line, a.rationale,
                      GROUP_CONCAT(DISTINCT e.job_key) job_keys,
                      GROUP_CONCAT(DISTINCT f.job_id) job_ids,
                      -- confirmed = at least one member job is a FAIL->PASS transition
                      SUM(EXISTS(SELECT 1 FROM transitions t
                                 WHERE t.fail_job_id = f.job_id)) confirmed,
                      GROUP_CONCAT(DISTINCT r.head_branch) branches
               FROM fingerprints f
               JOIN evidence e ON e.job_id = f.job_id
               JOIN jobs j ON j.id = f.job_id
               JOIN runs r ON r.id = j.run_id
               LEFT JOIN analyses a ON a.cluster_key = COALESCE(f.canonical_key, f.cluster_key)
               WHERE f.cluster_key IS NOT NULL
               GROUP BY COALESCE(f.canonical_key, f.cluster_key)
               ORDER BY members DESC"""
        )
    ]

    # Two metadata gates that no amount of reading the log text can replace.
    #
    # 1. UNCONFIRMED. A cluster that has never once passed on a re-run has no
    #    evidence of being flaky at all, whatever its error message looks like.
    #    Something consistently broken produces the same text as something
    #    intermittent. This is the gate that matters for the catalogue: an
    #    entry consumed by a /retrigger command (podman#28870) tells the system
    #    "retrying this is worthwhile", and for a hard breakage that is false.
    #
    #    Found by a maintainer's chat message rather than by testing. A seccomp
    #    profile failure appeared 8 times on `machine linux amd64` across three
    #    release branches from 11 Aug, never once green on a re-run. The lead
    #    maintainer diagnosed it by hand on 14 Aug: "the linux machine failure
    #    is not a flake ... a new test failure due underlying changes on the
    #    runner itself". The tool had the evidence and still listed it as a
    #    known flake, because the old gate demanded a single branch and this
    #    spanned three.
    #
    # 2. BRANCH-CONCENTRATED. Never seen on main, and unconfirmed, means the
    #    branch is the common factor rather than the infrastructure. Observed
    #    live: one PR failed the same test 37 times across 13 matrix jobs.
    for c in clusters:
        c.update(cluster_gates(c["confirmed"], c["branches"]))

    # ---------- digest.md ----------
    lines = [
        f"# Podman CI flake digest — {now:%Y-%m-%d}",
        "",
        f"Window: {window['lo']} → {window['hi']} · workflow `{cfg.workflow}` · repo `{cfg.repo}`",
        "",
        "## Volume",
        "",
        f"- runs analyzed (completed, non-`action_required`): **{total}**",
        f"- runs needing >1 attempt: **{multi}** ({multi / total:.0%})" if total else "",
        f"- confirmed flakes (job FAIL→PASS at identical commit): **{trans}**",
        "",
        "> Detection is attempt-diff based (`/jobs?filter=all`). A `?status=failure`",
        "> listing cannot see re-run-to-green runs at all, and a green re-run alone is",
        "> treated as *observation*, not proof — classification comes from log evidence.",
        "",
        "## Failure clusters",
        "",
    ]
    for c in clusters:
        cat = c["category"] or "UNCLASSIFIED"
        conf = f" ({c['confidence']:.2f}, {c['tier']})" if c["category"] else ""
        confirmed = f" · {c['confirmed']} re-run-confirmed" if c["confirmed"] else ""
        if c["branch_concentrated"]:
            confirmed += (f" · ⚠ never seen on main and never re-run to green"
                          f" (branches: {', '.join(c['branches_seen'])}) — the branch"
                          " looks like the common factor, not the infrastructure")
        elif c["unconfirmed"]:
            confirmed += (" · ⚠ never once passed on a re-run, so there is no evidence"
                          " it is intermittent rather than simply broken")
        lines += [
            f"### {cat}{conf} — {c['members']} occurrence(s){confirmed}",
            "",
            f"- signature: `{c['cluster_key']}`",
            f"- evidence: `{(c['evidence_line'] or '').strip()}`" if c["evidence_line"] else "",
            f"- note: {c['rationale']}" if c["rationale"] else "",
            f"- jobs: {c['job_keys']}",
            f"- seen: {c['first_seen'][:10]} → {c['last_seen'][:10]}",
            "",
        ]
    top = conn.execute(
        "SELECT job_key, COUNT(*) n FROM transitions GROUP BY job_key ORDER BY n DESC LIMIT 10"
    ).fetchall()
    if top:
        lines += ["## Top re-run-confirmed flaky jobs", ""]
        lines += [f"- {r['n']}× `{r['job_key']}`" for r in top]
        lines.append("")
    digest_path = out_dir / "digest.md"
    digest_path.write_text("\n".join(filter(None, lines)) + "\n")

    # ---------- known-flakes.yaml (shape from podman issue #28870) ----------
    ylines = [
        "# Draft known-flakes catalog — generated by podman-flake-triage",
        "# Shape follows the proposal in podman issue #28870 (flake detection for",
        "# the /retrigger command). Entries are cluster signatures with evidence.",
        f"# Generated: {now:%Y-%m-%dT%H:%M:%SZ}  Window: {window['lo']} .. {window['hi']}",
        "flakes:",
    ]
    for c in clusters:
        if not c["category"] or c["category"] in ("GENUINE_REGRESSION", "UNKNOWN"):
            continue  # a known-flakes catalog must not contain regressions or guesses
        if not c["catalogue_eligible"]:
            continue  # never observed to pass on a re-run, so not a known flake
        ylines += [
            f"  - signature: {_yaml_quote(c['cluster_key'])}",
            f"    category: {c['category']}",
            f"    confidence: {c['confidence']:.2f}",
            f"    classified_by: {c['tier']}",
            f"    occurrences: {c['members']}",
            f"    rerun_confirmed: {c['confirmed']}",
            f"    first_seen: {c['first_seen'][:10]}",
            f"    last_seen: {c['last_seen'][:10]}",
            f"    jobs: [{', '.join(_yaml_quote(k) for k in (c['job_keys'] or '').split(','))}]",
        ]
    yaml_path = out_dir / "known-flakes.yaml"
    yaml_path.write_text("\n".join(ylines) + "\n")

    log.info("report: wrote %s and %s", digest_path, yaml_path)
    return {"digest": digest_path, "known_flakes": yaml_path}
