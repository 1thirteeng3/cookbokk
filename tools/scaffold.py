"""Create the repository skeleton from INDEX.md and promote items to draft.

Commands:
    python tools/scaffold.py init              # create every planned recipe/project (never overwrites)
    python tools/scaffold.py promote N1.01     # copy templates into the item and set status: draft
    python tools/scaffold.py list [--status planned]

Folder slugs are derived once from the English title and are immutable afterwards: ``init``
matches existing folders by ID and leaves them untouched.
"""

from __future__ import annotations

import argparse
import re
import sys
import unicodedata
from dataclasses import dataclass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (  # noqa: E402
    DOCS,
    GROUP_DOMAINS,
    GROUP_FOLDERS,
    INDEX,
    LANGS,
    LEVEL_EMOJI,
    LEVEL_LABEL,
    PART_FOLDERS,
    PROJECTS,
    RECIPES,
    ROOT,
    TEMPLATES,
    dump_yaml,
    load_catalog,
    load_yaml,
    review_cycle,
    write_if_changed,
)

# ---------------------------------------------------------------------------------------
# Title fixes for INDEX rows that are not in the "PT / EN" form
# ---------------------------------------------------------------------------------------
TITLE_OVERRIDES = {
    "N1.05": (
        "Perda esperada IFRS 9 / CPC 48 / Resolução CMN 4.966",
        "Expected credit loss: IFRS 9 / CPC 48 / CMN Resolution 4.966",
    ),
}
EN_OVERRIDES = {
    "D2.13": "Survival analysis and churn",
    "E6.01": "Autoencoders and VAEs",
    "F2.08": "GraphRAG and knowledge graphs",
    "L2.05": "Neural likelihood and ratio estimation (NLE, NRE)",
}
# Parts H and I have no "###" subsections in INDEX.md
SECTION_FALLBACK = {
    "H1": ("Experimentação", "Experimentation"),
    "H2": ("Inferência causal", "Causal inference"),
    "H3": ("Interpretabilidade e equidade", "Interpretability and fairness"),
    "I1": (
        "Plataformas, infraestrutura, custo e segurança",
        "Platforms, infrastructure, cost and security",
    ),
}
STOPWORDS = {
    "a",
    "an",
    "the",
    "and",
    "or",
    "of",
    "for",
    "with",
    "in",
    "on",
    "from",
    "by",
    "as",
    "into",
    "its",
    "vs",
    "e",
    "g",
}

RE_PART = re.compile(r"^## PARTE (?P<code>[A-NP]): (?P<title>.+)$")
RE_SECTION = re.compile(r"^### (?P<code>[A-NP][0-9]{1,2})\. (?P<title>.+)$")
RE_RECIPE = re.compile(
    r"^\| (?P<id>[A-N][0-9]{1,2}\.[0-9]{2}) \| (?P<title>.+?) \| (?P<lvl>\S+) \| (?P<hint>.*) \|$"
)
RE_PROJECT = re.compile(
    r"^\| (?P<id>P[1-7]\.[0-9]{2}) \| (?P<title>.+?) \| (?P<recipes>.+?) \| (?P<data>.*) \|$"
)


def split_title(text: str, item_id: str | None = None) -> tuple[str, str]:
    text = text.strip()
    if item_id in TITLE_OVERRIDES:
        return TITLE_OVERRIDES[item_id]
    n = text.count(" / ")
    if n == 0:
        return text, EN_OVERRIDES.get(item_id, text)
    pt, en = text.rsplit(" / ", 1)
    return pt.strip(), en.strip()


def slugify(text: str, max_words: int = 6) -> str:
    ascii_text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode().lower()
    ascii_text = ascii_text.replace("&", " and ").replace("+", " plus ")
    words = [w for w in re.findall(r"[a-z0-9]+", ascii_text) if w not in STOPWORDS]
    return "-".join(words[:max_words]) or "item"


@dataclass
class Row:
    id: str
    pt: str
    en: str
    level: str | None = None
    hint: str = ""
    recipes: list[str] | None = None


