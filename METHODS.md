# Evaluation notes

- Generated observations are grouped by fictional site. A site appears wholly in either training or holdout data.
- Three-fold `GroupKFold` tuning uses training groups only.
- Median imputation is part of the scikit-learn pipeline and is fitted within each training fold.
- The held-out groups are evaluated once after model selection.
- Balanced accuracy, precision, recall, F1, and a confusion matrix are shown with a majority-class baseline.

For real work, I would also check label quality, class balance, time separation, sampling bias, and errors by data slice. No real-world validity follows from this synthetic example.
