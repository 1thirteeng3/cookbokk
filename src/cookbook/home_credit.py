"""Home Credit Default Risk: loader, cleaning, deterministic split and an offline synthetic twin.

Real data (Kaggle, competition rules): ``application_train.csv`` (one row per application,
target ``TARGET`` = 1 for payment difficulties) and ``bureau.csv`` (previous credits reported
by other institutions). We load a curated subset of columns to keep memory low on Colab.

The **synthetic twin** has the same columns, realistic marginal distributions, missingness
patterns, the ``DAYS_EMPLOYED = 365243`` anomaly and a ~8% default rate driven by a latent
risk factor. It exists so notebooks run offline (CI, tests, smoke). **Never draw conclusions
from it**: results in the docs come only from ``run_mode='full'`` on the real data.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from cookbook.data import REGISTRY, DatasetSpec, download, register, sha256_file

TARGET = "TARGET"
ID = "SK_ID_CURR"
DAYS_EMPLOYED_ANOMALY = 365243

APPLICATION_COLUMNS = [
    "SK_ID_CURR",
    "TARGET",
    "NAME_CONTRACT_TYPE",
    "CODE_GENDER",
    "FLAG_OWN_CAR",
    "FLAG_OWN_REALTY",
    "CNT_CHILDREN",
    "AMT_INCOME_TOTAL",
    "AMT_CREDIT",
    "AMT_ANNUITY",
    "AMT_GOODS_PRICE",
    "NAME_INCOME_TYPE",
    "NAME_EDUCATION_TYPE",
    "NAME_FAMILY_STATUS",
    "NAME_HOUSING_TYPE",
    "REGION_POPULATION_RELATIVE",
    "DAYS_BIRTH",
    "DAYS_EMPLOYED",
    "DAYS_REGISTRATION",
    "DAYS_ID_PUBLISH",
    "OWN_CAR_AGE",
    "OCCUPATION_TYPE",
    "CNT_FAM_MEMBERS",
    "REGION_RATING_CLIENT",
    "ORGANIZATION_TYPE",
    "EXT_SOURCE_1",
    "EXT_SOURCE_2",
    "EXT_SOURCE_3",
    "DAYS_LAST_PHONE_CHANGE",
    "AMT_REQ_CREDIT_BUREAU_YEAR",
    "FLAG_DOCUMENT_3",
    "DEF_30_CNT_SOCIAL_CIRCLE",
    "FLAG_WORK_PHONE",
    "FLAG_PHONE",
    "FLAG_EMAIL",
    "HOUR_APPR_PROCESS_START",
    "WEEKDAY_APPR_PROCESS_START",
    "REG_CITY_NOT_WORK_CITY",
    "LIVE_CITY_NOT_WORK_CITY",
    "TOTALAREA_MODE",
    "YEARS_BEGINEXPLUATATION_AVG",
    "FLOORSMAX_AVG",
    "APARTMENTS_AVG",
]
REQUIRED = [
    "SK_ID_CURR",
    "TARGET",
    "AMT_INCOME_TOTAL",
    "AMT_CREDIT",
    "AMT_ANNUITY",
    "DAYS_BIRTH",
    "DAYS_EMPLOYED",
    "EXT_SOURCE_2",
]
BUREAU_COLUMNS = [
    "SK_ID_CURR",
    "CREDIT_ACTIVE",
    "DAYS_CREDIT",
    "CREDIT_DAY_OVERDUE",
    "AMT_CREDIT_SUM",
    "AMT_CREDIT_SUM_DEBT",
    "AMT_CREDIT_SUM_OVERDUE",
    "AMT_CREDIT_MAX_OVERDUE",
    "CREDIT_TYPE",
]


# --------------------------------------------------------------------------------------
# Loading
# --------------------------------------------------------------------------------------


def _read_application(path) -> pd.DataFrame:
    wanted = set(APPLICATION_COLUMNS)
    df = pd.read_csv(path, usecols=lambda c: c in wanted)
    missing = [c for c in REQUIRED if c not in df.columns]
    if missing:
        raise ValueError(f"application file lacks required columns: {missing}")
    return df


def load(source: str = "home-credit", data_dir="data", n_synthetic: int = 30_000, seed: int = 42):
    """Return ``(application, bureau, meta)``.

    ``source``: ``"home-credit"`` (Kaggle download, cached in ``data_dir``) or
    ``"home-credit-synthetic"`` (generated offline).
    """
    if source == "home-credit-synthetic":
        app, bureau = synthetic_twin(n_synthetic, seed)
        meta = {"name": REGISTRY[source].name, "sha256": None, "n_rows": len(app)}
        return app, bureau, meta
    if source != "home-credit":
        raise ValueError(f"unknown source {source!r}")
    folder = download(source, data_dir)
    app = _read_application(folder / "application_train.csv")
    wanted = set(BUREAU_COLUMNS)
    bureau = pd.read_csv(folder / "bureau.csv", usecols=lambda c: c in wanted)
    meta = {
        "name": REGISTRY[source].name,
        "sha256": sha256_file(folder / "application_train.csv"),
        "n_rows": len(app),
    }
    return app, bureau, meta


def clean(app: pd.DataFrame) -> pd.DataFrame:
    """Minimal, documented cleaning shared by every tier.

    - ``DAYS_EMPLOYED == 365243`` is a placeholder (mostly pensioners): set to NaN and keep a
      flag, because the placeholder itself carries information.
    - ``CODE_GENDER == "XNA"`` (a handful of rows) becomes missing.
    """
    out = app.copy()
    anomaly = out["DAYS_EMPLOYED"] == DAYS_EMPLOYED_ANOMALY
    out["DAYS_EMPLOYED_ANOM"] = anomaly.astype(int)
    out.loc[anomaly, "DAYS_EMPLOYED"] = np.nan
    if "CODE_GENDER" in out:
        out["CODE_GENDER"] = out["CODE_GENDER"].replace("XNA", np.nan)
    return out


def split(ids: pd.Series, seed: int = 0, valid: float = 0.2, test: float = 0.2) -> pd.Series:
    """Deterministic train/valid/test assignment from a hash of the ID.

    Hash-based splits survive re-downloads, row reordering and new rows: the same applicant
    always lands in the same partition. Home Credit has no application date, so there is no
    out-of-time split; see the project doc for the consequences.
    """
    h = pd.util.hash_pandas_object(
        pd.Series(ids).astype("int64"),
        index=False,
        hash_key=f"cookbook-{seed:010d}"[:16].ljust(16, "0"),
    )
    bucket = (h.to_numpy() % 10_000) / 10_000
    labels = np.where(bucket < test, "test", np.where(bucket < test + valid, "valid", "train"))
    return pd.Series(labels, index=pd.Series(ids).index, name="split")


# --------------------------------------------------------------------------------------
# Feature engineering (shared by training notebooks and the scoring API)
# --------------------------------------------------------------------------------------

CATEGORICAL = [
    "NAME_CONTRACT_TYPE",
    "FLAG_OWN_CAR",
    "FLAG_OWN_REALTY",
    "NAME_INCOME_TYPE",
    "NAME_EDUCATION_TYPE",
    "NAME_FAMILY_STATUS",
    "NAME_HOUSING_TYPE",
    "OCCUPATION_TYPE",
    "ORGANIZATION_TYPE",
    "WEEKDAY_APPR_PROCESS_START",
]
# Kept out of the model on purpose: protected attribute, used only for fairness checks.
PROTECTED = ["CODE_GENDER"]


def _ratio(a, b):
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    with np.errstate(divide="ignore", invalid="ignore"):
        out = a / b
    return np.where(np.isfinite(out), out, np.nan)


def engineer(app: pd.DataFrame) -> pd.DataFrame:
    """Application-level features. Input: cleaned application rows (see :func:`clean`)."""
    out = app.copy()
    out["AGE_YEARS"] = -out["DAYS_BIRTH"] / 365.25
    out["EMPLOYED_YEARS"] = -out["DAYS_EMPLOYED"] / 365.25
    out["EMPLOYED_TO_AGE"] = _ratio(out["EMPLOYED_YEARS"], out["AGE_YEARS"])
    out["CREDIT_INCOME"] = _ratio(out["AMT_CREDIT"], out["AMT_INCOME_TOTAL"])
    out["ANNUITY_INCOME"] = _ratio(out["AMT_ANNUITY"], out["AMT_INCOME_TOTAL"])
    out["CREDIT_TERM"] = _ratio(out["AMT_CREDIT"], out["AMT_ANNUITY"])
    out["GOODS_CREDIT"] = _ratio(out["AMT_GOODS_PRICE"], out["AMT_CREDIT"])
    out["INCOME_PER_PERSON"] = _ratio(out["AMT_INCOME_TOTAL"], out["CNT_FAM_MEMBERS"])
    ext = out[["EXT_SOURCE_1", "EXT_SOURCE_2", "EXT_SOURCE_3"]]
    out["EXT_SOURCE_MEAN"] = ext.mean(axis=1)
    out["EXT_SOURCE_MIN"] = ext.min(axis=1)
    out["EXT_SOURCE_PROD"] = ext.prod(axis=1, min_count=3)
    out["EXT_SOURCE_NULLS"] = ext.isna().sum(axis=1)
    return out


def aggregate_bureau(bureau: pd.DataFrame) -> pd.DataFrame:
    """One row per applicant from previous credits reported to the bureau (uses Polars).

    Every column is an aggregate over credits that existed *before* the application
    (``DAYS_CREDIT`` <= 0), so there is no look-ahead.
    """
    import polars as pl

    b = pl.from_pandas(bureau).filter(pl.col("DAYS_CREDIT") <= 0)
    active = pl.col("CREDIT_ACTIVE") == "Active"
    agg = (
        b.group_by("SK_ID_CURR")
        .agg(
            pl.len().alias("BUREAU_COUNT"),
            active.sum().alias("BUREAU_ACTIVE_COUNT"),
            active.mean().alias("BUREAU_ACTIVE_SHARE"),
            (pl.col("CREDIT_ACTIVE") == "Bad debt").sum().alias("BUREAU_BAD_DEBT_COUNT"),
            (pl.col("CREDIT_TYPE") == "Microloan").sum().alias("BUREAU_MICROLOAN_COUNT"),
            pl.col("AMT_CREDIT_SUM").sum().alias("BUREAU_CREDIT_SUM"),
            pl.col("AMT_CREDIT_SUM_DEBT").sum().alias("BUREAU_DEBT_SUM"),
            pl.col("AMT_CREDIT_SUM_OVERDUE").sum().alias("BUREAU_OVERDUE_SUM"),
            pl.col("CREDIT_DAY_OVERDUE").max().alias("BUREAU_MAX_DAYS_OVERDUE"),
            (pl.col("CREDIT_DAY_OVERDUE") > 0).sum().alias("BUREAU_OVERDUE_COUNT"),
            pl.col("AMT_CREDIT_MAX_OVERDUE").max().alias("BUREAU_MAX_OVERDUE_AMT"),
            pl.col("DAYS_CREDIT").max().alias("BUREAU_DAYS_LAST_CREDIT"),
            pl.col("DAYS_CREDIT").min().alias("BUREAU_DAYS_FIRST_CREDIT"),
        )
        .with_columns(
            (pl.col("BUREAU_DEBT_SUM") / pl.col("BUREAU_CREDIT_SUM")).alias(
                "BUREAU_DEBT_CREDIT_RATIO"
            ),
        )
    )
    out = agg.to_pandas()
    ratio = out["BUREAU_DEBT_CREDIT_RATIO"].astype(float)
    out["BUREAU_DEBT_CREDIT_RATIO"] = ratio.where(np.isfinite(ratio))
    return out


def coerce_types(app: pd.DataFrame, bureau: pd.DataFrame | None = None):
    """Give every known column its training dtype (numbers as float, labels as object).

    Training data comes typed from CSV; API requests come from JSON with ``None`` and mixed
    types. Running both through this function is part of keeping training and serving equal.
    """
    text = set(CATEGORICAL) | set(PROTECTED)
    a = app.copy()
    for c in a.columns:
        if c in text:
            a[c] = a[c].astype("object").where(a[c].notna(), None)
        elif c in APPLICATION_COLUMNS:
            a[c] = pd.to_numeric(a[c], errors="coerce")
    if bureau is None:
        return a
    b = bureau.copy()
    for c in BUREAU_COLUMNS:
        if c not in b:
            b[c] = None
        if c in {"CREDIT_ACTIVE", "CREDIT_TYPE"}:
            b[c] = b[c].astype("object")
        else:
            b[c] = pd.to_numeric(b[c], errors="coerce")
    return a, b[BUREAU_COLUMNS]


def build_features(app: pd.DataFrame, bureau: pd.DataFrame) -> pd.DataFrame:
    """Full feature table: types → clean → engineer → bureau aggregates (no bureau = 0 credits)."""
    app, bureau = coerce_types(app, bureau)
    feats = engineer(clean(app)).merge(aggregate_bureau(bureau), on=ID, how="left")
    counts = [c for c in feats.columns if c.startswith("BUREAU_") and c.endswith("_COUNT")]
    feats[counts] = feats[counts].fillna(0)
    feats["BUREAU_HAS_HISTORY"] = (feats["BUREAU_COUNT"] > 0).astype(int)
    return feats


def model_columns(feats: pd.DataFrame) -> list[str]:
    """Columns that may enter a model: everything except ID, target and protected attributes."""
    excluded = {ID, TARGET, *PROTECTED}
    return [c for c in feats.columns if c not in excluded]


def to_categorical(df: pd.DataFrame, categories: dict[str, list] | None = None):
    """Cast categorical columns with a fixed vocabulary (learned on train when ``None``).

    Unseen categories at scoring time become missing instead of shifting codes, which is
    what keeps training and serving consistent for LightGBM's native categorical support.
    """
    out = df.copy()
    learned = categories or {
        c: sorted(out[c].dropna().astype(str).unique().tolist()) for c in CATEGORICAL if c in out
    }
    for c, cats in learned.items():
        if c in out:
            values = out[c].astype("object")
            known = values.isin(cats)  # unknown (and missing) -> None before building the dtype
            out[c] = pd.Categorical(values.where(known, None), categories=cats)
    return out, learned


# --------------------------------------------------------------------------------------
# Synthetic twin
# --------------------------------------------------------------------------------------


def _choice(rng, options: dict, n: int, shift=None):
    """Categorical draw; ``shift`` (n×k logits added) lets risk tilt the probabilities."""
    names = np.array(list(options))
    logp = np.log(np.array(list(options.values()), dtype=float))
    logits = np.tile(logp, (n, 1)) + (0 if shift is None else shift)
    g = rng.gumbel(size=logits.shape)
    return names[np.argmax(logits + g, axis=1)]


def _sigmoid(x):
    return 1 / (1 + np.exp(-x))


def synthetic_twin(n: int = 30_000, seed: int = 42, default_rate: float = 0.0807):
    """Generate ``(application, bureau)`` shaped like Home Credit. Offline use only."""
    rng = np.random.default_rng(seed)
    r = rng.normal(size=n)  # latent risk: higher = riskier

    income_type = _choice(
        rng,
        {"Working": 0.52, "Commercial associate": 0.23, "Pensioner": 0.18, "State servant": 0.07},
        n,
    )
    pensioner = income_type == "Pensioner"
    age = np.where(pensioner, rng.uniform(55, 69, n), rng.uniform(21, 64, n))
    age = np.clip(age - 2.5 * r * ~pensioner, 21, 69)

    income = np.exp(rng.normal(np.log(150_000), 0.5, n) - 0.08 * r)
    credit = np.clip(
        income * np.exp(rng.normal(np.log(3.5), 0.55, n) + 0.12 * r), 45_000, 4_050_000
    )
    annuity = credit * np.clip(rng.normal(0.05, 0.012, n) + 0.004 * r, 0.02, 0.12)
    goods = credit * rng.uniform(0.82, 1.0, n)

    edu_shift = np.zeros((n, 5))
    edu_shift[:, 0] = 0.6 * r  # Secondary more likely when risky
    edu_shift[:, 1] = -0.6 * r  # Higher less likely
    education = _choice(
        rng,
        {
            "Secondary / secondary special": 0.71,
            "Higher education": 0.243,
            "Incomplete higher": 0.033,
            "Lower secondary": 0.0124,
            "Academic degree": 0.0006,
        },
        n,
        edu_shift,
    )

    years_employed = np.where(
        pensioner, np.nan, np.clip(rng.gamma(1.6, 4.0, n) * np.exp(-0.25 * r), 0.05, 45)
    )
    days_employed = np.where(pensioner, DAYS_EMPLOYED_ANOMALY, -np.round(years_employed * 365.25))

    def ext(loc, scale, miss):
        v = _sigmoid(loc - 0.75 * r + rng.normal(0, scale, n))
        return np.where(rng.random(n) < miss, np.nan, np.round(v, 6))

    has_car = rng.random(n) < 0.34
    children = rng.poisson(0.42, n)
    family = _choice(
        rng,
        {
            "Married": 0.64,
            "Single / not married": 0.15,
            "Civil marriage": 0.10,
            "Separated": 0.064,
            "Widow": 0.046,
        },
        n,
    )
    occupation = _choice(
        rng,
        {
            "Laborers": 0.26,
            "Sales staff": 0.15,
            "Core staff": 0.13,
            "Managers": 0.10,
            "Drivers": 0.09,
            "High skill tech staff": 0.05,
            "Accountants": 0.05,
            "Medicine staff": 0.04,
            "Security staff": 0.03,
            "Cooking staff": 0.03,
            "Cleaning staff": 0.02,
            "Low-skill Laborers": 0.01,
        },
        n,
        np.c_[0.3 * r, np.zeros((n, 10)), 0.6 * r],
    )
    occupation = np.where(pensioner | (rng.random(n) < 0.16), None, occupation)
    organization = np.where(
        pensioner,
        "XNA",
        _choice(
            rng,
            {
                "Business Entity Type 3": 0.27,
                "Self-employed": 0.15,
                "Other": 0.065,
                "Medicine": 0.045,
                "Government": 0.04,
                "Business Entity Type 2": 0.04,
                "School": 0.035,
                "Trade: type 7": 0.03,
                "Kindergarten": 0.03,
                "Construction": 0.026,
                "Transport: type 4": 0.02,
            },
            n,
            np.c_[np.zeros((n, 1)), 0.4 * r, np.zeros((n, 9))],
        ),
    )
    housing_stats_missing = rng.random(n) < 0.5

    app = pd.DataFrame(
        {
            "SK_ID_CURR": np.arange(100_002, 100_002 + n),
            "NAME_CONTRACT_TYPE": _choice(rng, {"Cash loans": 0.905, "Revolving loans": 0.095}, n),
            "CODE_GENDER": _choice(rng, {"F": 0.658, "M": 0.342}, n, np.c_[np.zeros(n), 0.25 * r]),
            "FLAG_OWN_CAR": np.where(has_car, "Y", "N"),
            "FLAG_OWN_REALTY": np.where(rng.random(n) < 0.69, "Y", "N"),
            "CNT_CHILDREN": children,
            "AMT_INCOME_TOTAL": np.round(income, -2),
            "AMT_CREDIT": np.round(credit, 1),
            "AMT_ANNUITY": np.where(rng.random(n) < 0.0001, np.nan, np.round(annuity, 1)),
            "AMT_GOODS_PRICE": np.where(rng.random(n) < 0.001, np.nan, np.round(goods, -3)),
            "NAME_INCOME_TYPE": income_type,
            "NAME_EDUCATION_TYPE": education,
            "NAME_FAMILY_STATUS": family,
            "NAME_HOUSING_TYPE": _choice(
                rng,
                {
                    "House / apartment": 0.887,
                    "With parents": 0.048,
                    "Municipal apartment": 0.036,
                    "Rented apartment": 0.016,
                    "Office apartment": 0.009,
                    "Co-op apartment": 0.004,
                },
                n,
                np.c_[np.zeros(n), 0.5 * r, np.zeros((n, 2)) + 0.0, np.zeros((n, 2))],
            ),
            "REGION_POPULATION_RELATIVE": rng.choice(
                [0.0016, 0.0046, 0.0072, 0.0101, 0.0188, 0.0287, 0.0358, 0.0725], n
            ),
            "DAYS_BIRTH": -np.round(age * 365.25).astype(int),
            "DAYS_EMPLOYED": days_employed,
            "DAYS_REGISTRATION": -np.round(rng.uniform(0, 20_000, n)),
            "DAYS_ID_PUBLISH": -np.round(rng.uniform(0, 6_000, n) * np.exp(-0.1 * r)).astype(int),
            "OWN_CAR_AGE": np.where(has_car, np.round(rng.gamma(2.0, 6.0, n)), np.nan),
            "OCCUPATION_TYPE": occupation,
            "CNT_FAM_MEMBERS": children
            + np.where(np.isin(family, ["Married", "Civil marriage"]), 2, 1),
            "REGION_RATING_CLIENT": _choice(
                rng, {"1": 0.105, "2": 0.738, "3": 0.157}, n, np.c_[-0.4 * r, np.zeros(n), 0.4 * r]
            ).astype(int),
            "ORGANIZATION_TYPE": organization,
            "EXT_SOURCE_1": ext(0.0, 0.9, 0.56),
            "EXT_SOURCE_2": ext(0.6, 0.8, 0.002),
            "EXT_SOURCE_3": ext(0.1, 0.9, 0.198),
            "DAYS_LAST_PHONE_CHANGE": -np.round(rng.exponential(980, n) * np.exp(-0.15 * r)),
            "AMT_REQ_CREDIT_BUREAU_YEAR": np.where(
                rng.random(n) < 0.135, np.nan, rng.poisson(1.9, n)
            ),
            "FLAG_DOCUMENT_3": (rng.random(n) < 0.71).astype(int),
            "DEF_30_CNT_SOCIAL_CIRCLE": rng.poisson(0.14 * np.exp(0.35 * r)),
            "FLAG_WORK_PHONE": (rng.random(n) < 0.2).astype(int),
            "FLAG_PHONE": (rng.random(n) < 0.28).astype(int),
            "FLAG_EMAIL": (rng.random(n) < 0.057).astype(int),
            "HOUR_APPR_PROCESS_START": np.clip(np.round(rng.normal(12, 3.3, n)), 0, 23).astype(int),
            "WEEKDAY_APPR_PROCESS_START": _choice(
                rng,
                {
                    "TUESDAY": 0.175,
                    "WEDNESDAY": 0.169,
                    "MONDAY": 0.165,
                    "THURSDAY": 0.164,
                    "FRIDAY": 0.164,
                    "SATURDAY": 0.11,
                    "SUNDAY": 0.053,
                },
                n,
            ),
            "REG_CITY_NOT_WORK_CITY": (rng.random(n) < _sigmoid(-1.25 + 0.3 * r)).astype(int),
            "LIVE_CITY_NOT_WORK_CITY": (rng.random(n) < 0.18).astype(int),
            "TOTALAREA_MODE": np.where(
                housing_stats_missing, np.nan, np.round(rng.beta(1.6, 14, n), 4)
            ),
            "YEARS_BEGINEXPLUATATION_AVG": np.where(
                housing_stats_missing,
                np.nan,
                np.round(np.clip(rng.normal(0.977, 0.06, n), 0, 1), 4),
            ),
            "FLOORSMAX_AVG": np.where(
                housing_stats_missing, np.nan, np.round(rng.beta(2.2, 7, n), 4)
            ),
            "APARTMENTS_AVG": np.where(
                housing_stats_missing, np.nan, np.round(rng.beta(1.5, 11, n), 4)
            ),
        }
    )
    app.loc[rng.choice(n, size=min(2, n), replace=False), "CODE_GENDER"] = "XNA"

    # Default: latent risk + a few explicit drivers; intercept tuned to hit the target rate.
    ratio = np.log(credit / income)
    logit_wo_b = 1.15 * r + 0.25 * (ratio - ratio.mean()) + 0.2 * (education == "Lower secondary")
    lo, hi = -10.0, 5.0
    for _ in range(60):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if _sigmoid(logit_wo_b + mid).mean() < default_rate else (lo, mid)
    app.insert(1, TARGET, rng.binomial(1, _sigmoid(logit_wo_b + lo)))

    # Bureau: previous credits; riskier clients have more active, overdue, micro credits.
    counts = np.where(rng.random(n) < 0.14, 0, rng.poisson(np.clip(4.8 + 0.6 * r, 0.5, None)))
    owner = np.repeat(np.arange(n), counts)
    rb = r[owner]
    m = len(owner)
    active = rng.random(m) < _sigmoid(-0.55 + 0.45 * rb)
    status = np.where(active, "Active", "Closed")
    status = np.where((~active) & (rng.random(m) < 0.004 * np.exp(rb)), "Sold", status)
    status = np.where(rng.random(m) < 0.0001 * np.exp(1.5 * rb), "Bad debt", status)
    amount = np.round(np.exp(rng.normal(np.log(200_000), 1.1, m)), -2)
    overdue_days = np.where(rng.random(m) < 0.025 * np.exp(0.9 * rb), rng.integers(1, 120, m), 0)
    bureau = pd.DataFrame(
        {
            "SK_ID_CURR": app["SK_ID_CURR"].to_numpy()[owner],
            "CREDIT_ACTIVE": status,
            "DAYS_CREDIT": -rng.integers(0, 2_922, m),
            "CREDIT_DAY_OVERDUE": overdue_days,
            "AMT_CREDIT_SUM": amount,
            "AMT_CREDIT_SUM_DEBT": np.where(
                active, np.round(amount * rng.uniform(0.05, 0.95, m), -2), 0.0
            ),
            "AMT_CREDIT_SUM_OVERDUE": np.where(
                overdue_days > 0, np.round(amount * rng.uniform(0, 0.1, m), -1), 0.0
            ),
            "AMT_CREDIT_MAX_OVERDUE": np.where(
                rng.random(m) < 0.65,
                np.nan,
                np.round(rng.exponential(3_000, m) * np.exp(0.6 * rb), -1),
            ),
            "CREDIT_TYPE": _choice(
                rng,
                {
                    "Consumer credit": 0.73,
                    "Credit card": 0.234,
                    "Car loan": 0.016,
                    "Mortgage": 0.011,
                    "Microloan": 0.007,
                    "Loan for business development": 0.002,
                },
                m,
                np.c_[np.zeros((m, 4)), 1.2 * rb, np.zeros(m)],
            ),
        }
    )
    return app, bureau


register(
    DatasetSpec(
        key="home-credit",
        name="Home Credit Default Risk (Kaggle)",
        license="Kaggle competition rules",
        kind="kaggle",
        kaggle_competition="home-credit-default-risk",
        kaggle_files=("application_train.csv", "bureau.csv"),
        reader=_read_application,
        target=TARGET,
        notes="Aceite as regras da competição no Kaggle com a mesma conta das credenciais.",
    )
)

register(
    DatasetSpec(
        key="home-credit-synthetic",
        name="Home Credit synthetic twin (cookbook, offline)",
        license="CC0 (generated)",
        kind="generated",
        reader=lambda p: pd.DataFrame(),
        generator=lambda seed: synthetic_twin(30_000, seed)[0],
        target=TARGET,
        notes="Mesmas colunas da base real; só para testes, CI e smoke. Nunca para conclusões.",
    )
)