def parse_index(path: Path = INDEX) -> tuple[dict, dict, list[Row], list[Row]]:
    parts: dict[str, dict] = {}
    sections: dict[str, dict] = {}
    recipes: list[Row] = []
    projects: list[Row] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if m := RE_PART.match(line):
            pt, en = split_title(m["title"])
            parts[m["code"]] = {"pt": pt, "en": en}
        elif m := RE_SECTION.match(line):
            pt, en = split_title(m["title"])
            sections[m["code"]] = {"pt": pt, "en": en}
        elif m := RE_RECIPE.match(line):
            pt, en = split_title(m["title"], m["id"])
            level = LEVEL_EMOJI.get(m["lvl"])
            if level is None:
                raise ValueError(f"{m['id']}: unknown level marker {m['lvl']!r}")
            recipes.append(Row(m["id"], pt, en, level, m["hint"].strip()))
        elif m := RE_PROJECT.match(line):
            pt, en = split_title(m["title"], m["id"])
            refs = [r.strip() for r in m["recipes"].split(",") if r.strip()]
            projects.append(Row(m["id"], pt, en, None, m["data"].strip(), refs))
    for code, (pt, en) in SECTION_FALLBACK.items():
        sections.setdefault(code, {"pt": pt, "en": en})
    return parts, sections, recipes, projects


# ---------------------------------------------------------------------------------------
# Stub pages
# ---------------------------------------------------------------------------------------
STUB = {
    "pt": {
        "planned": "Receita planejada",
        "planned_p": "Projeto planejado",
        "body": "Ainda não escrita. Veja o [catálogo]({back}) para o andamento.",
        "level": "Nível de entrada",
        "section": "Seção",
        "group": "Grupo",
        "hint": "Stacks e eixos a explorar",
        "recipes": "Receitas combinadas",
        "data": "Dados públicos sugeridos",
    },
    "en": {
        "planned": "Planned recipe",
        "planned_p": "Planned project",
        "body": "Not written yet. See the [catalog]({back}) for progress.",
        "level": "Entry level",
        "section": "Section",
        "group": "Group",
        "hint": "Stacks and axes to explore",
        "recipes": "Recipes combined",
        "data": "Suggested public data",
    },
}


def _front(item_id: str, title: str, status: str) -> str:
    # Status lives in recipe.yaml/project.yaml only: Material reserves the `status` front-matter key.
    del status
    safe = title.replace('"', "'")
    return f'---\nid: {item_id}\ntitle: "{item_id} · {safe}"\n---\n\n'


def recipe_stub(row: Row, lang: str, section_title: dict) -> str:
    t = STUB[lang]
    title = row.pt if lang == "pt" else row.en
    sec = section_title.get(lang, "")
    return (
        _front(row.id, title, "planned")
        + f"# {row.id} · {title}\n\n"
        + f'!!! note "{t["planned"]}"\n    {t["body"].format(back="../../index.md")}\n\n'
        + f"| {t['level']} | {t['section']} |\n|---|---|\n"
        + f"| {LEVEL_LABEL[lang][row.level]} | {row.id.split('.')[0]} · {sec} |\n\n"
        + f"**{t['hint']}:** {row.hint}\n"
    )


def project_stub(row: Row, lang: str, group_title: dict) -> str:
    t = STUB[lang]
    title = row.pt if lang == "pt" else row.en
    refs = ", ".join(f"`{r}`" for r in row.recipes or [])
    return (
        _front(row.id, title, "planned")
        + f"# {row.id} · {title}\n\n"
        + f'!!! note "{t["planned_p"]}"\n    {t["body"].format(back="../index.md")}\n\n'
        + f"| {t['group']} |\n|---|\n| {row.id.split('.')[0]} · {group_title[lang]} |\n\n"
        + f"**{t['recipes']}:** {refs}\n\n"
        + f"**{t['data']}:** {row.hint}\n"
    )


def _existing(folder: Path, item_id: str) -> Path | None:
    hits = sorted(folder.glob(f"{item_id}-*")) if folder.exists() else []
    return hits[0] if hits else None


def _unique_slug(folder: Path, item_id: str, slug: str) -> str:
    taken = (
        {p.name.split("-", 1)[1] for p in folder.glob("*-*") if p.is_dir()}
        if folder.exists()
        else set()
    )
    base, n = slug, 2
    while slug in taken:
        slug, n = f"{base}-{n}", n + 1
    return slug


