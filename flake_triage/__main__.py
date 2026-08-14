"""CLI: flake-triage <command>

    sync     discover runs + diff attempts (stages 1-2)
    stats    print measured flake numbers from the local DB
"""

from __future__ import annotations

import argparse
import logging
import sys

from . import config, db
from .attempts import sync_jobs
from .classify import classify
from .discover import discover
from .evaluate import evaluate
from .extract import extract
from .fingerprint import fingerprint
from .gh import GitHub
from .report import report


def cmd_sync(args) -> None:
    cfg = config.load()
    conn = db.connect(cfg.db_path)
    gh = GitHub(cfg.token, conn)
    d = discover(cfg, gh, conn, days=args.days)
    print(f"discover: kept {d['kept']}/{d['seen']} runs "
          f"(dropped {d['skipped_conclusion']} action_required, {d['skipped_event']} other-event)")
    a = sync_jobs(cfg, gh, conn, limit=args.limit)
    print(f"attempts: synced {a['runs']} runs, {a['jobs']} job records, "
          f"{a['transitions']} FAIL->PASS transitions, {a['persistent']} persistent failures")


def cmd_extract(args) -> None:
    cfg = config.load()
    conn = db.connect(cfg.db_path)
    gh = GitHub(cfg.token, conn)
    if args.retry_empty:
        n = conn.execute("DELETE FROM evidence WHERE length(summary) = 0").rowcount
        conn.commit()
        print(f"retry-empty: cleared {n} empty evidence rows for re-extraction")
    e = extract(cfg, gh, conn, limit=args.limit)
    print(f"extract: {e['jobs']} failing jobs -> {e['artifact']} via artifact, "
          f"{e['raw_log']} via raw log, {e['none']} with no extractable text")


def cmd_fingerprint(args) -> None:
    cfg = config.load()
    conn = db.connect(cfg.db_path)
    if args.rebuild:
        n = conn.execute("DELETE FROM fingerprints").rowcount
        conn.commit()
        print(f"rebuild: cleared {n} fingerprints (normalization/key rules changed)")
    f = fingerprint(conn)
    signed = f["signed"]
    print(f"fingerprint: {f['jobs']} evidence records -> {signed} signatures "
          f"in {f['clusters']} clusters"
          + (f" ({1 - f['clusters'] / signed:.0%} dedup)" if signed else "")
          + f", {f['no_signal']} with no extractable signal")


def cmd_classify(args) -> None:
    cfg = config.load()
    conn = db.connect(cfg.db_path)
    if args.rebuild:
        n = conn.execute("DELETE FROM analyses").rowcount
        conn.commit()
        print(f"rebuild: cleared {n} analyses (rules/prompt changed)")
    c = classify(conn, provider_name=args.llm, max_llm_calls=args.max_llm_calls)
    print(f"classify: {c['clusters']} new clusters -> {c['regex']} regex-tier, "
          f"{c['llm']} llm-tier, {c['llm_rejected']} llm answers rejected, "
          f"{c['skipped_no_llm']} awaiting llm")


def cmd_report(args) -> None:
    cfg = config.load()
    conn = db.connect(cfg.db_path)
    paths = report(cfg, conn)
    print(f"wrote {paths['digest']}")
    print(f"wrote {paths['known_flakes']}")


def cmd_evaluate(args) -> None:
    cfg = config.load()
    conn = db.connect(cfg.db_path)
    path = evaluate(cfg, conn)
    print(f"wrote {path}")
    print(path.read_text())


def cmd_stats(args) -> None:
    cfg = config.load()
    conn = db.connect(cfg.db_path)

    total = conn.execute("SELECT COUNT(*) c FROM runs WHERE jobs_synced=1").fetchone()["c"]
    multi = conn.execute(
        "SELECT COUNT(*) c FROM runs WHERE jobs_synced=1 AND run_attempt > 1"
    ).fetchone()["c"]
    trans = conn.execute("SELECT COUNT(*) c FROM transitions").fetchone()["c"]
    print(f"runs synced:            {total}")
    if total:
        print(f"runs with >1 attempt:   {multi} ({multi / total:.1%})")
    print(f"FAIL->PASS transitions: {trans}  (confirmed flakes, same head_sha)")

    print("\ntop flaking jobs (by confirmed transitions):")
    for r in conn.execute(
        "SELECT job_key, COUNT(*) n FROM transitions GROUP BY job_key ORDER BY n DESC LIMIT 15"
    ):
        print(f"  {r['n']:>3}  {r['job_key']}")

    print("\nattempt distribution:")
    for r in conn.execute(
        "SELECT run_attempt, COUNT(*) n FROM runs WHERE jobs_synced=1 "
        "GROUP BY run_attempt ORDER BY run_attempt"
    ):
        print(f"  attempt {r['run_attempt']}: {r['n']} runs")


def main() -> None:
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s"
    )
    p = argparse.ArgumentParser(prog="flake-triage")
    sub = p.add_subparsers(dest="cmd", required=True)

    ps = sub.add_parser("sync", help="discover runs and diff attempts (stages 1-2)")
    ps.add_argument("--days", type=int, default=7, help="lookback window (default 7)")
    ps.add_argument("--limit", type=int, default=None, help="max runs to job-sync this call")
    ps.set_defaults(fn=cmd_sync)

    pe = sub.add_parser("extract", help="extract failure evidence (stage 3)")
    pe.add_argument("--limit", type=int, default=None, help="max failing jobs to process")
    pe.add_argument("--retry-empty", action="store_true",
                    help="re-extract jobs whose previous extraction yielded no text")
    pe.set_defaults(fn=cmd_extract)

    pf = sub.add_parser("fingerprint", help="cluster failure evidence (stage 4)")
    pf.add_argument("--rebuild", action="store_true",
                    help="recompute all fingerprints (after normalization-rule changes)")
    pf.set_defaults(fn=cmd_fingerprint)

    pc = sub.add_parser("classify", help="classify clusters: regex tier + optional LLM (stage 5)")
    pc.add_argument("--llm", choices=["anthropic", "ollama", "openai"], default=None,
                    help="LLM provider for unmatched clusters (default: regex tier only)")
    pc.add_argument("--max-llm-calls", type=int, default=40)
    pc.add_argument("--rebuild", action="store_true",
                    help="reclassify all clusters (after rule/prompt changes)")
    pc.set_defaults(fn=cmd_classify)

    pr = sub.add_parser("report", help="write digest.md + known-flakes.yaml (stage 6)")
    pr.set_defaults(fn=cmd_report)

    pv = sub.add_parser("evaluate", help="measure pipeline against FAIL->PASS ground truth")
    pv.set_defaults(fn=cmd_evaluate)

    pt = sub.add_parser("stats", help="print measured flake numbers")
    pt.set_defaults(fn=cmd_stats)

    args = p.parse_args()
    args.fn(args)


if __name__ == "__main__":
    sys.exit(main())
