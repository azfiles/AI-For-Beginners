#!/usr/bin/env python3
"""Fail when the repository's Site/runtime declarations drift from real files."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from website.prepare_lite import SPECS  # noqa: E402


def require_file(relative: str) -> None:
    path = ROOT / relative
    if not path.is_file():
        raise SystemExit(f"missing required file: {relative}")


def main() -> None:
    required = [
        "README.md",
        "CONTRIBUTING.md",
        "NOTEBOOK_STATUS.zh-CN.md",
        "docs/ARCHITECTURE.zh-CN.md",
        "docs/GITHUB_ACTIONS.zh-CN.md",
        "site/RUNNING.zh-CN.md",
        "site/VALIDATION.zh-CN.md",
        "runtime/README.zh-CN.md",
        "website/build.py",
        "website/learning.css",
        "website/learning.js",
        "website/notebook-status.json",
        "website/validation-status.json",
    ]
    for relative in required:
        require_file(relative)

    browser = set(SPECS)
    if len(browser) != 7:
        raise SystemExit(f"expected 7 browser notebooks, found {len(browser)}")
    for relative in sorted(browser):
        require_file(relative)

    status = json.loads((ROOT / "website/notebook-status.json").read_text())
    blocked = set(status.get("blocked", {}))
    short_verified = set(status.get("short_verified", {}))
    overlap = blocked & short_verified
    if overlap:
        raise SystemExit("blocked and short_verified overlap: " + ", ".join(sorted(overlap)))

    for relative in sorted(blocked | short_verified):
        require_file(relative)

    if not status.get("browser_run"):
        raise SystemExit("website/notebook-status.json has no browser_run")
    if not status.get("short_training_run"):
        raise SystemExit("website/notebook-status.json has no short_training_run")
    if not status.get("full_audit", {}).get("run"):
        raise SystemExit("website/notebook-status.json has no full_audit run")

    print(
        "repository contract OK: "
        f"{len(browser)} browser, {len(short_verified)} short-verified, "
        f"{len(blocked)} resource-gated notebooks"
    )


if __name__ == "__main__":
    main()
