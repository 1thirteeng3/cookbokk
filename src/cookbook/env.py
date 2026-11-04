"""Environment helpers: platform detection, seeds, hardware and package versions."""

from __future__ import annotations

import importlib.metadata as md
import importlib.util
import os
import platform as _platform
import random
import shutil
import subprocess
import sys
from collections.abc import Iterable, Mapping


def in_colab() -> bool:
    return "google.colab" in sys.modules or "COLAB_RELEASE_TAG" in os.environ


def platform() -> str:
    """``colab``, ``ci`` or ``local``."""
    if in_colab():
        return "colab"
    if os.environ.get("CI"):
        return "ci"
    return "local"


def set_seeds(seed: int = 42, deterministic_torch: bool = False) -> None:
    """Seed Python, NumPy and (when installed) PyTorch and TensorFlow."""
    os.environ["PYTHONHASHSEED"] = str(seed)
    random.seed(seed)
    try:
        import numpy as np

        np.random.seed(seed)
    except ImportError:
        pass
    if importlib.util.find_spec("torch") is not None:
        import torch

        torch.manual_seed(seed)
        if torch.cuda.is_available():
            torch.cuda.manual_seed_all(seed)
        if deterministic_torch:
            os.environ.setdefault("CUBLAS_WORKSPACE_CONFIG", ":4096:8")
            torch.use_deterministic_algorithms(True)
            torch.backends.cudnn.benchmark = False
    if "tensorflow" in sys.modules:
        sys.modules["tensorflow"].random.set_seed(seed)


def _ram_gb() -> float:
    try:
        return round(os.sysconf("SC_PAGE_SIZE") * os.sysconf("SC_PHYS_PAGES") / 1024**3, 1)
    except (ValueError, OSError, AttributeError):
        return 0.0


def _gpu_name() -> str | None:
    if "torch" in sys.modules:
        torch = sys.modules["torch"]
        if torch.cuda.is_available():
            return torch.cuda.get_device_name(0)
    if shutil.which("nvidia-smi"):
        try:
            out = subprocess.run(
                ["nvidia-smi", "--query-gpu=name", "--format=csv,noheader"],
                capture_output=True,
                text=True,
                timeout=10,
                check=True,
            )
            return out.stdout.strip().splitlines()[0] or None
        except (subprocess.SubprocessError, IndexError):
            return None
    return None


def hardware_info() -> dict:
    """Hardware summary stored with every result (see result.schema.json)."""
    cpu = _platform.processor() or _platform.machine()
    return {
        "platform": platform(),
        "cpu": f"{cpu} x{os.cpu_count()}",
        "gpu": _gpu_name(),
        "ram_gb": _ram_gb(),
    }


def quiet_logs() -> None:
    """Silence noisy third-party loggers (CVXPY solver probing, MLflow info chatter).

    CVXPY configures its logger *during* import and reports every optional solver it fails
    to load (harmless for optbinning's default solver), so it is imported here with stderr
    captured, then limited to errors.

    Order matters: ``ortools`` (used by optbinning) and ``highspy`` (pulled in by CVXPY) ship
    different builds of the HiGHS library; whichever loads first wins. Loading ortools first
    keeps optbinning working and only disables CVXPY's optional HiGHS solver.
    """
    import contextlib
    import io
    import logging
    import warnings

    if importlib.util.find_spec("ortools") is not None:
        import ortools.sat.python.cp_model  # noqa: F401
    if "cvxpy" not in sys.modules and importlib.util.find_spec("cvxpy") is not None:
        with contextlib.redirect_stderr(io.StringIO()):
            import cvxpy  # noqa: F401
        for handler in logging.getLogger("__cvxpy__").handlers:
            if isinstance(handler, logging.StreamHandler):
                handler.setStream(sys.stderr)
    for name in ("__cvxpy__", "cvxpy", "mlflow", "alembic", "optuna"):
        logging.getLogger(name).setLevel(logging.ERROR)
    os.environ.setdefault("MLFLOW_DISABLE_AGENT_HINT", "1")
    warnings.filterwarnings("ignore", category=FutureWarning)
    warnings.filterwarnings("ignore", message=".*X does not have valid feature names.*")


def colab_secrets_to_env(names=("KAGGLE_API_TOKEN", "KAGGLE_USERNAME", "KAGGLE_KEY")) -> list[str]:
    """Copy Colab secrets (🔑 menu) into environment variables. Returns the names found.

    Outside Colab it does nothing, so notebooks can call it unconditionally.
    """
    if not in_colab():
        return []
    from google.colab import userdata  # type: ignore[import-not-found]

    found = []
    for name in names:
        try:
            value = userdata.get(name)
        except Exception:  # noqa: BLE001  (SecretNotFoundError / NotebookAccessError)
            continue
        if value:
            os.environ[name] = value
            found.append(name)
    return found


def require_gpu() -> str:
    """Stop with a clear message when a notebook with ``gpu: required`` has no accelerator."""
    name = _gpu_name()
    if name is None:
        raise RuntimeError(
            "Este notebook precisa de GPU. No Colab: Ambiente de execução > Alterar o tipo "
            "de ambiente de execução > GPU. / This notebook needs a GPU. In Colab: Runtime > "
            "Change runtime type > GPU."
        )
    return name


def versions(packages: Mapping[str, str] | Iterable[str] = ()) -> dict[str, str]:
    """Installed versions for the given packages, plus Python."""
    out = {"python": _platform.python_version()}
    for pkg in packages:
        try:
            out[pkg] = md.version(pkg)
        except md.PackageNotFoundError:
            out[pkg] = "not-installed"
    return out
