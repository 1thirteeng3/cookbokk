"""Public dataset registry with cached download, checksum and deterministic sampling.

Add a dataset with :func:`register`. Every recipe loads data through :func:`fetch`, which
returns the DataFrame and a metadata dict that goes straight into the result file.
"""

from __future__ import annotations

import hashlib
import io
import os
import shutil
import tempfile
import urllib.request
import zipfile
from collections.abc import Callable
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np
import pandas as pd

Reader = Callable[[Path], pd.DataFrame]


@dataclass(frozen=True)
class DatasetSpec:
    key: str
    name: str
    license: str
    kind: str  # "http" | "kaggle" | "generated"
    reader: Reader
    url: str | None = None
    filename: str | None = None
    sha256: str | None = None
    kaggle_competition: str | None = None
    kaggle_files: tuple[str, ...] = ()
    target: str | None = None
    notes: str = ""
    generator: Callable[[int], pd.DataFrame] | None = field(default=None, repr=False)


REGISTRY: dict[str, DatasetSpec] = {}


def register(spec: DatasetSpec) -> DatasetSpec:
    if spec.key in REGISTRY:
        raise ValueError(f"dataset '{spec.key}' already registered")
    REGISTRY[spec.key] = spec
    return spec


def sha256_file(path: Path, chunk: int = 1 << 20) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while block := f.read(chunk):
            h.update(block)
    return h.hexdigest()


