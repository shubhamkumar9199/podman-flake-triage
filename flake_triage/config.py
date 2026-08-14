"""Configuration. Env-overridable, validated at load, no hidden defaults in code paths."""

from __future__ import annotations

import os
import subprocess
from dataclasses import dataclass, field
from pathlib import Path


def _default_token() -> str:
    """GITHUB_TOKEN env var, falling back to the gh CLI's stored token."""
    tok = os.environ.get("GITHUB_TOKEN", "").strip()
    if tok:
        return tok
    try:
        out = subprocess.run(
            ["gh", "auth", "token"], capture_output=True, text=True, timeout=10, check=True
        )
        return out.stdout.strip()
    except (OSError, subprocess.SubprocessError):
        return ""


@dataclass(frozen=True)
class Config:
    repo: str = os.environ.get("FT_REPO", "podman-container-tools/podman")
    workflow: str = os.environ.get("FT_WORKFLOW", "ci.yml")
    data_dir: Path = field(
        default_factory=lambda: Path(os.environ.get("FT_DATA_DIR", "data")).resolve()
    )
    token: str = field(default_factory=_default_token)
    # Merge-gate aggregation job: always red when anything is red, zero diagnostic
    # signal (failed 47/47 in sampled failed runs). ci.yml comments "do not change it".
    excluded_jobs: tuple[str, ...] = ("Total Success",)
    # Fork-PR runs awaiting approval never ran tests at all (~25% of runs sampled).
    excluded_conclusions: tuple[str, ...] = ("action_required",)
    events: tuple[str, ...] = ("push", "pull_request")

    @property
    def db_path(self) -> Path:
        return self.data_dir / "flake.db"

    @property
    def artifacts_dir(self) -> Path:
        return self.data_dir / "artifacts"

    def validate(self) -> None:
        if not self.token:
            raise SystemExit(
                "No GitHub token: set GITHUB_TOKEN or authenticate the gh CLI (gh auth login)."
            )
        if "/" not in self.repo:
            raise SystemExit(f"FT_REPO must be owner/name, got {self.repo!r}")
        self.data_dir.mkdir(parents=True, exist_ok=True)


def load() -> Config:
    cfg = Config()
    cfg.validate()
    return cfg
