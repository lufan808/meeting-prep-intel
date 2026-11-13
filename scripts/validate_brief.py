#!/usr/bin/env python3
"""Validate the observable structure of a portable pre-meeting brief."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


REQUIRED_SECTIONS = (
    "1. 🌱 背景与关键转折",
    "2. 🔥 最近信号",
    "3. 🧭 自述 vs 外界叙事",
    "4. 🧠 工作方式与价值判断",
    "5. 🎯 会面准备",
    "6. 📊 可信度与搜索备注",
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
        if not re.search(rf"^## {re.escape(section)}\s*$", text, flags=re.MULTILINE):
            errors.append(f"missing section: {section}")

    if "Talking Points" not in text:
        errors.append("missing talking points")

    links = re.findall(r"\[[^\]]+\]\(https?://[^)]+\)", text)
    if not links:
        errors.append("no opened source link found")
    elif len(links) < 3:
        warnings.append("fewer than three source links; confirm that the evidence is sufficient")

    if not re.search(r"可信度\s*`?(?:HIGH|MEDIUM|LOW)\b", text):
        errors.append("missing confidence labels")

    if not re.search(r"时效\s*`?(?:BREAKING|RECENT|OLDER)\b", text):
        errors.append("missing freshness labels")

    if not re.search(r"^### \d{4}-\d{2}-\d{2} · ", text, flags=re.MULTILINE):
        warnings.append("no dated signal heading; explain thin evidence")

    for label in ("生成日期", "初始窗口", "实际窗口"):
        if label not in text:
            errors.append(f"missing window metadata: {label}")

    if "90" not in text and "90天" not in text:
        warnings.append("initial 90-day window is not visible")

    effective_window = re.search(r"实际窗口[^\n]*180\s*天", text)
    if effective_window:
        if not re.search(r"扩展原因\s*[:：]\s*\S+", text):
            errors.append("180-day window is mentioned without an expansion reason")

    if re.search(r"供应商|制作方|vendor|supplier", text, flags=re.IGNORECASE):
        if not re.search(r"身份|职位|项目参与|identity|title|participation", text, flags=re.IGNORECASE):
            warnings.append("supplier/vendor evidence needs an explicit identity or project-participation boundary")

    if re.search(r"用户提供材料\s*[:：]|附件\s*[:：]", text, flags=re.IGNORECASE):
        if not re.search(r"材料待核实\s*[:：]", text):
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
