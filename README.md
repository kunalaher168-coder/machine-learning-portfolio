# Geospatial reporting - public work sample

This branch demonstrates a small aerial-observation reporting workflow using invented coordinates in a unit square. It was rebuilt for public display. It contains no real imagery, map coordinates, customer information, private flowchart, or original notebook.

The script validates observations, summarizes counts by category, and creates a simple SVG map and Markdown report. Coordinates are arbitrary local positions from 0 to 1, not latitude or longitude.

## Run

```powershell
python synthetic_reporting.py --output-dir output
python -m unittest discover -s tests -v
```

`output/` contains the generated example report and map. The input records are created by the script and are not derived from client data. This sample shows data validation and reporting structure, not an operational mapping system.

The committed [sample report](sample_output/report.md) and [schematic SVG map](sample_output/map.svg) show the expected output.
