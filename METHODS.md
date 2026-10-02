# Classification Evaluation Notes

## Dataset construction

The generator creates 36 fictional site IDs and 12 rows per site. Four numeric features are formed from random components, with a site-specific offset introducing within-site dependence. Binary labels are calculated from those features plus random noise, using the 60th percentile of a synthetic latent score as the threshold. Roughly 4% of feature entries are then replaced with missing values. This construction is meant to exercise an evaluation pipeline; it is not a simulation calibrated to a real site or sensor.

## Split and model selection

1. `GroupShuffleSplit(test_size=0.25, random_state=17)` separates whole sites into 27 training and nine holdout sites.
2. A pipeline fits median imputation and a class-weighted `RandomForestClassifier`.
3. `GridSearchCV` uses three-fold `GroupKFold` on training sites only, with balanced accuracy as the selection metric.
4. The grid tests 40 or 80 trees, maximum depth 4 or unlimited, and minimum leaf size 2. These are demonstration settings, not an optimized search for a real dataset.
5. The selected pipeline predicts the untouched holdout sites once. The report checks that the train and holdout site sets have no overlap.

Because imputation is inside the pipeline, each cross-validation fold estimates medians from its own training portion. The holdout observations are not used to select hyperparameters.

## Report interpretation

The JSON output includes balanced accuracy, precision, recall, F1, and a two-class confusion matrix for the holdout. A constant majority-class prediction, determined from training labels, provides a simple baseline. Cross-validation balanced accuracy is shown separately from holdout balanced accuracy so the two are not confused.

## Limits and next checks

This is one generated dataset and one fixed site split. It does not test geographic or temporal shift, label uncertainty, sampling bias, calibration, or stability across independent real datasets. A real study would require documented label definitions, a justified split by site and time, error analysis by data slice, and repeated evaluation under an agreed protocol. No operational accuracy can be inferred from this example.
