import json

import pytest

from cookbook import data, env, results
from cookbook.validation import errors


def test_synthetic_dataset_is_deterministic():
    a, meta = data.fetch("synthetic-credit")
    b, _ = data.fetch("synthetic-credit")
    assert a.equals(b)
    assert meta["n_rows"] == len(a) == 20_000
    assert 0.05 < a["default"].mean() < 0.3


def test_sample_is_stratified_and_deterministic():
    df, _ = data.fetch("synthetic-credit")
    s1 = data.sample(df, 0.1, seed=1, stratify="default")
    s2 = data.sample(df, 0.1, seed=1, stratify="default")
    assert s1.index.equals(s2.index)
    assert abs(s1["default"].mean() - df["default"].mean()) < 0.01
    with pytest.raises(ValueError):
        data.sample(df, 0)


def test_unknown_dataset():
    with pytest.raises(KeyError):
        data.fetch("nope")


def test_env_helpers():
    env.set_seeds(7)
    hw = env.hardware_info()
    assert hw["platform"] in {"local", "ci", "colab"}
    assert hw["ram_gb"] >= 0
    v = env.versions(["pandas", "definitely-not-installed"])
    assert v["python"].startswith("3.")
    assert v["definitely-not-installed"] == "not-installed"


def test_summarize():
    s = results.summarize([0.5, 0.6, 0.7])
    assert s == {"mean": 0.6, "std": 0.1, "n": 3}
    assert results.summarize([1.0])["std"] is None


def _result_kwargs(**over):
    kw = dict(
        recipe_id="N1.01",
        notebook="01-x",
        stack="x",
        run_mode="smoke",
        hardware=env.hardware_info(),
        versions=env.versions(["pandas"]),
        dataset={"name": "d"},
        params={},
        metrics={"gini": results.summarize([0.5, 0.52])},
        time_s={"train": 1.0, "inference_per_1k": None},
    )
    kw.update(over)
    return kw


def test_save_result_roundtrip(tmp_path):
    p = results.save_result(**_result_kwargs(results_dir=tmp_path, variant="bins=10"))
    assert p.name == "01-x__x__bins-10.smoke.json"
    doc = json.loads(p.read_text())
    assert errors("result", doc) == []


def test_save_result_rejects_invalid(tmp_path):
    with pytest.raises(ValueError, match="invalid result"):
        results.save_result(**_result_kwargs(results_dir=tmp_path, metrics={}))


def test_timer():
    with results.Timer() as t:
        sum(range(1000))
    assert t.seconds >= 0


def test_two_stacks_same_notebook_do_not_overwrite(tmp_path):
    a = results.save_result(**_result_kwargs(results_dir=tmp_path, stack="model"))
    b = results.save_result(**_result_kwargs(results_dir=tmp_path, stack="baseline"))
    assert a != b and a.exists() and b.exists()
