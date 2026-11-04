import pickle

import numpy as np
import pandas as pd
import pytest

from cookbook import credit as cr
from cookbook import home_credit as hc


@pytest.fixture(scope="module")
def twin():
    return hc.load("home-credit-synthetic", n_synthetic=6_000, seed=7)


# ------------------------------------------------------------------ credit metrics
def test_gini_ks_bounds_and_direction():
    rng = np.random.default_rng(0)
    y = rng.binomial(1, 0.2, 5_000)
    good_score = y + rng.normal(0, 0.5, 5_000)
    assert cr.gini(y, good_score) > 0.5
    assert cr.gini(y, -good_score) < -0.5
    assert 0 < cr.ks(y, good_score) <= 1
    assert abs(cr.gini(y, rng.random(5_000))) < 0.1


def test_bootstrap_format():
    rng = np.random.default_rng(1)
    y, s = rng.binomial(1, 0.3, 800), rng.random(800)
    out = cr.bootstrap(cr.gini, y, s, n=30)
    assert set(out) == {"mean", "std", "n"} and out["n"] == 30 and out["std"] > 0


def test_psi_numeric_and_categorical():
    rng = np.random.default_rng(2)
    a = rng.normal(size=20_000)
    assert cr.psi(a, rng.normal(size=20_000)) < 0.01
    assert cr.psi(a, rng.normal(1.0, 1, 20_000)) > 0.25
    cats = pd.Series(rng.choice(["x", "y", "z"], 5_000), dtype="str")
    assert cr.psi(cats, cats.sample(frac=1, random_state=0)) < 1e-6
    assert cr.psi(cats, pd.Series(["x"] * 5_000, dtype="str")) > 0.25
    assert cr.psi_label(0.05) == "estável" and cr.psi_label(0.3, "en") == "significant shift"


def test_score_scale():
    pd_at_base = 1 / (1 + 50)  # odds good:bad = 50
    assert cr.score_from_pd(pd_at_base) == pytest.approx(600)
    assert cr.score_from_pd(1 / (1 + 100)) == pytest.approx(620)  # odds doubled -> +PDO
    p = np.linspace(0.01, 0.9, 50)
    assert np.all(np.diff(cr.score_from_pd(p)) < 0)


def test_cutoffs_and_profit():
    rng = np.random.default_rng(3)
    p = rng.random(2_000)
    y = rng.binomial(1, p)
    table = cr.cutoff_table(y, p)
    assert table["bad_rate_approved"].is_monotonic_increasing
    approved = p < 0.5
    exposure = np.full(2_000, 100.0)
    expected = np.where(y[approved] == 1, -60.0, 10.0).sum()
    assert cr.realized_profit(y, exposure, approved, 0.10, 0.60) == pytest.approx(expected)
    curve = cr.policy_curve(y, p, exposure, 0.10, 0.60, n_points=21)
    assert curve["approval_rate"].is_monotonic_increasing


def test_reason_codes_only_positive():
    contrib = np.array([[0.5, -1.0, 0.2], [-0.1, -0.2, -0.3]])
    assert cr.reason_codes(contrib, ["a", "b", "c"], k=2) == [["a", "c"], []]


@pytest.mark.parametrize("method", ["identity", "platt", "isotonic"])
def test_calibrator_roundtrip(method):
    rng = np.random.default_rng(4)
    raw = rng.random(3_000)
    y = rng.binomial(1, raw**2)
    cal = pickle.loads(pickle.dumps(cr.ProbabilityCalibrator(method).fit(raw, y)))
    out = cal.predict(raw)
    assert out.shape == raw.shape and np.all((out >= 0) & (out <= 1))
    if method != "identity":
        assert cr.ece(y, out) < cr.ece(y, raw)


# ------------------------------------------------------------------ home credit
def test_twin_shape_and_rates(twin):
    app, bureau, meta = twin
    assert list(app.columns) == hc.APPLICATION_COLUMNS
    assert list(bureau.columns) == hc.BUREAU_COLUMNS
    assert 0.06 < app[hc.TARGET].mean() < 0.10
    assert app[hc.ID].is_unique and meta["n_rows"] == len(app)
    assert (app["DAYS_EMPLOYED"] == hc.DAYS_EMPLOYED_ANOMALY).mean() > 0.1


def test_clean_flags_sentinel(twin):
    app = hc.clean(twin[0])
    assert app["DAYS_EMPLOYED"].max() < 0
    assert (
        app["DAYS_EMPLOYED_ANOM"].sum()
        == (twin[0]["DAYS_EMPLOYED"] == hc.DAYS_EMPLOYED_ANOMALY).sum()
    )
    assert "XNA" not in set(app["CODE_GENDER"].dropna())


def test_split_is_stable(twin):
    ids = twin[0][hc.ID]
    a = hc.split(ids)
    b = hc.split(ids.sample(frac=1, random_state=3)).reindex(ids.index)
    assert (a == b).all()
    shares = a.value_counts(normalize=True)
    assert shares["train"] == pytest.approx(0.6, abs=0.03)


def test_features_single_request_match_batch(twin):
    app, bureau, _ = twin
    batch = hc.build_features(app, bureau).set_index(hc.ID)
    one_id = int(bureau[hc.ID].iloc[0])
    row = app[app[hc.ID] == one_id].astype(object)
    row = row.where(row.notna(), None)  # JSON-like: None for missing, mixed types
    single = hc.build_features(row, bureau[bureau[hc.ID] == one_id].astype(object)).set_index(hc.ID)
    cols = hc.model_columns(batch.reset_index())
    num = [c for c in cols if c not in hc.CATEGORICAL]
    np.testing.assert_allclose(
        batch.loc[one_id, num].astype(float), single.loc[one_id, num].astype(float), equal_nan=True
    )
    assert "CODE_GENDER" not in cols


def test_unknown_category_becomes_missing(twin):
    feats = hc.build_features(*twin[:2])
    cols = hc.model_columns(feats)
    _, vocab = hc.to_categorical(feats[cols])
    odd = feats[cols].head(3).copy()
    odd["OCCUPATION_TYPE"] = "Astronaut"
    X, _ = hc.to_categorical(odd, vocab)
    assert X["OCCUPATION_TYPE"].isna().all()
    assert list(X["OCCUPATION_TYPE"].cat.categories) == vocab["OCCUPATION_TYPE"]
