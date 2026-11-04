"""Split bilingual source notebooks into per-language notebooks.

Text cells tagged ``lang:pt`` / ``lang:en`` go only to that language; untagged cells
(code and shared markdown) go to both. The ``lang:*`` tag is removed from the output and
Colab badges are pointed at the right language folder.

Usage:
    python tools/split_notebooks.py <src_root> <out_root> [--langs pt en]

Example:
    python tools/split_notebooks.py docs build/colab
    # docs/recipes/.../notebooks/01-x.ipynb -> build/colab/pt/recipes/.../notebooks/01-x.ipynb
"""

from __future__ import annotations

import argparse
import copy
import re
from pathlib import Path

import nbformat

LANG_TAG = re.compile(r"^lang:(?P<lang>[a-z]{2})$")


def cell_langs(cell) -> set[str]:
    tags = cell.get("metadata", {}).get("tags", [])
    return {m["lang"] for t in tags if (m := LANG_TAG.match(t))}


def split(nb, lang: str):
    out = copy.deepcopy(nb)
    kept = []
    for cell in out.cells:
        langs = cell_langs(cell)
        if langs and lang not in langs:
            continue
        tags = [t for t in cell.metadata.get("tags", []) if not LANG_TAG.match(t)]
        if tags:
            cell.metadata["tags"] = tags
        else:
            cell.metadata.pop("tags", None)
        if cell.cell_type == "markdown":
            cell.source = re.sub(r"/blob/colab/[a-z]{2}/", f"/blob/colab/{lang}/", cell.source)
        kept.append(cell)
    out.cells = kept
    out.metadata.setdefault("cookbook", {})
    out.metadata["cookbook"].update({"source_notebook": False, "language": lang})
    out.metadata["cookbook"].pop("languages", None)
    return out


def check_pairs(nb, langs: list[str], path: Path) -> list[str]:
    """Every language must have the same number of tagged text cells."""
    counts = {lang: sum(lang in cell_langs(c) for c in nb.cells) for lang in langs}
    if len(set(counts.values())) > 1:
        return [f"{path}: unbalanced language cells {counts}"]
    return []


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("src_root", type=Path)
    ap.add_argument("out_root", type=Path)
    ap.add_argument("--langs", nargs="+", default=["pt", "en"])
    args = ap.parse_args()

    errors: list[str] = []
    n = 0
    for src in sorted(args.src_root.rglob("*.ipynb")):
        if ".ipynb_checkpoints" in src.parts:
            continue
        nb = nbformat.read(src, as_version=4)
        errors += check_pairs(nb, args.langs, src)
        rel = src.relative_to(args.src_root)
        for lang in args.langs:
            dst = args.out_root / lang / rel
            dst.parent.mkdir(parents=True, exist_ok=True)
            out = split(nb, lang)
            nbformat.validate(out)
            nbformat.write(out, dst)
        n += 1
    for e in errors:
        print("ERROR", e)
    print(f"split {n} notebook(s) into {args.langs}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