def _download(url: str, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(url, headers={"User-Agent": "ds-ai-cookbook"})
    with (
        urllib.request.urlopen(req, timeout=120) as resp,
        tempfile.NamedTemporaryFile(delete=False, dir=dest.parent) as tmp,
    ):
        shutil.copyfileobj(resp, tmp)
    os.replace(tmp.name, dest)


def _download_kaggle(spec: DatasetSpec, folder: Path) -> None:
    """Download competition files with the official ``kaggle`` client (>= 2.2).

    Credentials: ``KAGGLE_API_TOKEN`` or ``KAGGLE_USERNAME``/``KAGGLE_KEY`` (on Colab, call
    :func:`cookbook.env.colab_secrets_to_env` first). You must accept the competition rules
    on kaggle.com once with the same account.
    """
    try:
        from kaggle.api.kaggle_api_extended import KaggleApi
    except ImportError as exc:  # pragma: no cover - depends on optional extra
        raise RuntimeError(
            "Instale o extra 'kaggle' e configure KAGGLE_API_TOKEN (ou KAGGLE_USERNAME e "
            "KAGGLE_KEY). / Install the 'kaggle' extra and set Kaggle credentials."
        ) from exc
    api = KaggleApi()
    api.authenticate()
    folder.mkdir(parents=True, exist_ok=True)
    for name in spec.kaggle_files:
        if (folder / name).exists():
            continue
        api.competition_download_file(
            spec.kaggle_competition, name, path=str(folder), quiet=True, unzip=True
        )
        zipped = folder / f"{name}.zip"
        if zipped.exists():  # older clients do not unzip
            with zipfile.ZipFile(zipped) as zf:
                zf.extractall(folder)
            zipped.unlink()


def download(key: str, data_dir: str | Path = "data") -> Path:
    """Make sure every file of a downloadable dataset is cached; return its folder."""
    spec = REGISTRY[key]
    folder = Path(data_dir) / key
    if spec.kind == "http":
        path = folder / spec.filename  # type: ignore[operator]
        if not path.exists():
            _download(spec.url, path)  # type: ignore[arg-type]
    elif spec.kind == "kaggle":
        if not all((folder / f).exists() for f in spec.kaggle_files):
            _download_kaggle(spec, folder)
    return folder


def fetch(
    key: str, data_dir: str | Path = "data", verify: bool = True
) -> tuple[pd.DataFrame, dict]:
    """Load a registered dataset, downloading it once into ``data_dir/<key>/``.

    Returns ``(df, meta)`` where ``meta`` has ``name``, ``sha256`` and ``n_rows``.
    """
    if key not in REGISTRY:
        raise KeyError(f"unknown dataset '{key}'. Registered: {sorted(REGISTRY)}")
    spec = REGISTRY[key]
    digest: str | None = None

    if spec.kind == "generated":
        df = spec.generator(42)  # type: ignore[misc]
        path = None
    elif spec.kind == "http":
        path = download(key, data_dir) / spec.filename  # type: ignore[operator]
        digest = sha256_file(path)
        if verify and spec.sha256 and digest != spec.sha256:
            raise ValueError(f"checksum mismatch for {key}: {digest} != {spec.sha256}")
        df = spec.reader(path)
    elif spec.kind == "kaggle":
        path = download(key, data_dir) / spec.kaggle_files[0]
        digest = sha256_file(path)
        df = spec.reader(path)
    else:
        raise ValueError(f"unknown kind '{spec.kind}'")

    meta = {"name": spec.name, "sha256": digest, "n_rows": int(len(df))}
    return df, meta


def sample(
    df: pd.DataFrame, frac: float, seed: int = 42, stratify: str | None = None
) -> pd.DataFrame:
    """Deterministic subsample, stratified by ``stratify`` when given."""
    if not 0 < frac <= 1:
        raise ValueError("frac must be in (0, 1]")
    if frac == 1:
        return df
    if stratify is None:
        return df.sample(frac=frac, random_state=seed)
    return df.groupby(stratify, group_keys=False).sample(frac=frac, random_state=seed)


# --------------------------------------------------------------------------------------
# Built-in datasets
# --------------------------------------------------------------------------------------


def _synthetic_credit(seed: int, n: int = 20_000) -> pd.DataFrame:
    """Offline credit-like dataset for tests, CI and smoke runs. Not for conclusions."""
    rng = np.random.default_rng(seed)
    age = rng.integers(18, 75, n)
    income = np.round(rng.lognormal(8.0, 0.6, n), 2)
    utilization = np.clip(rng.beta(2, 5, n), 0, 1)
    tenure_months = rng.integers(0, 240, n)
    late_payments = rng.poisson(0.4 + 1.5 * utilization, n)
    region = rng.choice(["N", "NE", "CO", "SE", "S"], n, p=[0.08, 0.27, 0.08, 0.42, 0.15])
    logit = (
        -2.2
        + 2.4 * utilization
        + 0.55 * late_payments
        - 0.018 * (age - 18)
        - 0.25 * np.log(income / 3000)
        - 0.004 * tenure_months
    )
    default = rng.binomial(1, 1 / (1 + np.exp(-logit)))
    income[rng.random(n) < 0.05] = np.nan
    return pd.DataFrame(
        {
            "age": age,
            "income": income,
            "utilization": utilization,
            "tenure_months": tenure_months,
            "late_payments": late_payments,
            "region": region,
            "default": default,
        }
    )


def _read_uci_credit(path: Path) -> pd.DataFrame:
    with zipfile.ZipFile(path) as zf:
        name = next(n for n in zf.namelist() if n.endswith((".xls", ".xlsx")))
        raw = zf.read(name)
    df = pd.read_excel(io.BytesIO(raw), header=1)
    return df.rename(columns={"default payment next month": "default"})


register(
    DatasetSpec(
        key="synthetic-credit",
        name="Synthetic credit (cookbook, offline)",
        license="CC0 (generated)",
        kind="generated",
        reader=lambda p: pd.DataFrame(),
        generator=_synthetic_credit,
        target="default",
        notes="Gerado localmente; usar só para testes, CI e smoke.",
    )
)

register(
    DatasetSpec(
        key="uci-credit-default",
        name="Default of Credit Card Clients (UCI)",
        license="CC BY 4.0",
        kind="http",
        url="https://archive.ics.uci.edu/static/public/350/default+of+credit+card+clients.zip",
        filename="default-of-credit-card-clients.zip",
        reader=_read_uci_credit,
        target="default",
        notes="Requer o extra 'excel' (xlrd). Preencher sha256 após o primeiro download verificado.",
    )
)

# Home Credit (real + synthetic twin) is registered by cookbook.home_credit.


from cookbook import home_credit as _home_credit  # noqa: E402,F401  (registers datasets)
