# Machine Learning Portfolio

Three runnable Python work samples covering structured classification, object detection post-processing, and observation reporting. Each topic has its own branch and README. The examples were rebuilt for public review with invented data, so a reviewer can inspect the code and run the tests without access to private material.

## Projects

| Project | What to inspect | Engineering decisions | Verification |
| --- | --- | --- | --- |
| [Classification](https://github.com/kunalaher168-coder/machine-learning-portfolio/tree/ml-classification) | [Pipeline](https://github.com/kunalaher168-coder/machine-learning-portfolio/blob/ml-classification/synthetic_pipeline.py) and [methods](https://github.com/kunalaher168-coder/machine-learning-portfolio/blob/ml-classification/METHODS.md) | Separate fictional sites across train and holdout sets; fit imputation inside cross-validation; compare the selected model with a majority-class baseline | Two automated tests check group separation and the report |
| [Object detection](https://github.com/kunalaher168-coder/machine-learning-portfolio/tree/object-detection) | [Post-processing module](https://github.com/kunalaher168-coder/machine-learning-portfolio/blob/object-detection/detection_postprocess.py) | Validate candidate boxes; compute intersection over union; suppress overlaps within each class with deterministic score ordering | Four automated tests cover geometry, suppression, stable ordering, and invalid input |
| [Geospatial reporting](https://github.com/kunalaher168-coder/machine-learning-portfolio/tree/geospatial-reporting) | [Reporting script](https://github.com/kunalaher168-coder/machine-learning-portfolio/blob/geospatial-reporting/synthetic_reporting.py), [sample map](https://github.com/kunalaher168-coder/machine-learning-portfolio/blob/geospatial-reporting/sample_output/map.svg), and [sample report](https://github.com/kunalaher168-coder/machine-learning-portfolio/blob/geospatial-reporting/sample_output/report.md) | Validate invented observations; aggregate category counts; produce reproducible SVG and Markdown outputs | Three automated tests check totals, escaping, validation, and generated files |

## Review path

1. Open a project branch above and read its README for the question, method, output, and limits.
2. Inspect the linked module and tests. The examples are small enough to run locally.
3. Use the branch's run commands to reproduce the result. GitHub Actions also runs the tests on each branch.

The default branch is an index. Project code stays on the named branches so each work sample can be reviewed on its own.

## What the work demonstrates

- An evaluation structure that keeps related observations together during splitting and tuning.
- Careful implementation of detection geometry and class-aware filtering.
- Transformation of structured observations into a readable report and a schematic visual.
- Input checks, deterministic examples, and automated tests around the public code.

## Evidence and limits

Every record, label, site ID, bounding box, and coordinate in these branches is invented. The map uses unit-square positions, not real geography. No client data, private instructions, original notebook, imagery, trained weights, or source archive is included. The repository shows technical approach and code quality; it does not establish measured accuracy on real data, production deployment, or a client's endorsement.

For code review and test-design work, see the separate [Code QA portfolio](https://github.com/kunalaher168-coder/code-qa-portfolio). For algorithms, see [Competitive Coding](https://github.com/kunalaher168-coder/competitive-coding).
