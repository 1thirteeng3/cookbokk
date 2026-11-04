"""Execute recipe/project notebooks with papermill (smoke in CI, full locally if desired).

    python tools/run_notebooks.py N1.01 P1.01             # all notebooks of these items
    python tools/run_notebooks.py --changed-since origin/main
    python tools/run_notebooks.py --all                   # every non-planned item
    python tools/run_notebooks.py N1.01 --mode full

The kernel runs with the item folder as working directory, so ``save_result`` writes into
``<item>/results/``. Executed copies go to ``build/executed/`` (sources stay stripped).
Notebooks still named ``*todo*`` or ``*template*`` are skipped.
"""

from __future__ import annotations

import argparse
import ast
import os
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import ROOT, Item, load_catalog  # noqa: E402

RUNNABLE = {"draft", "review", "done", "outdated"}


def changed_items(items: list[Item], ref: str) -> list[Item]:
    out = subprocess.run(
        ["git", "diff", "--name-only", f"{ref}...HEAD"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    ).stdout.split()
    changed = [ROOT / p for p in out]
    if any(p.is_relative_to(ROOT / "src" / "cookbook") for p in changed):
        return items  # shared code changed: re-run everything runnable
    return [i for i in items if any(p.is_relative_to(i.path) for p in changed)]


def notebooks_of(item: Item) -> list[Path]:
    nbs = sorted(item.path.glob("notebooks/*.ipynb"))
    return [p for p in nbs if not any(k in p.stem for k in ("todo", "template"))]


def run_one(
    nb: Path, item: Item, params: dict, out_root: Path, timeout: int
) -> tuple[bool, float, str]:
    import papermill as pm

    out = out_root / nb.relative_to(ROOT)
    out.parent.mkdir(parents=True, exist_ok=True)
    start = time.perf_counter()
    try:
        pm.execute_notebook(
            str(nb),
            str(out),
            parameters=params,
            cwd=str(item.path),
            kernel_name="python3",
            progress_bar=False,
            execution_timeout=timeout,
            log_output=False,
        )
        return True, time.perf_counter() - start, ""
    except Exception as e:  # noqa: BLE001
        msg = str(e).strip().splitlines()
        return False, time.perf_counter() - start, (msg[-1] if msg else repr(e))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("ids", nargs="*")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--changed-since")
    ap.add_argument("--mode", choices=["smoke", "full"], default="smoke")
    ap.add_argument(
        "--data-dir", type=Path, default=Path(os.environ.get("COOKBOOK_DATA_DIR", ROOT / "data"))
    )
    ap.add_argument("--out", type=Path, default=ROOT / "build" / "executed")
    ap.add_argument("--timeout", type=int, default=900, help="seconds per cell")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument(
        "--offline",
        action="store_true",
        default=bool(os.environ.get("COOKBOOK_OFFLINE")),
        help="pass OFFLINE=True: notebooks use synthetic twins instead of downloads (CI, tests)",
    )
    ap.add_argument(
        "-p",
        "--param",
        action="append",
        default=[],
        metavar="KEY=VALUE",
        help="extra papermill parameter (value parsed as Python literal when possible)",
    )
    args = ap.parse_args()

    items = [i for i in load_catalog().all_items() if i.status in RUNNABLE]
    if args.ids:
        items = [i for i in items if i.id in set(args.ids)]
    elif args.changed_since:
        items = changed_items(items, args.changed_since)
    elif not args.all:
        ap.error("give IDs, --changed-since REF or --all")

    jobs = [(nb, i) for i in items for nb in notebooks_of(i)]
    print(f"{len(jobs)} notebook(s) from {len(items)} item(s), mode={args.mode}")
    if args.dry_run:
        for nb, _ in jobs:
            print("  ", nb.relative_to(ROOT))
        return 0

    args.data_dir.mkdir(parents=True, exist_ok=True)
    params = {
        "RUN_MODE": args.mode,
        "DATA_DIR": str(args.data_dir.resolve()),
        "OFFLINE": args.offline,
    }
    for kv in args.param:
        key, _, raw = kv.partition("=")
        try:
            params[key] = ast.literal_eval(raw)
        except (ValueError, SyntaxError):
            params[key] = raw
    failures = 0
    for nb, item in jobs:
        ok, secs, msg = run_one(nb, item, params, args.out, args.timeout)
        failures += not ok
        print(
            f"{'PASS' if ok else 'FAIL'} {secs:7.1f}s  {nb.relative_to(ROOT)}"
            + (f"\n      {msg}" if msg else "")
        )
    print(f"{len(jobs) - failures} passed, {failures} failed")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
