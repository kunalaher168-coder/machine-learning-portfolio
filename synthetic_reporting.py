"""Create a public example map and report from wholly invented observations."""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass
from html import escape
import math
from pathlib import Path


CATEGORIES = ("candidate", "verified", "needs review")
COLORS = {"candidate": "#5470a7", "verified": "#27866a", "needs review": "#bb6c2e"}


@dataclass(frozen=True)
class Observation:
    identifier: str
    x: float
    y: float
    category: str

    def __post_init__(self) -> None:
        if not self.identifier.strip():
            raise ValueError("identifier cannot be empty")
        if self.category not in CATEGORIES:
            raise ValueError("unknown category")
        if not all(math.isfinite(v) and 0 <= v <= 1 for v in (self.x, self.y)):
            raise ValueError("coordinates must be finite unit-square values")


def synthetic_observations() -> list[Observation]:
    """Return fixed, invented positions with no geographic reference system."""
    return [
        Observation("S01", 0.12, 0.18, "verified"),
        Observation("S02", 0.28, 0.72, "candidate"),
        Observation("S03", 0.42, 0.31, "verified"),
        Observation("S04", 0.57, 0.58, "needs review"),
        Observation("S05", 0.76, 0.21, "candidate"),
        Observation("S06", 0.86, 0.78, "verified"),
        Observation("S07", 0.68, 0.85, "needs review"),
        Observation("S08", 0.32, 0.49, "verified"),
    ]


def summarize(observations: list[Observation]) -> dict[str, int]:
    identifiers = [item.identifier for item in observations]
    if len(identifiers) != len(set(identifiers)):
        raise ValueError("duplicate observation identifier")
    counts = Counter(item.category for item in observations)
    return {category: counts[category] for category in CATEGORIES}


def render_markdown(observations: list[Observation]) -> str:
    counts = summarize(observations)
    rows = [
        "# Synthetic observation report",
        "",
        "All positions and categories in this report are invented. Coordinates are local unit-square values.",
        "",
        f"Total observations: **{len(observations)}**",
        "",
        "| Category | Count | Share |",
        "| --- | ---: | ---: |",
    ]
    for category, count in counts.items():
        share = 100 * count / len(observations) if observations else 0
        rows.append(f"| {category.title()} | {count} | {share:.1f}% |")
    rows.extend(["", "See [map.svg](map.svg) for the schematic map.", ""])
    return "\n".join(rows)


def render_svg(observations: list[Observation]) -> str:
    summarize(observations)
    lines = [
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 450" role="img" aria-labelledby="title description">',
        '<title id="title">Synthetic observation map</title>',
        '<desc id="description">Invented observations on a local unit square, with category colors.</desc>',
        '<rect width="640" height="450" fill="#f8fafc"/>',
        '<text x="48" y="39" font-family="sans-serif" font-size="22" fill="#17324d">Synthetic observation map</text>',
        '<text x="48" y="61" font-family="sans-serif" font-size="12" fill="#53677a">Arbitrary local coordinates - no geographic reference</text>',
        '<rect x="48" y="82" width="400" height="320" fill="#ffffff" stroke="#a3b4c4" stroke-width="2"/>',
    ]
    for step in range(1, 4):
        gx = 48 + step * 100
        gy = 82 + step * 80
        lines.extend(
            [
                f'<path d="M {gx} 82 V 402" stroke="#e4ebf1"/>',
                f'<path d="M 48 {gy} H 448" stroke="#e4ebf1"/>',
            ]
        )
    for item in observations:
        x = 48 + 400 * item.x
        y = 402 - 320 * item.y
        label = escape(item.identifier, quote=True)
        color = COLORS[item.category]
        lines.extend(
            [
                f'<circle cx="{x:.1f}" cy="{y:.1f}" r="8" fill="{color}" stroke="#ffffff" stroke-width="2"/>',
                f'<text x="{x + 12:.1f}" y="{y + 4:.1f}" font-family="sans-serif" font-size="11" fill="#17324d">{label}</text>',
            ]
        )
    for index, category in enumerate(CATEGORIES):
        y = 120 + index * 34
        lines.extend(
            [
                f'<circle cx="487" cy="{y}" r="7" fill="{COLORS[category]}"/>',
                f'<text x="503" y="{y + 4}" font-family="sans-serif" font-size="13" fill="#17324d">{escape(category.title())}</text>',
            ]
        )
    lines.append('</svg>')
    return "\n".join(lines) + "\n"


def write_report(output_dir: Path, observations: list[Observation]) -> None:
    markdown = render_markdown(observations)
    svg = render_svg(observations)
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "report.md").write_text(markdown, encoding="utf-8")
    (output_dir / "map.svg").write_text(svg, encoding="utf-8")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=Path("output"))
    args = parser.parse_args()
    write_report(args.output_dir, synthetic_observations())
    print(f"Wrote synthetic report to {args.output_dir}")
