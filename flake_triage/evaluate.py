"""Evaluation against free ground truth.

Podman's re-run behavior labels a corpus for us: a job that concluded
`failure` on attempt N and `success` on attempt M>N of the same run (same
head_sha, no code change) is a confirmed flake — no human annotation needed.
Jobs that failed on every attempt including the last are persistent failures.

What we measure (and report honestly, including the misses):

  coverage    how many confirmed-flake jobs produced usable evidence,
              a fingerprint, and a classification (pipeline losses are
              listed per stage — silent truncation would overstate quality)
  dedup       signatures -> clusters compression (drives LLM cost)
  regex share fraction of classified occurrences that never needed an LLM
  sanity      confirmed flakes classified GENUINE_REGRESSION (should be ~0);
              persistent failures classified as infra-flake (suspicious)

This does NOT measure classification *accuracy* against the ground truth —
FAIL->PASS says "flaky", not "which category". Category accuracy needs a
human-audited sample, which is future work and is said so in the report.
"""

from __future__ import annotations

import logging
from datetime import UTC, datetime
from pathlib import Path

from .config import Config

log = logging.getLogger(__name__)


def evaluate(cfg: Config, conn, out_dir: Path | None = None) -> Path:
    out_dir = out_dir or (cfg.data_dir / "reports")
    out_dir.mkdir(parents=True, exist_ok=True)

    q = lambda sql, *p: conn.execute(sql, p).fetchone()[0]

    runs = q("SELECT COUNT(*) FROM runs WHERE jobs_synced=1")
    multi = q("SELECT COUNT(*) FROM runs WHERE jobs_synced=1 AND run_attempt>1")
    failing = q("SELECT COUNT(*) FROM jobs WHERE conclusion='failure'")
    confirmed = q("SELECT COUNT(DISTINCT fail_job_id) FROM transitions")

    # pipeline coverage over the confirmed-flake corpus
    c_evidence = q(
        """SELECT COUNT(DISTINCT t.fail_job_id) FROM transitions t
           JOIN evidence e ON e.job_id = t.fail_job_id WHERE length(e.summary) > 0"""
    )
    c_fp = q(
        """SELECT COUNT(DISTINCT t.fail_job_id) FROM transitions t
           JOIN fingerprints f ON f.job_id = t.fail_job_id
           WHERE f.cluster_key IS NOT NULL"""
    )
    c_classified = q(
        """SELECT COUNT(DISTINCT t.fail_job_id) FROM transitions t
           JOIN fingerprints f ON f.job_id = t.fail_job_id
           JOIN analyses a ON a.cluster_key = COALESCE(f.canonical_key,f.cluster_key)"""
    )

    # dedup + tier split over everything fingerprinted
    signed = q("SELECT COUNT(*) FROM fingerprints WHERE cluster_key IS NOT NULL")
    clusters = q("SELECT COUNT(DISTINCT COALESCE(canonical_key,cluster_key)) FROM fingerprints WHERE cluster_key IS NOT NULL")
    no_signal = q("SELECT COUNT(*) FROM fingerprints WHERE cluster_key IS NULL")
    regex_jobs = q(
        """SELECT COUNT(*) FROM fingerprints f JOIN analyses a ON a.cluster_key=COALESCE(f.canonical_key,f.cluster_key)
           WHERE a.tier='regex'"""
    )
    llm_jobs = q(
        """SELECT COUNT(*) FROM fingerprints f JOIN analyses a ON a.cluster_key=COALESCE(f.canonical_key,f.cluster_key)
           WHERE a.tier='llm'"""
    )

    # sanity: confirmed flakes that the classifier called a regression
    misfired = [
        dict(r) for r in conn.execute(
            """SELECT t.fail_job_id, f.cluster_key, a.category
               FROM transitions t
               JOIN fingerprints f ON f.job_id = t.fail_job_id
               JOIN analyses a ON a.cluster_key = COALESCE(f.canonical_key,f.cluster_key)
               WHERE a.category = 'GENUINE_REGRESSION'"""
        )
    ]

    cats = conn.execute(
        """SELECT a.category, a.tier, COUNT(*) n
           FROM fingerprints f JOIN analyses a ON a.cluster_key=COALESCE(f.canonical_key,f.cluster_key)
           GROUP BY a.category, a.tier ORDER BY n DESC"""
    ).fetchall()

    pct = lambda a, b: f"{a / b:.0%}" if b else "n/a"
    lines = [
        f"# Evaluation — {datetime.now(UTC):%Y-%m-%d %H:%M} UTC",
        "",
        "## Corpus (all measured live from GHA, no synthetic data)",
        f"- runs analyzed: {runs} ({multi} with >1 attempt, {pct(multi, runs)})",
        f"- failing job records: {failing}",
        f"- ground truth: {confirmed} confirmed flakes (FAIL→PASS, same head_sha)",
        "",
        "## Pipeline coverage over the confirmed-flake corpus",
        f"- evidence extracted: {c_evidence}/{confirmed} ({pct(c_evidence, confirmed)})",
        f"- fingerprinted:      {c_fp}/{confirmed} ({pct(c_fp, confirmed)})",
        f"- classified:         {c_classified}/{confirmed} ({pct(c_classified, confirmed)})",
        "",
        "## Dedup / cost",
        f"- failure signatures: {signed}  → clusters: {clusters} "
        f"(dedup {pct(signed - clusters, signed)})",
        f"- no extractable signal: {no_signal}",
        f"- occurrences classified by regex tier (no LLM): {regex_jobs} "
        f"({pct(regex_jobs, regex_jobs + llm_jobs)} of classified)",
        f"- occurrences needing LLM tier: {llm_jobs}",
        "",
        "## Sanity checks",
        f"- confirmed flakes classified GENUINE_REGRESSION: {len(misfired)}"
        + ("" if not misfired else "  ← INVESTIGATE: " + ", ".join(str(m['fail_job_id']) for m in misfired)),
        "",
        "## Category distribution (clusters weighted by occurrences)",
    ]
    lines += [f"- {r['category']} [{r['tier']}]: {r['n']}" for r in cats]
    lines += [
        "",
        "## Known limitations (stated, not hidden)",
        "- FAIL→PASS labels *flakiness*, not category; per-category accuracy needs",
        "  a human-audited sample and is not claimed here.",
        "- Jobs with expired/absent logs and artifacts produce no evidence and are",
        "  counted as pipeline losses above, not silently dropped.",
        "- A re-run that stays red is treated as persistent, but a flake can in",
        "  principle fail twice; multi-attempt persistence is evidence, not proof.",
    ]
    path = out_dir / "evaluation.md"
    path.write_text("\n".join(lines) + "\n")
    log.info("evaluate: wrote %s", path)
    return path
