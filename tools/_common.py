"""Shared definitions for repository tools: paths, parts, levels, YAML I/O, catalog loading."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
RECIPES = DOCS / "recipes"
PROJECTS = DOCS / "projects"
TEMPLATES = ROOT / "templates"
INDEX = ROOT / "INDEX.md"
LANGS = ("pt", "en")

PART_FOLDERS = {
    "A": "A-foundations",
    "B": "B-data-engineering",
    "C": "C-analysis-features",
    "D": "D-classical-ml",
    "E": "E-deep-learning",
    "F": "F-ai-engineering",
    "G": "G-mlops",
    "H": "H-stats-causal",
    "I": "I-platforms",
    "J": "J-llmops",
    "K": "K-dataops",
    "L": "L-generative-sciences",
    "M": "M-technical-audit",
    "N": "N-finance-economics",
}
GROUP_FOLDERS = {
    "P1": "P1-credit",
    "P2": "P2-fraud-aml",
    "P3": "P3-markets",
    "P4": "P4-macro",
    "P5": "P5-socioeconomics",
    "P6": "P6-financial-platforms",
    "P7": "P7-other-domains",
}
GROUP_DOMAINS = {
    "P1": "credit",
    "P2": "fraud-aml",
    "P3": "markets",
    "P4": "macro",
    "P5": "socioeconomics",
    "P6": "financial-platforms",
    "P7": "other",
}
LEVEL_EMOJI = {"🟢": "L1", "🟡": "L2", "🟠": "L3", "🔴": "L4"}
LEVEL_LABEL = {
    "pt": {
        "L1": "🟢 L1 · Introdutório",
        "L2": "🟡 L2 · Intermediário",
        "L3": "🟠 L3 · Avançado",
        "L4": "🔴 L4 · SOTA",
    },
    "en": {
        "L1": "🟢 L1 · Introductory",
        "L2": "🟡 L2 · Intermediate",
        "L3": "🟠 L3 · Advanced",
        "L4": "🔴 L4 · SOTA",
    },
}
STATUS_LABEL = {
    "pt": {
        "planned": "⚪ planejada",
        "draft": "✏️ rascunho",
        "review": "🔍 revisão",
        "done": "✅ pronta",
        "outdated": "⚠️ desatualizada",
    },
    "en": {
        "planned": "⚪ planned",
        "draft": "✏️ draft",
        "review": "🔍 review",
        "done": "✅ done",
        "outdated": "⚠️ outdated",
    },
}
# Projects are masculine in Portuguese ("projeto planejado")
PROJECT_STATUS_PT = {
    "planned": "⚪ planejado",
    "draft": "✏️ rascunho",
    "review": "🔍 revisão",
    "done": "✅ pronto",
    "outdated": "⚠️ desatualizado",
}
STATUSES = ("planned", "draft", "review", "done", "outdated")

# SPEC.md §12
FAST_SECTIONS = {"E4", "E5"}
REVIEW_CYCLE = {
    **dict.fromkeys("FJ", 3),
    **dict.fromkeys("BGKLM", 6),
    **dict.fromkeys("ACDHIN", 12),
    "E": 6,
}

RECIPE_ID = re.compile(r"^(?P<part>[A-N])(?P<sec>[0-9]{1,2})\.(?P<num>[0-9]{2})$")
PROJECT_ID = re.compile(r"^(?P<group>P[1-7])\.(?P<num>[0-9]{2})$")


def review_cycle(part: str, section: str) -> int:
    if section in FAST_SECTIONS:
        return 3
    return REVIEW_CYCLE[part]


# --------------------------------------------------------------------------------------
# YAML: dates stay strings (schema expects "YYYY-MM-DD"); readable dumps
# --------------------------------------------------------------------------------------


class _Loader(yaml.SafeLoader):
    pass


_Loader.yaml_implicit_resolvers = {
    k: [(tag, rx) for tag, rx in v if tag != "tag:yaml.org,2002:timestamp"]
    for k, v in yaml.SafeLoader.yaml_implicit_resolvers.items()
}


def load_yaml(path: Path) -> dict:
    return yaml.load(path.read_text(encoding="utf-8"), Loader=_Loader) or {}


class _Dumper(yaml.SafeDumper):
    pass


def _str_repr(dumper, data: str):
    style = ">" if len(data) > 90 and "\n" not in data else None
    return dumper.represent_scalar("tag:yaml.org,2002:str", data, style=style)


_Dumper.add_representer(str, _str_repr)


def dump_yaml(data: dict, header: str = "") -> str:
    body = yaml.dump(data, Dumper=_Dumper, sort_keys=False, allow_unicode=True, width=100)
    return (header + body) if header else body


def write_if_changed(path: Path, text: str) -> bool:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and path.read_text(encoding="utf-8") == text:
        return False
    path.write_text(text, encoding="utf-8")
    return True


# --------------------------------------------------------------------------------------
# Catalog: everything under docs/, loaded from YAML (source of truth after scaffold)
# --------------------------------------------------------------------------------------


@dataclass
class Item:
    kind: str  # "recipe" | "project"
    id: str
    path: Path  # folder
    meta: dict

    @property
    def title(self) -> dict:
        return self.meta["title"]

    @property
    def status(self) -> str:
        return self.meta["status"]

    def doc(self, lang: str) -> Path:
        return self.path / f"index.{lang}.md"

    def rel(self, base: Path) -> str:
        """Path of the item's index.md relative to ``base`` folder (for links/nav)."""
        return (self.path / "index.md").relative_to(base).as_posix()


@dataclass
class Group:
    """A part (A–N) or a project group (P1–P7)."""

    code: str
    path: Path
    meta: dict
    items: list[Item] = field(default_factory=list)


@dataclass
class Catalog:
    parts: dict[str, Group]
    groups: dict[str, Group]

    def all_items(self) -> list[Item]:
        out = [i for g in self.parts.values() for i in g.items]
        return out + [i for g in self.groups.values() for i in g.items]

    def ids(self) -> set[str]:
        return {i.id for i in self.all_items()}


def _sort_key(item_id: str) -> tuple:
    m = re.match(r"^([A-NP])([0-9]+)\.([0-9]+)$", item_id)
    return (m.group(1), int(m.group(2)), int(m.group(3))) if m else (item_id,)


def load_catalog() -> Catalog:
    parts: dict[str, Group] = {}
    for code, folder in PART_FOLDERS.items():
        p = RECIPES / folder
        if not (p / "part.yaml").exists():
            continue
        g = Group(code, p, load_yaml(p / "part.yaml"))
        for y in p.glob("*/*/recipe.yaml"):
            meta = load_yaml(y)
            g.items.append(Item("recipe", meta.get("id", y.parent.name), y.parent, meta))
        g.items.sort(key=lambda i: _sort_key(i.id))
        parts[code] = g
    groups: dict[str, Group] = {}
    for code, folder in GROUP_FOLDERS.items():
        p = PROJECTS / folder
        if not (p / "group.yaml").exists():
            continue
        g = Group(code, p, load_yaml(p / "group.yaml"))
        for y in p.glob("*/project.yaml"):
            meta = load_yaml(y)
            g.items.append(Item("project", meta.get("id", y.parent.name), y.parent, meta))
        g.items.sort(key=lambda i: _sort_key(i.id))
        groups[code] = g
    return Catalog(parts, groups)
