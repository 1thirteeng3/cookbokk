"""Build the bilingual site with Zensical: one site per language, linked by a language selector.

    python tools/build_site.py build            # site/ (pt) and site/en/ (en)
    python tools/build_site.py serve --lang en  # live preview of one language

Zensical supports a single language per site (no i18n plugin), so for each language this script:
  1. stages docs/ into build/site-src/<lang>/ with symlinks: ``index.<lang>.md`` -> ``index.md``;
     other languages, notebooks, YAML and JSON are left out; assets are linked as-is;
  2. writes .zensical.<lang>.toml (repo root, git-ignored) from config/site.base.toml + language, nav and selector;
  3. runs ``zensical build`` (pt into site/, en into site/en/).

Symlinks keep ``serve`` live: editing docs/**/index.<lang>.md reloads the preview. New or
renamed files need a restart.
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import tomllib
from pathlib import Path

import tomli_w

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import DOCS, LANGS, ROOT, load_catalog, load_yaml  # noqa: E402
from render import nav  # noqa: E402

BASE = ROOT / "config" / "site.base.toml"
BUILD = ROOT / "build"
SITE = ROOT / "site"
SKIP_SUFFIXES = {".ipynb", ".yaml", ".yml", ".json"}
SKIP_NAMES = {".gitkeep"}
SKIP_DIRS = {".ipynb_checkpoints", "__pycache__", "mlruns", "artifacts", "results", "notebooks"}
LANG_META = {
    "pt": {"name": "Português", "theme": "pt-BR", "path": "/"},
    "en": {"name": "English", "theme": "en", "path": "/en/"},
}


def stage(lang: str) -> Path:
    dest = BUILD / "site-src" / lang
    if dest.exists():
        shutil.rmtree(dest)
    others = {f".{o}.md" for o in LANGS if o != lang}
    n = 0
    for src in DOCS.rglob("*"):
        if not src.is_file() or src.suffix in SKIP_SUFFIXES or src.name in SKIP_NAMES:
            continue
        if any(src.name.endswith(o) for o in others) or SKIP_DIRS & set(
            src.relative_to(DOCS).parts
        ):
            continue
        rel = src.relative_to(DOCS)
        if src.name.endswith(f".{lang}.md"):
            rel = rel.with_name(src.name.removesuffix(f".{lang}.md") + ".md")
        target = dest / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.symlink_to(src.resolve())
        n += 1
    print(f"staged {n} file(s) for '{lang}' in {dest.relative_to(ROOT)}")
    return dest


def config(lang: str, docs_dir: Path) -> Path:
    cfg = tomllib.loads(BASE.read_text(encoding="utf-8"))
    repo = load_yaml(ROOT / "config" / "cookbook.yml")
    project = cfg["project"]
    project["docs_dir"] = docs_dir.relative_to(ROOT).as_posix()
    project["site_dir"] = (SITE if lang == "pt" else SITE / lang).relative_to(ROOT).as_posix()
    if repo.get("site_url"):
        project["site_url"] = repo["site_url"].rstrip("/") + LANG_META[lang]["path"]
    project["theme"]["language"] = LANG_META[lang]["theme"]
    project["nav"] = nav(load_catalog(), lang)
    project.setdefault("extra", {})["alternate"] = [
        {"name": m["name"], "link": m["path"], "lang": code} for code, m in LANG_META.items()
    ]
    # Zensical requires site_dir inside the config file's folder: configs live at the repo root.
    path = ROOT / f".zensical.{lang}.toml"
    header = "# GERADO por tools/build_site.py. Não edite. / GENERATED. Do not edit.\n\n"
    path.write_text(header + tomli_w.dumps(cfg), encoding="utf-8")
    return path


def zensical(*args: str) -> int:
    exe = shutil.which("zensical") or str(Path(sys.executable).parent / "zensical")
    return subprocess.run([exe, *args], cwd=ROOT).returncode


def cmd_build(args) -> int:
    if SITE.exists():
        shutil.rmtree(SITE)
    for lang in LANGS:  # pt first: it owns site/, en goes into site/en/
        cfg = config(lang, stage(lang))
        flags = ["build", "-f", str(cfg), "--clean"] + (["--strict"] if args.strict else [])
        if (rc := zensical(*flags)) != 0:
            print(f"zensical build failed for '{lang}'")
            return rc
    print(f"site ready: {SITE.relative_to(ROOT)}/ (pt) and {SITE.relative_to(ROOT)}/en/ (en)")
    return 0


def cmd_serve(args) -> int:
    cfg = config(args.lang, stage(args.lang))
    return zensical("serve", "-f", str(cfg), "-a", args.addr)


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    sub = ap.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("build")
    b.add_argument("--no-strict", dest="strict", action="store_false")
    s = sub.add_parser("serve")
    s.add_argument("--lang", choices=LANGS, default="pt")
    s.add_argument("--addr", default="localhost:8000")
    args = ap.parse_args()
    return {"build": cmd_build, "serve": cmd_serve}[args.cmd](args)


if __name__ == "__main__":
    raise SystemExit(main())
