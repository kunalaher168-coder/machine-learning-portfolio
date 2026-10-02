from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from synthetic_reporting import Observation, render_markdown, render_svg, summarize, synthetic_observations, write_report


class SyntheticReportingTests(unittest.TestCase):
    def test_summary_and_report(self) -> None:
        items = synthetic_observations()
        self.assertEqual(summarize(items), {"candidate": 2, "verified": 4, "needs review": 2})
        report = render_markdown(items)
        self.assertIn("invented", report)
        self.assertIn("Total observations: **8**", report)
        self.assertIn("| Verified | 4 | 50.0% |", report)

    def test_validation_and_svg_escaping(self) -> None:
        with self.assertRaises(ValueError):
            Observation("bad", 51.5, 0.5, "candidate")
        with self.assertRaises(ValueError):
            Observation("bad", float("nan"), 0.5, "candidate")
        with self.assertRaises(ValueError):
            summarize([Observation("same", 0, 0, "candidate"), Observation("same", 1, 1, "verified")])
        svg = render_svg([Observation("A<&", 0.5, 0.5, "candidate")])
        self.assertIn("A&lt;&amp;", svg)
        self.assertNotIn("A<&", svg)

    def test_written_artifacts_match_renderers(self) -> None:
        items = synthetic_observations()
        with tempfile.TemporaryDirectory() as directory:
            destination = Path(directory)
            write_report(destination, items)
            self.assertEqual((destination / "report.md").read_text(encoding="utf-8"), render_markdown(items))
            self.assertEqual((destination / "map.svg").read_text(encoding="utf-8"), render_svg(items))


if __name__ == "__main__":
    unittest.main()
