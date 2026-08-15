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
                      COUNT(DISTINCT r.head_branch) n_branches,
                      MAX(r.head_branch) any_branch
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

    # Metadata gate no log-text classifier can provide: a cluster confined to a
    # single non-main branch with zero FAIL->PASS confirmations is almost
    # certainly that PR breaking things, not a flake. (Observed live: the
    # top signature in a 10-day window was one PR failing the same test 37x
    # across 13 matrix jobs.) These are annotated in the digest and excluded
    # from the known-flakes catalog regardless of their text classification.
    for c in clusters:
        c["pr_concentrated"] = (
            c["confirmed"] == 0
            and c["n_branches"] == 1
            and c["any_branch"] not in ("main",)
            and not c["any_branch"].startswith("v")  # release branches
        )

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
        if c["pr_concentrated"]:
            confirmed += (f" · ⚠ confined to branch `{c['any_branch']}`, never re-run to"
                          " green — likely that PR's regression, not a flake")
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
        if c["pr_concentrated"]:
            continue  # single-PR breakage is not a known flake, whatever the text says
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
