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
        errors, _ = validate(FIXTURE.replace("## 3. 🧭 自述 vs 外界叙事", "## 对照缺失"))
        self.assertIn("missing section: 3. 🧭 自述 vs 外界叙事", errors)

    def test_expansion_requires_reason(self) -> None:
        errors, _ = validate(FIXTURE.replace("实际窗口：2026-08-15 至 2026-11-13（90 天）", "实际窗口：2026-05-17 至 2026-11-13（180 天）"))
        self.assertIn("180-day window is mentioned without an expansion reason", errors)

    def test_user_material_needs_boundary(self) -> None:
        text = FIXTURE + "\n用户提供材料：项目介绍 PDF。"
        errors, _ = validate(text)
        self.assertIn("user-provided material is not separated from public verification", errors)

    def test_freshness_does_not_count_as_confidence(self) -> None:
        errors, _ = validate(FIXTURE.replace("可信度 `HIGH`", "可信度 `BREAKING`"))
        self.assertIn("missing confidence labels", errors)

    def test_evidence_expansion_with_reason_passes(self) -> None:
        text = FIXTURE.replace("实际窗口：2026-08-15 至 2026-11-13（90 天）", "实际窗口：2026-05-17 至 2026-11-13（180 天）｜扩展原因：初始窗口没有足够的直接证据")
        errors, _ = validate(text)
        self.assertEqual(errors, [])

    def test_user_material_with_boundary_passes(self) -> None:
        errors, _ = validate(FIXTURE + "\n用户提供材料：项目介绍 PDF。材料待核实：项目日期。")
        self.assertEqual(errors, [])


if __name__ == "__main__":
    unittest.main()
