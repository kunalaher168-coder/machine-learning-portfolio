"""Leakage-aware classifier evaluation on generated numeric observations."""

from __future__ import annotations

import json

import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.metrics import balanced_accuracy_score, confusion_matrix, f1_score, precision_score, recall_score
from sklearn.model_selection import GridSearchCV, GroupKFold, GroupShuffleSplit
from sklearn.pipeline import Pipeline


def make_synthetic_observations(seed: int = 17) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Return invented features, binary labels, and site groups.

    No observations or parameter values come from a private dataset.
    """
    rng = np.random.default_rng(seed)
    groups = np.repeat(np.arange(36), 12)
    count = len(groups)
    site_offset = rng.normal(0, 0.35, size=36)[groups]
    signal = rng.normal(size=count) + site_offset
    texture = rng.normal(size=count)
    shape = rng.normal(size=count)
    context = rng.normal(size=count) - site_offset / 2
    features = np.column_stack((signal, texture, shape, context))

    latent = 1.2 * signal - 0.8 * texture + 0.65 * shape + 0.3 * context
    latent += rng.normal(0, 0.75, size=count)
    labels = (latent > np.quantile(latent, 0.6)).astype(int)

    missing = rng.random(features.shape) < 0.04
    features[missing] = np.nan
    return features, labels, groups


def group_holdout(
    features: np.ndarray, labels: np.ndarray, groups: np.ndarray, seed: int = 17
) -> tuple[np.ndarray, np.ndarray]:
    """Keep every observation from a site wholly in train or test."""
    splitter = GroupShuffleSplit(n_splits=1, test_size=0.25, random_state=seed)
    train_index, test_index = next(splitter.split(features, labels, groups))
    if set(groups[train_index]) & set(groups[test_index]):
        raise AssertionError("site overlap across train and test")
    return train_index, test_index


def run_experiment(seed: int = 17) -> dict[str, object]:
    """Select settings on training groups and evaluate held-out groups once."""
    features, labels, groups = make_synthetic_observations(seed)
    train_index, test_index = group_holdout(features, labels, groups, seed)
    train_x, train_y, train_groups = features[train_index], labels[train_index], groups[train_index]
    test_x, test_y = features[test_index], labels[test_index]

    estimator = Pipeline(
        [
            ("impute", SimpleImputer(strategy="median")),
            ("model", RandomForestClassifier(class_weight="balanced", random_state=seed, n_jobs=1)),
        ]
    )
    search = GridSearchCV(
        estimator,
        {
            "model__n_estimators": [40, 80],
            "model__max_depth": [4, None],
            "model__min_samples_leaf": [2],
        },
        scoring="balanced_accuracy",
        cv=GroupKFold(n_splits=3),
        n_jobs=1,
    )
    search.fit(train_x, train_y, groups=train_groups)
    predicted = search.predict(test_x)

    majority = int(np.bincount(train_y, minlength=2).argmax())
    baseline = np.full(test_y.shape, majority, dtype=int)

    return {
        "dataset": "synthetic",
        "train_groups": int(len(np.unique(train_groups))),
        "test_groups": int(len(np.unique(groups[test_index]))),
        "shared_groups": int(len(set(train_groups) & set(groups[test_index]))),
        "best_parameters": search.best_params_,
        "cross_validation_balanced_accuracy": round(float(search.best_score_), 3),
        "test_balanced_accuracy": round(float(balanced_accuracy_score(test_y, predicted)), 3),
        "test_f1": round(float(f1_score(test_y, predicted, zero_division=0)), 3),
        "test_precision": round(float(precision_score(test_y, predicted, zero_division=0)), 3),
        "test_recall": round(float(recall_score(test_y, predicted, zero_division=0)), 3),
        "test_confusion_matrix": confusion_matrix(test_y, predicted, labels=[0, 1]).tolist(),
        "baseline_balanced_accuracy": round(float(balanced_accuracy_score(test_y, baseline)), 3),
    }


if __name__ == "__main__":
    print(json.dumps(run_experiment(), indent=2))
