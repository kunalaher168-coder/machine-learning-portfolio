from __future__ import annotations

import sys
import unittest
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from synthetic_pipeline import group_holdout, make_synthetic_observations, run_experiment


class SyntheticPipelineTests(unittest.TestCase):
    def test_generated_data_and_group_boundary(self) -> None:
        features, labels, groups = make_synthetic_observations()
        self.assertEqual(features.shape, (432, 4))
        self.assertEqual(set(np.unique(labels)), {0, 1})
        self.assertTrue(np.isnan(features).any())
        train, test = group_holdout(features, labels, groups)
        self.assertEqual(len(train) + len(test), len(labels))
        self.assertFalse(set(groups[train]) & set(groups[test]))

    def test_holdout_report_is_explicitly_synthetic(self) -> None:
        report = run_experiment()
        self.assertEqual(report["dataset"], "synthetic")
        self.assertEqual(report["shared_groups"], 0)
        self.assertEqual(report["train_groups"] + report["test_groups"], 36)
        self.assertEqual(sum(map(sum, report["test_confusion_matrix"])), report["test_groups"] * 12)
        for name in ["cross_validation_balanced_accuracy", "test_balanced_accuracy", "test_f1", "test_precision", "test_recall", "baseline_balanced_accuracy"]:
            self.assertGreaterEqual(report[name], 0)
            self.assertLessEqual(report[name], 1)


if __name__ == "__main__":
    unittest.main()
