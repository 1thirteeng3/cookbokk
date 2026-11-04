"""End-to-end: promote a recipe in a copy of the repo, run a real notebook, render, validate, build."""

import os
import shutil
import subprocess
import sys
from pathlib import Path

import nbformat
import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]
pytestmark = pytest.mark.slow

NOTEBOOK_CELLS = [
    ("md", "pt", "# N1.01 · Teste\n## 0. Parâmetros"),
    ("md", "en", "# N1.01 · Test\n## 0. Parameters"),
    (
        "code",
        "parameters",
        'RUN_MODE = "smoke"\nSEED = 42\nDATA_DIR = "data"\nSAMPLE_FRAC = 0.2\nN_SEEDS = 3',
    ),
    (
        "code",
        None,
        (
            "from sklearn.linear_model import LogisticRegression\n"
            "from sklearn.metrics import roc_auc_score\n"
            "from sklearn.model_selection import train_test_split\n"
            "from cookbook.data import fetch, sample\n"
            "from cookbook.env import hardware_info, set_seeds, versions\n"
            "from cookbook.results import Timer, save_result, summarize\n"
            "set_seeds(SEED)\n"
            'df, DATASET = fetch("synthetic-credit", data_dir=DATA_DIR)\n'
            'if RUN_MODE == "smoke":\n'
            '    df = sample(df, SAMPLE_FRAC, SEED, stratify="default")\n'
            'X = df.drop(columns=["default", "region"]).fillna(df.median(numeric_only=True))\n'
            'y = df["default"]\n'
            "ginis = []\n"
            "with Timer() as t:\n"
            "    for s in range(N_SEEDS):\n"
            "        Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.3, stratify=y, random_state=s)\n"
            "        m = LogisticRegression(max_iter=1000).fit(Xtr, ytr)\n"
            "        ginis.append(2 * roc_auc_score(yte, m.predict_proba(Xte)[:, 1]) - 1)\n"
            'save_result(recipe_id="N1.01", notebook="01-logistic", stack="logistic", run_mode=RUN_MODE,\n'
            '            hardware=hardware_info(), versions=versions(["scikit-learn"]), dataset=DATASET,\n'
            '            params={"seed": SEED}, metrics={"gini": summarize(ginis)},\n'
            '            time_s={"train": t.seconds, "inference_per_1k": None})'
        ),
    ),
]


def _notebook() -> nbformat.NotebookNode:
    nb = nbformat.v4.new_notebook()
    for kind, tag, src in NOTEBOOK_CELLS:
        cell = (
            nbformat.v4.new_markdown_cell(src) if kind == "md" else nbformat.v4.new_code_cell(src)
        )
        if tag:
            cell.metadata["tags"] = [f"lang:{tag}"] if kind == "md" else [tag]
        nb.cells.append(cell)
    nb.metadata["kernelspec"] = {
        "name": "python3",
        "display_name": "Python 3",
        "language": "python",
    }
    return nb


def _run(args, cwd):
    env = dict(os.environ)
    r = subprocess.run([sys.executable, *args], cwd=cwd, capture_output=True, text=True, env=env)
    assert r.returncode == 0, r.stdout + r.stderr
    return r.stdout


@pytest.fixture
def repo(tmp_path):
    dst = tmp_path / "repo"
    dst.mkdir()
    for name in ("INDEX.md", "docs", "tools", "templates", "config"):
        src = ROOT / name
        (shutil.copytree if src.is_dir() else shutil.copy)(src, dst / name)
    return dst


def test_promote_run_render_validate_build(repo):
    _run(["tools/scaffold.py", "promote", "N1.01"], repo)
    item = next((repo / "docs/recipes/N-finance-economics/N1").glob("N1.01-*"))

    doc_pt = (item / "index.pt.md").read_text()
    assert "N1.01 · Scorecard de concessão com WoE/IV" in doc_pt
    assert (
        "blob/colab/pt/recipes/N-finance-economics/N1/N1.01-application-scorecard-woe-iv/" in doc_pt
    )

    # Fill metadata like an author would
    meta = yaml.safe_load((item / "recipe.yaml").read_text())
    meta["stacks"][0].update(
        id="logistic",
        name="LogisticRegression",
        notebook="notebooks/01-logistic.ipynb",
        packages={"scikit-learn": "1.0.0"},
    )
    meta["metrics"] = {"primary": "gini", "secondary": []}
    (item / "recipe.yaml").write_text(yaml.safe_dump(meta, allow_unicode=True, sort_keys=False))
    (item / "notebooks/01-todo-stack.ipynb").unlink()
    nbformat.write(_notebook(), item / "notebooks/01-logistic.ipynb")

    out = _run(["tools/run_notebooks.py", "N1.01", "--mode", "full"], repo)
    assert "1 passed" in out
    result = item / "results/01-logistic__logistic.full.json"
    assert result.exists()

    _run(["tools/render.py"], repo)
    doc_pt = (item / "index.pt.md").read_text()
    bench = doc_pt.split("<!-- BENCHMARK:START -->")[1].split("<!-- BENCHMARK:END -->")[0]
    assert "| logistic |" in bench and "±" in bench
    assert "✏️ rascunho" in (repo / "docs/recipes/N-finance-economics/index.pt.md").read_text()

    out = _run(["tools/validate.py"], repo)
    assert "0 error(s)" in out
    assert "TODO" in out  # draft: placeholders are warnings, not errors

    _run(["tools/split_notebooks.py", "docs", "build/colab"], repo)
    assert (
        repo
        / "build/colab/en/recipes/N-finance-economics/N1"
        / item.name
        / "notebooks/01-logistic.ipynb"
    ).exists()

    _run(["tools/build_site.py", "build"], repo)
    assert (repo / "site/en/recipes/N-finance-economics/N1" / item.name / "index.html").exists()
