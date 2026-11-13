#!/usr/bin/env python3
"""Golden tests for the public brief validator."""

from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from validate_brief import validate  # noqa: E402


FIXTURE = (ROOT / "tests" / "fixtures" / "golden-brief.md").read_text(encoding="utf-8")


class ValidateBriefTests(unittest.TestCase):
    def test_golden_brief_passes(self) -> None:
        errors, warnings = validate(FIXTURE)
        self.assertEqual(errors, [])
        self.assertLessEqual(len(warnings), 1)

    def test_missing_section_fails(self) -> None:
        errors, _ = validate(FIXTURE.replace("## 🧭 自述 vs 外界叙事", "## 对照缺失"))
        self.assertIn("missing section: 自述 vs 外界叙事", errors)

    def test_expansion_requires_reason(self) -> None:
        errors, _ = validate(FIXTURE.replace("最近 90 天", "最近 180 天").replace("没有必要扩展到 180 天；90 天内已有足够的直接证据。", ""))
        self.assertIn("180-day window is mentioned without an expansion reason", errors)

    def test_user_material_needs_boundary(self) -> None:
        text = FIXTURE.replace("待核实", "待处理") + "\n用户提供材料：项目介绍 PDF。"
        errors, _ = validate(text)
        self.assertIn("user-provided material is not separated from public verification", errors)


if __name__ == "__main__":
    unittest.main()
