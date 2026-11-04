"""Credit-risk building blocks shared by Part N recipes and P1 projects.

Discrimination (Gini, KS), calibration (ECE), stability (PSI/CSI), scorecard scaling (PDO),
cut-off tables, profit-based policy and reason codes. Pure NumPy/pandas, no model dependency.
"""

from __future__ import annotations

from collections.abc import Callable

import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score

# --------------------------------------------------------------------------------------
# Discrimination and calibration
# --------------------------------------------------------------------------------------


def gini(y, score) -> float:
    """Gini = 2·AUC − 1. ``score`` must increase with risk (e.g. PD)."""
    return float(2 * roc_auc_score(y, score) - 1)


def ks(y, score) -> float:
    """Kolmogorov–Smirnov: max distance between score CDFs of bads and goods."""
    y = np.asarray(y)
    s = np.asarray(score, dtype=float)
    order = np.argsort(s)
    y_sorted = y[order]
    cum_bad = np.cumsum(y_sorted) / max(y_sorted.sum(), 1)
    cum_good = np.cumsum(1 - y_sorted) / max((1 - y_sorted).sum(), 1)
    return float(np.max(np.abs(cum_bad - cum_good)))


def ece(y, p, n_bins: int = 10) -> float:
    """Expected calibration error with equal-frequency bins."""
    y = np.asarray(y, dtype=float)
    p = np.asarray(p, dtype=float)
    bins = pd.qcut(p, q=n_bins, labels=False, duplicates="drop")
    frame = pd.DataFrame({"y": y, "p": p, "b": bins})
    g = frame.groupby("b").agg(y=("y", "mean"), p=("p", "mean"), n=("y", "size"))
    return float((g["n"] * (g["y"] - g["p"]).abs()).sum() / len(frame))


def bootstrap(fn: Callable[..., float], *arrays, n: int = 200, seed: int = 0) -> dict:
    """Bootstrap mean/std of ``fn(*arrays)`` (rows resampled together). Result-file format."""
    rng = np.random.default_rng(seed)
    arrays = [np.asarray(a) for a in arrays]
    size = len(arrays[0])
    values = []
    for _ in range(n):
        idx = rng.integers(0, size, size)
        try:
            values.append(fn(*(a[idx] for a in arrays)))
        except ValueError:  # e.g. single class in a resample
            continue
    point = fn(*arrays)
    return {
        "mean": round(float(point), 6),
        "std": round(float(np.std(values, ddof=1)), 6),
        "n": len(values),
    }


# --------------------------------------------------------------------------------------
# Stability
# --------------------------------------------------------------------------------------


def psi(expected, actual, bins: int = 10, eps: float = 1e-4) -> float:
    """Population Stability Index of ``actual`` against ``expected``.

    Numeric: quantile bins from ``expected`` (+ one bin for missing values).
    Categorical (object/category dtype): one bin per category.
    Rule of thumb: < 0.10 stable · 0.10–0.25 attention · > 0.25 significant shift.
    """
    e = pd.Series(expected)
    a = pd.Series(actual)
    if not (pd.api.types.is_numeric_dtype(e) or pd.api.types.is_bool_dtype(e)):
        e_dist = e.astype(str).value_counts(normalize=True)
        a_dist = a.astype(str).value_counts(normalize=True)
    else:
        edges = np.unique(np.nanquantile(e.astype(float), np.linspace(0, 1, bins + 1)))
        edges[0], edges[-1] = -np.inf, np.inf

        def dist(s: pd.Series) -> pd.Series:
            cut = pd.cut(s.astype(float), edges, include_lowest=True).astype(str)
            return cut.where(s.notna(), "missing").value_counts(normalize=True)

        e_dist, a_dist = dist(e), dist(a)
    keys = e_dist.index.union(a_dist.index)
    pe = e_dist.reindex(keys, fill_value=0).to_numpy() + eps
    pa = a_dist.reindex(keys, fill_value=0).to_numpy() + eps
    return float(np.sum((pa - pe) * np.log(pa / pe)))


def psi_label(value: float, lang: str = "pt") -> str:
    labels = {
        "pt": ("estável", "atenção", "mudança relevante"),
        "en": ("stable", "attention", "significant shift"),
    }[lang]
    return labels[0] if value < 0.10 else labels[1] if value < 0.25 else labels[2]


def csi(reference: pd.DataFrame, current: pd.DataFrame, columns=None, bins: int = 10) -> pd.Series:
    """Characteristic Stability Index: PSI per feature, sorted descending."""
    cols = columns or [c for c in reference.columns if c in current.columns]
    return pd.Series({c: psi(reference[c], current[c], bins) for c in cols}).sort_values(
        ascending=False
    )


# --------------------------------------------------------------------------------------
# Scorecard scaling
# --------------------------------------------------------------------------------------


