"""podman-flake-triage: evidence-first flake detection for Podman's GitHub Actions CI.

Pipeline (each stage is a CLI subcommand, all state in local SQLite + files):

    discover -> attempts -> extract -> fingerprint -> classify -> report

Design constraints this tool is built around (see docs/design-notes.md):
- Flakes are only visible at the GHA *run-attempt* layer: Podman sets
  GINKGO_FLAKE_ATTEMPTS=0, so a flake is "a red job a human re-ran".
- `?status=failure` on the runs API reports only the latest attempt's
  conclusion, so re-run-to-green flakes are invisible to failure polling.
  This tool never uses it.
- FAIL->PASS transitions at the same head_sha are free, human-label-free
  ground truth for evaluation.
"""

__version__ = "0.1.0"
