import copy
import subprocess
import sys

import nbformat
import pytest
import render
import scaffold
import split_notebooks
import validate
from _common import ROOT, TEMPLATES, load_catalog, load_yaml

from cookbook.validation import errors


def test_parse_index_counts():
    parts, sections, recipes, projects = scaffold.parse_index()
    assert len(recipes) == 587
    assert len(projects) == 54
    assert set("ABCDEFGHIJKLMN") <= set(parts)
    assert len({r.id for r in recipes}) == len(recipes)
    for r in recipes:
        assert r.id.split(".")[0] in sections, r.id


@pytest.mark.parametrize(
    "text,item_id,expected",
    [
        (
            "Ingestão incremental / Incremental ingestion",
            "B1.04",
            ("Ingestão incremental", "Incremental ingestion"),
        ),
        ("AutoML", "D1.09", ("AutoML", "AutoML")),
        ("Autoencoders e VAEs", "E6.01", ("Autoencoders e VAEs", "Autoencoders and VAEs")),
        (
            "Agentes para dados (analista de dados / SQL / BI) / Data agents",
            "F3.11",
            ("Agentes para dados (analista de dados / SQL / BI)", "Data agents"),
        ),
    ],
)
def test_split_title(text, item_id, expected):
    assert scaffold.split_title(text, item_id) == expected


def test_slugify():
    assert scaffold.slugify("Application scorecard with WoE/IV") == "application-scorecard-woe-iv"
    assert scaffold.slugify("Ação & reação") == "acao-reacao"


def test_catalog_complete_and_valid():
    cat = load_catalog()
    assert len(cat.all_items()) == 641
    rep = validate.Report()
    for item in cat.all_items():
        validate.check_item(item, cat, rep)
    assert rep.errors == []


def test_generated_files_up_to_date():
    outputs = render.build(load_catalog())
    stale = [p for p, t in outputs.items() if not p.exists() or p.read_text(encoding="utf-8") != t]
    assert stale == [], "run `make render`"


def test_templates_valid():
    rec = load_yaml(TEMPLATES / "recipe" / "recipe.yaml")
    proj = load_yaml(TEMPLATES / "project" / "project.yaml")
    assert errors("recipe", rec) == []
    assert errors("project", proj) == []
    done = copy.deepcopy(rec)
    done.update(status="done", last_verified="2026-11-03")
    assert errors("recipe", done), "done with <pin> versions must be rejected"


def test_split_template_notebook():
    nb = nbformat.read(TEMPLATES / "recipe" / "notebooks" / "01-stack-template.ipynb", 4)
    pt, en = split_notebooks.split(nb, "pt"), split_notebooks.split(nb, "en")
    assert len(pt.cells) == len(en.cells)
    assert "Parâmetros" in "".join(c.source for c in pt.cells)
    assert "Parâmetros" not in "".join(c.source for c in en.cells)
    tags = [t for c in pt.cells for t in c.metadata.get("tags", [])]
    assert "parameters" in tags and not any(t.startswith("lang:") for t in tags)


def test_nbstripout_keeps_language_tags(tmp_path):
    nb = nbformat.read(TEMPLATES / "recipe" / "notebooks" / "01-stack-template.ipynb", 4)
    nb.cells[3].outputs = [nbformat.v4.new_output("stream", text="hi")]
    nb.cells[3].execution_count = 1
    p = tmp_path / "x.ipynb"
    nbformat.write(nb, p)
    subprocess.run([sys.executable, "-m", "nbstripout", str(p)], check=True)
    out = nbformat.read(p, 4)
    assert not any(c.get("outputs") for c in out.cells if c.cell_type == "code")
    assert sum("lang:pt" in c.metadata.get("tags", []) for c in out.cells) > 5
    assert any("parameters" in c.metadata.get("tags", []) for c in out.cells)


def test_placeholder_detection():
    text = "Use <br> here. Fill <Título da receita> and `a<b>c`.\n```\nx<y>\n```\n<!-- note -->"
    assert validate._placeholders(text) == ["<Título da receita>"]


def test_root_is_repo():
    assert (ROOT / "INDEX.md").exists()


def test_roadmap_covers_catalog_and_is_up_to_date():
    import roadmap

    cat = load_catalog()
    plan = roadmap.build_plan(cat)
    assert roadmap.check_coverage(plan) == []
    assert len(plan["rows"]) == 641
    assert [r["seq"] for r in plan["rows"]] == list(range(1, 642))
    # a project is never scheduled before the recipes it cites (except the finished pilot)
    seq = {r["id"]: r["seq"] for r in plan["rows"]}
    rids = sorted(i for i in plan["catalog"] if i[0] != "P")
    for item in cat.all_items():
        if item.kind != "project" or item.id == roadmap.PILOT:
            continue
        for token in item.meta.get("recipes", []):
            for r in roadmap.resolve_refs(token, rids):
                assert seq[r] < seq[item.id], f"{r} must come before {item.id}"
    outputs = roadmap.build(cat)
    stale = [
        p.name for p, t in outputs.items() if not p.exists() or p.read_text(encoding="utf-8") != t
    ]
    assert stale == [], "run `make roadmap`"
