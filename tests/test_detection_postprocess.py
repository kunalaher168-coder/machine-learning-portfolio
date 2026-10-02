from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from detection_postprocess import Detection, intersection_over_union, suppress_overlaps


class DetectionPostprocessTests(unittest.TestCase):
    def test_overlap_geometry(self) -> None:
        a = Detection((0, 0, 2, 2), 0.9, 1)
        b = Detection((1, 1, 3, 3), 0.8, 1)
        c = Detection((3, 3, 4, 4), 0.7, 1)
        self.assertAlmostEqual(intersection_over_union(a, b), 1 / 7)
        self.assertEqual(intersection_over_union(a, a), 1)
        self.assertEqual(intersection_over_union(a, c), 0)

    def test_class_aware_suppression_and_tie_order(self) -> None:
        strong = Detection((0, 0, 2, 2), 0.9, 1)
        duplicate = Detection((0.1, 0.1, 2.1, 2.1), 0.8, 1)
        other_class = Detection((0, 0, 2, 2), 0.7, 2)
        distant = Detection((5, 5, 6, 6), 0.7, 1)
        self.assertEqual(suppress_overlaps([strong, duplicate, other_class, distant]), [strong, other_class, distant])

    def test_invalid_inputs(self) -> None:
        with self.assertRaises(ValueError):
            Detection((1, 0, 1, 2), 0.8, 1)
        with self.assertRaises(ValueError):
            Detection((0, 0, 1, 1), 1.2, 1)
        with self.assertRaises(ValueError):
            suppress_overlaps([], -0.1)

    def test_equal_score_keeps_first_same_class_box(self) -> None:
        first = Detection((0, 0, 2, 2), 0.8, 1)
        second = Detection((0.1, 0.1, 2.1, 2.1), 0.8, 1)
        self.assertEqual(suppress_overlaps([first, second]), [first])


if __name__ == "__main__":
    unittest.main()