def score_from_pd(pd_, pdo: float = 20.0, base_score: float = 600.0, base_odds: float = 50.0):
    """Scale PD to points: ``base_score`` at good:bad odds ``base_odds``; +``pdo`` doubles odds."""
    p = np.clip(np.asarray(pd_, dtype=float), 1e-9, 1 - 1e-9)
    factor = pdo / np.log(2)
    offset = base_score - factor * np.log(base_odds)
    return offset + factor * np.log((1 - p) / p)


# --------------------------------------------------------------------------------------
# Cut-offs and policy
# --------------------------------------------------------------------------------------


def cutoff_table(y, pd_, approval_rates=(0.5, 0.6, 0.7, 0.8, 0.9, 1.0)) -> pd.DataFrame:
    """For each approval rate (approving the lowest PDs): PD threshold and bad rate."""
    y = np.asarray(y)
    p = np.asarray(pd_, dtype=float)
    order = np.argsort(p)
    rows = []
    for rate in approval_rates:
        k = max(1, int(round(rate * len(p))))
        approved = order[:k]
        rows.append(
            {
                "approval_rate": rate,
                "pd_threshold": float(p[order[k - 1]]),
                "bad_rate_approved": float(y[approved].mean()),
                "bads_avoided_share": float(1 - y[approved].sum() / max(y.sum(), 1)),
            }
        )
    return pd.DataFrame(rows)


def expected_profit(pd_, exposure, margin: float, lgd: float):
    """Expected profit per application if approved: (1 − PD)·margin·EAD − PD·LGD·EAD."""
    p = np.asarray(pd_, dtype=float)
    e = np.asarray(exposure, dtype=float)
    return (1 - p) * margin * e - p * lgd * e


def realized_profit(y, exposure, approved, margin: float, lgd: float) -> float:
    """Profit actually realized by a decision vector, using observed outcomes."""
    y = np.asarray(y)
    e = np.asarray(exposure, dtype=float)
    a = np.asarray(approved, dtype=bool)
    return float(np.sum(np.where(y[a] == 1, -lgd * e[a], margin * e[a])))


def policy_curve(y, pd_, exposure, margin: float, lgd: float, n_points: int = 101) -> pd.DataFrame:
    """Approval rate, bad rate and realized profit as the PD threshold moves."""
    p = np.asarray(pd_, dtype=float)
    thresholds = np.unique(np.quantile(p, np.linspace(0.01, 1.0, n_points)))
    rows = []
    for t in thresholds:
        approved = p <= t
        rows.append(
            {
                "pd_threshold": float(t),
                "approval_rate": float(approved.mean()),
                "bad_rate_approved": float(np.asarray(y)[approved].mean())
                if approved.any()
                else np.nan,
                "profit": realized_profit(y, exposure, approved, margin, lgd),
            }
        )
    return pd.DataFrame(rows)


# --------------------------------------------------------------------------------------
# Explanations
# --------------------------------------------------------------------------------------


def reason_codes(contributions: np.ndarray, feature_names, k: int = 3) -> list[list[str]]:
    """Top-k features pushing each prediction towards higher risk (positive contributions).

    ``contributions``: (n_samples, n_features) array, e.g. LightGBM ``pred_contrib`` without
    the bias column, or WoE × coefficient for a logistic scorecard.
    """
    c = np.asarray(contributions)
    names = np.asarray(feature_names)
    top = np.argsort(-c, axis=1)[:, :k]
    return [[str(names[j]) for j in row if c[i, j] > 0] for i, row in enumerate(top)]


# --------------------------------------------------------------------------------------
# Calibration
# --------------------------------------------------------------------------------------


class ProbabilityCalibrator:
    """Map raw model probabilities to calibrated PDs. Picklable, importable by the API.

    ``method``: ``"identity"``, ``"platt"`` (logistic on the logit) or ``"isotonic"``.
    """

    def __init__(self, method: str = "isotonic"):
        if method not in {"identity", "platt", "isotonic"}:
            raise ValueError(f"unknown method {method!r}")
        self.method = method

    @staticmethod
    def _logit(p):
        p = np.clip(np.asarray(p, dtype=float), 1e-6, 1 - 1e-6)
        return np.log(p / (1 - p)).reshape(-1, 1)

    def fit(self, raw, y) -> ProbabilityCalibrator:
        if self.method == "platt":
            from sklearn.linear_model import LogisticRegression

            self.model_ = LogisticRegression(C=1e6, max_iter=1000).fit(self._logit(raw), y)
        elif self.method == "isotonic":
            from sklearn.isotonic import IsotonicRegression

            self.model_ = IsotonicRegression(out_of_bounds="clip", y_min=1e-4, y_max=1 - 1e-4)
            self.model_.fit(np.asarray(raw, dtype=float), y)
        return self

    def predict(self, raw):
        raw = np.asarray(raw, dtype=float)
        if self.method == "identity":
            return raw
        if self.method == "platt":
            return self.model_.predict_proba(self._logit(raw))[:, 1]
        return self.model_.predict(raw)
