# Classification with Group-Aware Evaluation

This work sample asks a practical evaluation question: how can a classifier be tuned without mixing related observations from the same site into training and test data? It uses an entirely generated binary classification problem so the split, preprocessing, tuning, and reporting steps can be reviewed in public.

## Data and task

`synthetic_pipeline.py` creates 432 observations across 36 fictional sites, with 12 records per site. Each record has four invented numeric features, a generated binary label, and a site ID. A small fraction of feature values is set to missing so imputation is part of the evaluation. No record or parameter is taken from a private dataset.

## Approach

| Step | Implementation | Reason |
| --- | --- | --- |
| Holdout | `GroupShuffleSplit` reserves 25% of sites for testing | Correlated records from one site do not cross the train/test boundary |
| Preprocessing | `SimpleImputer` sits inside a scikit-learn `Pipeline` | Each training fold learns its own median values |
| Selection | `GridSearchCV` uses three-fold `GroupKFold` and balanced accuracy | Model settings are chosen from training groups only |
| Model | A class-weighted random forest with a small, explicit parameter grid | The experiment is reproducible and inspectable |
| Evaluation | Balanced accuracy, precision, recall, F1, confusion matrix, and majority-class baseline | The report shows more than a single accuracy number |

The site holdout contains nine sites; the remaining 27 sites support training and cross-validation. The holdout is evaluated after selection. See [METHODS.md](METHODS.md) for the exact grid and limitations.

## Reproduce

The CI workflow uses Python 3.11:

```powershell
python -m pip install -r requirements.txt
python synthetic_pipeline.py
python -m unittest discover -s tests -v
```

The script prints a JSON report with the dataset marker, group counts, selected parameters, cross-validation score, holdout metrics, baseline score, and confusion matrix. The two tests check generated-data shape, group separation, and report consistency. [GitHub Actions](.github/workflows/tests.yml) runs them on pushes to this branch.

## What this demonstrates

The example makes the evaluation boundary explicit and keeps imputation inside cross-validation. It also compares the selected classifier with a simple baseline, rather than presenting an isolated model score.

## Scope

The labels are generated from the same synthetic features that the model sees. Scores therefore describe this invented exercise only. This branch does not contain real imagery, customer records, an original training dataset, or a deployed model, and it makes no claim about real-world performance. The [portfolio index](https://github.com/kunalaher168-coder/machine-learning-portfolio) links the other ML samples.
