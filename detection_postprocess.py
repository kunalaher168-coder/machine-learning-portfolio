"""Class-aware non-maximum suppression for synthetic object detections."""

from __future__ import annotations

from dataclasses import asdict, dataclass
import json
import math
import sys


@dataclass(frozen=True)
class Detection:
    box: tuple[float, float, float, float]
    score: float
    label: int

    def __post_init__(self) -> None:
        if len(self.box) != 4 or not all(math.isfinite(value) for value in self.box):
            raise ValueError("box must contain four finite coordinates")
        left, top, right, bottom = self.box
        if left >= right or top >= bottom:
            raise ValueError("box needs positive width and height")
        if not math.isfinite(self.score) or not 0 <= self.score <= 1:
            raise ValueError("score must be between zero and one")


def intersection_over_union(first: Detection, second: Detection) -> float:
    """Return intersection area divided by union area."""
    ax1, ay1, ax2, ay2 = first.box
    bx1, by1, bx2, by2 = second.box
    width = max(0.0, min(ax2, bx2) - max(ax1, bx1))
    height = max(0.0, min(ay2, by2) - max(ay1, by1))
    intersection = width * height
    area_a = (ax2 - ax1) * (ay2 - ay1)
    area_b = (bx2 - bx1) * (by2 - by1)
    return intersection / (area_a + area_b - intersection)


def suppress_overlaps(detections: list[Detection], threshold: float = 0.5) -> list[Detection]:
    """Keep highest-scoring boxes; compare overlap only within a class."""
    if not math.isfinite(threshold) or not 0 <= threshold <= 1:
        raise ValueError("threshold must be between zero and one")
    ranked = sorted(enumerate(detections), key=lambda item: (-item[1].score, item[0]))
    kept: list[Detection] = []
    for _, candidate in ranked:
        if all(
            candidate.label != prior.label or intersection_over_union(candidate, prior) <= threshold
            for prior in kept
        ):
            kept.append(candidate)
    return kept


if __name__ == "__main__":
    payload = json.load(sys.stdin)
    items = [Detection(tuple(item["box"]), item["score"], item["label"]) for item in payload["detections"]]
    result = suppress_overlaps(items, payload.get("threshold", 0.5))
    print(json.dumps([asdict(item) for item in result]))
