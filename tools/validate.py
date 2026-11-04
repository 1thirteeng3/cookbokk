"""Validate the whole cookbook: metadata, docs, notebooks, results and freshness.

    python tools/validate.py                 # errors fail (exit 1), warnings are printed
    python tools/validate.py --strict        # warnings also fail
    python tools/validate.py --only N1.01    # restrict to some IDs
    python tools/validate.py --outdated      # list items past their review cycle

Rules by status (SPEC.md §11):
    planned  schema + structure only
    draft    + docs/notebooks consistency; TODO and template placeholders are warnings
    review   placeholders, instruction comments and TODO become errors
    done     + full results present for every stack notebook, versions pinned (schema)
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path

import nbformat

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from _common import (  # noqa: E402
    LANGS,
    PART_FOLDERS,
    PROJECT_ID,
    RECIPE_ID,
    ROOT,
    Catalog,
    Item,
    load_catalog,
)

from cookbook.validation import errors as schema_errors  # noqa: E402

HTML_TAGS = {
    "br",
    "img",
    "a",
    "div",
    "span",
    "details",
    "summary",
    "p",
    "sup",
    "sub",
    "kbd",
    "code",
    "table",
    "tr",
    "td",
    "th",
    "figure",
    "figcaption",
    "small",
    "abbr",
}
RE_PLACEHOLDER = re.compile(r"<(?!!--)(?!/)([^<>\n]{1,80})>")
RE_COMMENT = re.compile(r"<!--(.*?)-->", re.S)
ALLOWED_COMMENTS = re.compile(
    r"^\s*(SUMMARY|BENCHMARK|PROGRESS|CATALOG|RESULTS-L[134]):(START|END)\s*$"
)
RE_REF = re.compile(r"^[A-N][0-9]{1,2}(\.[0-9]{2})?$")
LANG_TAG = re.compile(r"^lang:([a-z]{2})$")


class Report:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def err(self, where: str, msg: str) -> None:
        self.errors.append(f"{where}: {msg}")

    def warn(self, where: str, msg: str) -> None:
        self.warnings.append(f"{where}: {msg}")

    def add(self, strict: bool, where: str, msg: str) -> None:
        (self.err if strict else self.warn)(where, msg)


def _rel(p: Path) -> str:
    return p.relative_to(ROOT).as_posix()


def _placeholders(text: str) -> list[str]:
    body = RE_COMMENT.sub("", text)
    body = re.sub(r"```.*?```", "", body, flags=re.S)  # code blocks may contain generics
    body = re.sub(r"`[^`\n]*`", "", body)
    found = []
    for m in RE_PLACEHOLDER.finditer(body):
        inner = m.group(1).strip()
        first = re.split(r"[\s/>]", inner, maxsplit=1)[0].lower()
        if first in HTML_TAGS or inner.startswith(("http://", "https://")):
            continue
        found.append(m.group(0))
    return found


def _headings(text: str) -> list[str]:
    body = re.sub(r"```.*?```", "", text, flags=re.S)
    return [
        re.sub(r"^(#+).*", r"\1", line) + re.sub(r"^#+\s*([0-9.]*).*", r" \1", line)
        for line in body.splitlines()
        if re.match(r"^#{1,3} ", line)
    ]


def check_item(item: Item, cat: Catalog, rep: Report) -> None:
    where = _rel(item.path)
    kind = item.kind
    meta = item.meta
    status = meta.get("status", "planned")
    strict = status in ("review", "done")

    for e in schema_errors(kind, meta):
        rep.err(where, f"schema: {e}")

    # identity vs path
    folder_id, _, folder_slug = item.path.name.partition("-")
    if meta.get("id") != folder_id:
        rep.err(where, f"id {meta.get('id')!r} != folder {folder_id!r}")
    if meta.get("slug") != folder_slug:
        rep.err(where, f"slug {meta.get('slug')!r} != folder slug {folder_slug!r}")
    if kind == "recipe":
        m = RECIPE_ID.match(meta.get("id", ""))
        if m:
            if item.path.parents[1].name != PART_FOLDERS.get(m["part"]):
                rep.err(where, "recipe is in the wrong part folder")
            if item.path.parent.name != f"{m['part']}{m['sec']}":
                rep.err(where, "recipe is in the wrong section folder")
        for ref in meta.get("prerequisites", []) + meta.get("related", []):
            if ref not in cat.ids():
                rep.err(where, f"unknown reference {ref}")
    else:
        if not PROJECT_ID.match(meta.get("id", "")):
            rep.err(where, "bad project id")
        sections = {i.meta.get("section") for g in cat.parts.values() for i in g.items}
        for ref in meta.get("recipes", []):
            for piece in ref.split("–"):
                if not RE_REF.match(piece) or (piece not in cat.ids() and piece not in sections):
                    rep.err(where, f"unknown recipe reference {piece!r}")

    # docs
    texts = {}
    for lang in LANGS:
        doc = item.doc(lang)
        if not doc.exists():
            rep.err(where, f"missing {doc.name}")
            continue
        texts[lang] = doc.read_text(encoding="utf-8")
        fm = re.match(r"^---\n(.*?)\n---\n", texts[lang], re.S)
        if not fm or f"id: {meta.get('id')}" not in fm.group(1):
            rep.err(_rel(doc), "front matter must contain the item id")
    if status == "planned" or len(texts) < 2:
        return

    h_pt, h_en = _headings(texts["pt"]), _headings(texts["en"])
    if h_pt != h_en:
        rep.err(where, f"pt/en headings differ ({len(h_pt)} vs {len(h_en)} or numbering)")
    for lang, text in texts.items():
        doc = _rel(item.doc(lang))
        ph = _placeholders(text)
        if ph:
            rep.add(strict, doc, f"{len(ph)} template placeholder(s), e.g. {ph[:3]}")
        instr = [c for c in RE_COMMENT.findall(text) if not ALLOWED_COMMENTS.match(c)]
        if instr:
            rep.add(strict, doc, f"{len(instr)} template instruction comment(s) left")
    todo = json.dumps(meta, ensure_ascii=False).count("TODO")
    if todo:
        rep.add(strict, where, f"{todo} TODO value(s) in metadata")

    # notebooks
    declared = set()
    if kind == "recipe":
        declared |= {s["notebook"] for s in meta.get("stacks", [])}
        declared |= {a["notebook"] for a in meta.get("variation_axes", [])}
    else:
        for tier in meta.get("tiers", {}).values():
            declared |= set(tier.get("notebooks", []))
    present = {p.relative_to(item.path).as_posix() for p in item.path.glob("notebooks/*.ipynb")}
    for nb in sorted(declared - present):
        rep.add(strict, where, f"declared notebook missing: {nb}")
    for nb in sorted(present - declared - {"notebooks/90-benchmark.ipynb"}):
        rep.warn(where, f"notebook not declared in metadata: {nb}")
    for nb_rel in sorted(present):
        check_notebook(item.path / nb_rel, rep)

    # results
    results = sorted(item.path.glob("results/*.json"))
    for r in results:
        try:
            doc = json.loads(r.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            rep.err(_rel(r), f"invalid JSON: {e}")
            continue
        for e in schema_errors("result", doc):
            rep.err(_rel(r), f"schema: {e}")
        if doc.get("recipe_id") != meta.get("id"):
            rep.err(_rel(r), "recipe_id does not match the item")
    if status == "done" and kind == "recipe":
        full = {
            json.loads(r.read_text())["notebook"] for r in results if r.name.endswith(".full.json")
        }
        for s in meta.get("stacks", []):
            stem = Path(s["notebook"]).stem
            if stem not in full:
                rep.err(where, f"done but no full result for {stem}")


def check_notebook(path: Path, rep: Report) -> None:
    where = _rel(path)
    try:
        nb = nbformat.read(path, as_version=4)
        nbformat.validate(nb)
    except Exception as e:  # noqa: BLE001
        rep.err(where, f"invalid notebook: {e}")
        return
    counts = {lang: 0 for lang in LANGS}
    for cell in nb.cells:
        for t in cell.metadata.get("tags", []):
            if (m := LANG_TAG.match(t)) and m.group(1) in counts:
                counts[m.group(1)] += 1
        if cell.cell_type == "code" and (cell.get("outputs") or cell.get("execution_count")):
            rep.err(where, "outputs not stripped (run nbstripout / pre-commit)")
            break
    if len(set(counts.values())) > 1:
        rep.err(where, f"unbalanced language cells {counts}")
    if not any("parameters" in c.metadata.get("tags", []) for c in nb.cells):
        rep.err(where, "missing a cell tagged 'parameters'")


def outdated(cat: Catalog, today: date | None = None) -> list[tuple[Item, str]]:
    today = today or date.today()
    out = []
    for item in cat.all_items():
        lv = item.meta.get("last_verified")
        if item.status not in ("done", "review") or not lv:
            continue
        y, m, d = map(int, lv.split("-"))
        months = (today.year - y) * 12 + today.month - m - (today.day < d)
        if months >= item.meta["review_cycle_months"]:
            out.append((item, f"verified {lv}, cycle {item.meta['review_cycle_months']} months"))
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--strict", action="store_true", help="treat warnings as errors")
    ap.add_argument("--only", nargs="*", help="restrict to these IDs")
    ap.add_argument("--outdated", action="store_true", help="list items past their review cycle")
    args = ap.parse_args()

    cat = load_catalog()
    if args.outdated:
        rows = outdated(cat)
        for item, why in rows:
            print(f"OUTDATED {item.id}: {why}")
        print(f"{len(rows)} outdated item(s)")
        return 0

    rep = Report()
    seen: dict[str, Path] = {}
    for item in cat.all_items():
        if item.id in seen:
            rep.err(_rel(item.path), f"duplicate id (also {_rel(seen[item.id])})")
        seen[item.id] = item.path
        if args.only and item.id not in args.only:
            continue
        check_item(item, cat, rep)

    for w in rep.warnings:
        print("WARN ", w)
    for e in rep.errors:
        print("ERROR", e)
    by_status: dict[str, int] = {}
    for i in cat.all_items():
        by_status[i.status] = by_status.get(i.status, 0) + 1
    print(
        f"checked {len(cat.all_items())} items {by_status}: "
        f"{len(rep.errors)} error(s), {len(rep.warnings)} warning(s)"
    )
    failed = rep.errors or (args.strict and rep.warnings)
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