def cmd_init(_args) -> int:
    parts, sections, recipes, projects = parse_index()
    created = skipped = 0

    for code, folder in PART_FOLDERS.items():
        secs = {
            s: sections[s]
            for s in sorted(
                {r.id.split(".")[0] for r in recipes if r.id[0] == code}, key=lambda s: int(s[1:])
            )
        }
        missing = [s for s in secs.values() if not s]
        if missing:
            raise ValueError(f"part {code}: section without title")
        part_meta = {"code": code, "title": parts[code], "sections": secs}
        write_if_changed(RECIPES / folder / "part.yaml", dump_yaml(part_meta))

    for row in recipes:
        part, section = row.id[0], row.id.split(".")[0]
        sec_dir = RECIPES / PART_FOLDERS[part] / section
        if _existing(sec_dir, row.id):
            skipped += 1
            continue
        slug = _unique_slug(sec_dir, row.id, slugify(row.en))
        item_dir = sec_dir / f"{row.id}-{slug}"
        meta = {
            "id": row.id,
            "slug": slug,
            "title": {"pt": row.pt, "en": row.en},
            "part": part,
            "section": section,
            "level": row.level,
            "status": "planned",
            "index_hint": row.hint,
            "environment": {"python": "3.12", "colab_runtime": "cpu"},
            "last_verified": None,
            "review_cycle_months": review_cycle(part, section),
        }
        write_if_changed(item_dir / "recipe.yaml", dump_yaml(meta))
        for lang in LANGS:
            write_if_changed(
                item_dir / f"index.{lang}.md", recipe_stub(row, lang, sections[section])
            )
        created += 1

    for code, folder in GROUP_FOLDERS.items():
        write_if_changed(
            PROJECTS / folder / "group.yaml", dump_yaml({"code": code, "title": sections[code]})
        )

    for row in projects:
        group = row.id.split(".")[0]
        g_dir = PROJECTS / GROUP_FOLDERS[group]
        if _existing(g_dir, row.id):
            skipped += 1
            continue
        slug = _unique_slug(g_dir, row.id, slugify(row.en))
        item_dir = g_dir / f"{row.id}-{slug}"
        meta = {
            "id": row.id,
            "slug": slug,
            "title": {"pt": row.pt, "en": row.en},
            "group": group,
            "domain": GROUP_DOMAINS[group],
            "status": "planned",
            "recipes": row.recipes,
            "index_hint": row.hint,
            "environment": {"python": "3.12", "colab_runtime": "cpu"},
            "last_verified": None,
            "review_cycle_months": 12,
        }
        write_if_changed(item_dir / "project.yaml", dump_yaml(meta))
        for lang in LANGS:
            write_if_changed(
                item_dir / f"index.{lang}.md", project_stub(row, lang, sections[group])
            )
        created += 1

    print(
        f"init: {created} created, {skipped} already existed "
        f"({len(recipes)} recipes, {len(projects)} projects in INDEX.md)"
    )
    return 0


# ---------------------------------------------------------------------------------------
# promote
# ---------------------------------------------------------------------------------------
TODO = "TODO"


def _repo() -> str:
    cfg = load_yaml(ROOT / "config" / "cookbook.yml")
    return cfg.get("github_repo", "OWNER/ds-ai-cookbook")


def _fill(text: str, item_id: str, title: dict, item_path: Path) -> str:
    rel = item_path.relative_to(DOCS).as_posix()
    repo = _repo()
    for ph in ("<caminho-da-receita>", "<recipe-path>", "<caminho-do-projeto>", "<project-path>"):
        text = text.replace(ph, rel)
    for ph in ("<usuario>/ds-ai-cookbook", "<user>/ds-ai-cookbook"):
        text = text.replace(ph, repo)
    return (
        text.replace("<PID>", item_id)
        .replace("<ID>", item_id)
        .replace("<Título da receita>", title["pt"])
        .replace("<Recipe title>", title["en"])
        .replace("<Título do projeto>", title["pt"])
        .replace("<Project title>", title["en"])
    )


