#!/usr/bin/env python3
"""Extracts RL training curves from local TensorBoard event files into a small JSON
file the site can statically import.

Walks `<cache-dir>/<experiment>/<variant>/seed<K>/<timestamp>/events.out.tfevents.*`,
picks one run per variant+seed (the timestamp with the most points for the target
tag), downsamples each series, and writes the result to `--out`.

Run with the tensorboard venv:
    ~/.venvs/tensorboard/bin/python scripts/extract_training_curves.py
"""

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from tensorboard.backend.event_processing.event_accumulator import EventAccumulator


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--cache-dir",
        type=Path,
        default=Path("~/.cache/rl-manipulation-hks-runs").expanduser(),
        help="Root dir mirroring the GCS bucket of run logs.",
    )
    parser.add_argument("--experiment", default="asset-bisect")
    parser.add_argument("--tag", default="Train/mean_reward")
    parser.add_argument(
        "--out",
        type=Path,
        default=Path("src/data/training-curves.json"),
    )
    parser.add_argument(
        "--max-points",
        type=int,
        default=200,
        help="Downsample each series to at most this many points.",
    )
    return parser.parse_args()


def round_sig(value: float, sig: int = 4) -> float:
    """Round to `sig` significant digits."""
    if value == 0:
        return 0.0
    from math import floor, log10

    digits = sig - int(floor(log10(abs(value)))) - 1
    return round(value, digits)


def downsample(points: list[tuple[int, float]], max_points: int) -> list[tuple[int, float]]:
    """Keep at most `max_points`, always including the first and last."""
    if len(points) <= max_points:
        return points
    if max_points < 2:
        return [points[0]]
    indices = sorted({round(i * (len(points) - 1) / (max_points - 1)) for i in range(max_points)})
    return [points[i] for i in indices]


def load_tag_points(run_dir: Path, tag: str) -> list[tuple[int, float]] | None:
    """Returns [(step, value), ...] for `tag` in `run_dir`, or None if the tag is absent."""
    ea = EventAccumulator(str(run_dir), size_guidance={"scalars": 0})
    ea.Reload()
    if tag not in ea.Tags().get("scalars", []):
        return None
    return [(event.step, event.value) for event in ea.Scalars(tag)]


def best_run_for_seed(seed_dir: Path, tag: str) -> list[tuple[int, float]] | None:
    """Across every timestamp dir under `seed_dir`, keep the run with the most
    points for `tag`. Returns None if no timestamp has the tag at all."""
    best: list[tuple[int, float]] | None = None
    for timestamp_dir in sorted(p for p in seed_dir.iterdir() if p.is_dir()):
        points = load_tag_points(timestamp_dir, tag)
        if points is None:
            continue
        if best is None or len(points) > len(best):
            best = points
    return best


def main() -> None:
    args = parse_args()
    experiment_dir = args.cache_dir / args.experiment
    if not experiment_dir.is_dir():
        sys.exit(f"experiment dir not found: {experiment_dir}")

    series = []
    missing_tag: list[str] = []
    for variant_dir in sorted(p for p in experiment_dir.iterdir() if p.is_dir()):
        variant = variant_dir.name
        for seed_dir in sorted(p for p in variant_dir.iterdir() if p.is_dir()):
            if not seed_dir.name.startswith("seed"):
                continue
            seed = seed_dir.name.removeprefix("seed")
            points = best_run_for_seed(seed_dir, args.tag)
            if points is None:
                missing_tag.append(f"{variant}/{seed_dir.name}")
                continue
            points.sort(key=lambda p: p[0])
            points = downsample(points, args.max_points)
            series.append(
                {
                    "variant": variant,
                    "seed": seed,
                    "points": [[step, round_sig(value)] for step, value in points],
                }
            )

    if missing_tag:
        sys.exit(
            f"tag {args.tag!r} missing for {len(missing_tag)} run(s): {', '.join(missing_tag)}"
        )
    if not series:
        sys.exit(f"no runs found under {experiment_dir}")

    payload = {
        "experiment": args.experiment,
        "tag": args.tag,
        "generated": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        "series": series,
    }

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(payload, indent=2) + "\n")
    print(f"wrote {len(series)} series to {args.out}")


if __name__ == "__main__":
    main()
