# Object detection post-processing - public work sample

This branch shows the geometry and filtering step used after an object detector produces candidate boxes. It is a standalone reconstruction with invented coordinates, labels, and confidence scores. No private imagery, annotations, trained weights, or model package is included.

`detection_postprocess.py` computes intersection over union and applies class-aware non-maximum suppression. Input validation rejects invalid boxes, scores, and thresholds. The implementation uses only Python's standard library.

## Run tests

```powershell
python -m unittest discover -s tests -v
```

## Example input

Send JSON to standard input:

```json
{"detections":[{"box":[0,0,2,2],"score":0.9,"label":1},{"box":[0.1,0.1,2.1,2.1],"score":0.8,"label":1}],"threshold":0.5}
```

The output retains the higher-scoring box. This illustrates post-processing logic only, not detector quality.
