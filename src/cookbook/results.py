"""Timing, metric aggregation and validated result files (``results/*.json``)."""

from __future__ import annotations

import json
import re
import subprocess
import time
from collections.abc import Iterable
from datetime import UTC, datetime
from pathlib import Path

from cookbook.validation import errors


class Timer:
    """``with Timer() as t: ...`` then ``t.seconds``."""

    def __enter__(self) -> Timer:
        self._start = time.perf_counter()
        self.seconds = 0.0
        return self

    def __exit__(self, *exc) -> None:
        self.seconds = round(time.perf_counter() - self._start, 4)


def summarize(values: Iterable[float]) -> dict:
    """``{"mean", "std", "n"}`` with sample std (ddof=1); std is None for n=1."""
    vals = [float(v) for v in values]
    if not vals:
        raise ValueError("no values")
    n = len(vals)
    mean = sum(vals) / n
    std = (sum((v - mean) ** 2 for v in vals) / (n - 1)) ** 0.5 if n > 1 else None
    return {"mean": round(mean, 6), "std": None if std is None else round(std, 6), "n": n}


def peak_mem_mb() -> float | None:
    try:
        import resource

        return round(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024, 1)  # Linux: KB
    except (ImportError, AttributeError):
        return None


def git_sha() -> str | None:
    try:
        out = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"], capture_output=True, text=True, timeout=5
        )
        return out.stdout.strip() or None
    except (OSError, subprocess.SubprocessError):
        return None


def _slug(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def result_path(
    results_dir: Path, notebook: str, run_mode: str, variant: str | None, stack: str | None = None
) -> Path:
    """``results/<notebook>__<stack>[__<variant>].<run_mode>.json``.

    The stack is part of the name so one notebook can record several stacks (e.g. a model
    and its baseline) without overwriting each other.
    """
    parts = [notebook] + ([_slug(stack)] if stack else []) + ([_slug(variant)] if variant else [])
    return results_dir / f"{'__'.join(parts)}.{run_mode}.json"


def save_result(
    *,
    recipe_id: str,
    notebook: str,
    stack: str,
    run_mode: str,
    hardware: dict,
    versions: dict,
    dataset: dict,
    params: dict,
    metrics: dict,
    time_s: dict,
    variant: str | None = None,
    results_dir: str | Path = "results",
    peak_mem: float | None = None,
) -> Path:
    """Validate against ``result.schema.json`` and write it (see :func:`result_path`)."""
    doc = {
        "recipe_id": recipe_id,
        "notebook": notebook,
        "stack": stack,
        "run_mode": run_mode,
        "timestamp": datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "git_sha": git_sha(),
        "hardware": hardware,
        "versions": versions,
        "dataset": dataset,
        "params": params,
        "metrics": metrics,
        "time_s": time_s,
        "peak_mem_mb": peak_mem if peak_mem is not None else peak_mem_mb(),
    }
    if variant is not None:
        doc["variant"] = variant
    problems = errors("result", doc)
    if problems:
        raise ValueError("invalid result:\n  " + "\n  ".join(problems))
    path = result_path(Path(results_dir), notebook, run_mode, variant, stack)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return path
