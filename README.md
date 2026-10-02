# ML classification - public work sample

This branch presents a small, runnable reconstruction of my structured-data classification work. All records, site IDs, labels, and feature values are generated in code. It contains no client dataset, private task brief, or model artifact.

The example separates whole sites into training and holdout sets, tunes a random forest with group-aware cross-validation, and reports holdout metrics alongside a majority-class baseline. Preprocessing is fitted inside the training pipeline.

## Run

```powershell
python -m pip install -r requirements.txt
python synthetic_pipeline.py
python -m unittest discover -s tests -v
```

The reported numbers measure performance only on invented data. They do not claim production accuracy or reproduce results from private work. See [METHODS.md](METHODS.md) for evaluation details.
