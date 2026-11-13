#!/usr/bin/env python3
"""Validate the observable structure of a portable pre-meeting brief."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


REQUIRED_SECTIONS = (
    "背景与关键转折",
    "最近信号",
    "自述 vs 外界叙事",
    "工作方式与价值判断",
    "可直接使用的 Talking Points",
    "可信度与搜索备注",
)


def validate(text: str) -> tuple[list[str], list[str]]:
    """Return (errors, warnings) for a generated brief."""
    errors: list[str] = []
    warnings: list[str] = []

    if not text.strip():
        return ["brief is empty"], warnings

    if "身份卡" not in text:
        errors.append("missing identity card")

    for section in REQUIRED_SECTIONS:
        if section not in text:
            errors.append(f"missing section: {section}")

    links = re.findall(r"\[[^\]]+\]\(https?://[^)]+\)", text)
    if not links:
        errors.append("no opened source link found")
    elif len(links) < 3:
        warnings.append("fewer than three source links; confirm that the evidence is sufficient")

    if not re.search(r"\bHIGH\b|\bBREAKING\b|\bLOW\b", text):
        errors.append("missing confidence labels")

    if "90" not in text and "90天" not in text:
        warnings.append("initial 90-day window is not visible")

    if "180" in text or "180天" in text:
        if not re.search(r"扩展|原因|insufficient|不足", text, flags=re.IGNORECASE):
            errors.append("180-day window is mentioned without an expansion reason")

    if re.search(r"供应商|制作方|vendor|supplier", text, flags=re.IGNORECASE):
        if not re.search(r"身份|职位|项目参与|identity|title|participation", text, flags=re.IGNORECASE):
            warnings.append("supplier/vendor evidence needs an explicit identity or project-participation boundary")

    if re.search(r"用户提供|附件|user-provided|provided material", text, flags=re.IGNORECASE):
        if not re.search(r"待核实|独立|separate|verify|核验", text, flags=re.IGNORECASE):
            errors.append("user-provided material is not separated from public verification")

    return errors, warnings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("brief", type=Path, help="Markdown brief to validate")
    args = parser.parse_args(argv)

    try:
        text = args.brief.read_text(encoding="utf-8")
    except OSError as exc:
        print(f"ERROR: cannot read {args.brief}: {exc}")
        return 1

    errors, warnings = validate(text)
    for warning in warnings:
        print(f"WARN: {warning}")
    for error in errors:
        print(f"ERROR: {error}")

    if errors:
        print(f"FAILED: {len(errors)} error(s), {len(warnings)} warning(s)")
        return 1

    print(f"PASSED: {args.brief} ({len(warnings)} warning(s))")
    return 0


if __name__ == "__main__":
    sys.exit(main())
