"""Point every Colab badge and in-notebook install line to the repository in config/cookbook.yml.

    python tools/set_repo.py            # rewrite docs/ and templates/
    python tools/set_repo.py --check    # exit 1 if anything points elsewhere

Rewrites ``github.com/<anything>/ds-ai-cookbook`` (Colab URLs and ``git+https://...`` installs)
in docs/ Markdown and notebooks. Run it once after creating the GitHub repository.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import DOCS, ROOT, load_yaml  # noqa: E402

PATTERN = re.compile(r"(github(?:\.com)?/)([A-Za-z0-9_.-]+|<[a-z]+>)/ds-ai-cookbook")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    repo = load_yaml(ROOT / "config" / "cookbook.yml").get("github_repo", "OWNER/ds-ai-cookbook")
    owner, _, name = repo.partition("/")
    if name != "ds-ai-cookbook":
        print(
            "config/cookbook.yml: github_repo must end with /ds-ai-cookbook (folder links depend on it)"
        )
        return 1
    changed = []
    # templates/ keep their <user> placeholders: `scaffold.py promote` fills them per item
    for path in [*DOCS.rglob("*.md"), *DOCS.rglob("*.ipynb")]:
        text = path.read_text(encoding="utf-8")
        new = PATTERN.sub(lambda m: f"{m.group(1)}{owner}/ds-ai-cookbook", text)
        if new != text:
            changed.append(path)
            if not args.check:
                path.write_text(new, encoding="utf-8")
    verb = "would change" if args.check else "updated"
    print(f"{verb} {len(changed)} file(s) to github.com/{owner}/ds-ai-cookbook")
    return 1 if (args.check and changed) else 0


if __name__ == "__main__":
    raise SystemExit(main())
