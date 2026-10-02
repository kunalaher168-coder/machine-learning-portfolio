# Object Detection Post-Processing

An object detector can return several boxes for the same object. This public example implements the post-processing step that removes strongly overlapping, lower-scoring boxes within each class. The boxes and scores are invented; no model, image, annotation, or trained weight is included.

## Input and output

`detection_postprocess.py` accepts JSON on standard input with `detections` and an optional overlap `threshold` (default `0.5`). Each detection has a box `[left, top, right, bottom]`, a confidence `score`, and an integer class `label`. It writes the retained detections as JSON in descending score order.

The committed [sample input](sample_input.json) contains two overlapping class-1 boxes, one class-2 box at the same position, and one distant class-1 box. The [sample output](sample_output.json) removes only the lower-scoring duplicate from class 1.

```powershell
Get-Content sample_input.json -Raw | python detection_postprocess.py
python -m unittest discover -s tests -v
```

The module uses only Python's standard library and the tests run on Python 3.11 in [GitHub Actions](.github/workflows/tests.yml).

## Method

1. Validate that every box has four finite coordinates with positive width and height, and that scores and thresholds fall between zero and one.
2. Sort candidates by descending score, retaining input order for equal scores.
3. For each candidate, compute intersection over union (IoU) against already-kept boxes of the same class.
4. Suppress the candidate when IoU is greater than the threshold; keep boxes of different classes independently.

The greedy pairwise comparison has worst-case quadratic time in the number of candidate boxes. The tests cover IoU geometry, same-class suppression, cross-class retention, stable ordering, and invalid input.

## Scope

This branch demonstrates one component of a detection workflow. It does not train or evaluate a detector, compute mAP, or establish performance on any real image. No private model package, imagery, or client label set is present. See the [portfolio index](https://github.com/kunalaher168-coder/machine-learning-portfolio) for the other ML samples.