def cmd_promote(args) -> int:
    cat = load_catalog()
    item = next((i for i in cat.all_items() if i.id == args.id), None)
    if item is None:
        print(f"unknown id {args.id}")
        return 1
    if item.status != "planned" and not args.force:
        print(f"{args.id} is '{item.status}', not 'planned' (use --force to overwrite docs)")
        return 1

    m = item.meta
    common = {
        "id": m["id"],
        "slug": m["slug"],
        "title": m["title"],
    }
    if item.kind == "recipe":
        tpl_dir = TEMPLATES / "recipe"
        meta = {
            **common,
            "part": m["part"],
            "section": m["section"],
            "level": m["level"],
            "status": "draft",
            "summary": {"pt": TODO, "en": TODO},
            "prerequisites": [],
            "related": [],
            "tags": [],
            "index_hint": m.get("index_hint", ""),
            "stacks": [
                {
                    "id": "todo-stack",
                    "name": TODO,
                    "level": m["level"],
                    "notebook": "notebooks/01-todo-stack.ipynb",
                    "packages": {},
                    "gpu": "none",
                    "runtime_min": {"smoke": 1, "full": 1},
                    "cost": "free",
                    "maturity": "stable",
                    "learning_curve": "low",
                }
            ],
            "variation_axes": [],
            "datasets": [
                {"name": TODO, "url": "https://example.org/TODO", "license": TODO, "loader": TODO}
            ],
            "metrics": {"primary": TODO, "secondary": []},
            "environment": m["environment"],
            "last_verified": None,
            "review_cycle_months": m["review_cycle_months"],
            "references": [],
        }
        yaml_name, nb_target = "recipe.yaml", "01-todo-stack.ipynb"
    else:
        tpl_dir = TEMPLATES / "project"
        meta = {
            **common,
            "group": m["group"],
            "domain": m["domain"],
            "status": "draft",
            "summary": {"pt": TODO, "en": TODO},
            "recipes": m["recipes"],
            "index_hint": m.get("index_hint", ""),
            "tiers": {
                lvl: {
                    "goal": {"pt": TODO, "en": TODO},
                    "notebooks": [f"notebooks/{n}-todo.ipynb"],
                    "stack": [TODO],
                }
                for lvl, n in (("L1", "10"), ("L3", "30"), ("L4", "40"))
            },
            "datasets": [
                {"name": TODO, "url": "https://example.org/TODO", "license": TODO, "loader": TODO}
            ],
            "business_metrics": [{"pt": TODO, "en": TODO}],
            "technical_metrics": [],
            "regulatory": [],
            "environment": m["environment"],
            "last_verified": None,
            "review_cycle_months": m["review_cycle_months"],
            "references": [],
        }
        yaml_name, nb_target = "project.yaml", "10-todo.ipynb"

    header = "# Promovido de 'planned' para 'draft'. Preencha os TODO. Spec: SPEC.md §6\n"
    (item.path / yaml_name).write_text(dump_yaml(meta, header), encoding="utf-8")
    for lang in LANGS:
        src = (tpl_dir / f"index.{lang}.md").read_text(encoding="utf-8")
        item.doc(lang).write_text(_fill(src, item.id, m["title"], item.path), encoding="utf-8")
    nb_src = TEMPLATES / "recipe" / "notebooks" / "01-stack-template.ipynb"
    nb_dst = item.path / "notebooks" / nb_target
    nb_dst.parent.mkdir(exist_ok=True)
    if not nb_dst.exists():
        nb_dst.write_text(
            _fill(nb_src.read_text(encoding="utf-8"), item.id, m["title"], item.path),
            encoding="utf-8",
        )
    for sub in ("results", "assets"):
        (item.path / sub).mkdir(exist_ok=True)
        (item.path / sub / ".gitkeep").touch()
    print(f"promoted {item.id} -> draft at {item.path.relative_to(RECIPES.parent.parent)}")
    print("next: rename the stack/notebook, fill the TODO fields, then run `make validate`.")
    return 0


def cmd_list(args) -> int:
    for item in load_catalog().all_items():
        if args.status and item.status != args.status:
            continue
        print(f"{item.id:7} {item.status:9} {item.title['pt']}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("init")
    p = sub.add_parser("promote")
    p.add_argument("id")
    p.add_argument("--force", action="store_true")
    ls = sub.add_parser("list")
    ls.add_argument("--status")
    args = ap.parse_args()
    return {"init": cmd_init, "promote": cmd_promote, "list": cmd_list}[args.cmd](args)


if __name__ == "__main__":
    raise SystemExit(main())
