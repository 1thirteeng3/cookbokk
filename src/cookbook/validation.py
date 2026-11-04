"""JSON Schema validators for recipe, project and result documents."""

from __future__ import annotations

import json
from functools import cache
from importlib.resources import files
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource

SCHEMA_NAMES = ("recipe", "project", "result")


@cache
def _schemas() -> dict[str, dict]:
    base = files("cookbook") / "schemas"
    return {
        f"{name}.schema.json": json.loads(
            (base / f"{name}.schema.json").read_text(encoding="utf-8")
        )
        for name in SCHEMA_NAMES
    }


@cache
def validator(name: str) -> Draft202012Validator:
    """Return a validator for ``recipe``, ``project`` or ``result``."""
    schemas = _schemas()
    registry = Registry().with_resources(
        (key, Resource.from_contents(schema)) for key, schema in schemas.items()
    )
    schema = schemas[f"{name}.schema.json"]
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema, registry=registry, format_checker=FormatChecker())


def errors(name: str, document: Any) -> list[str]:
    """Human-readable validation errors (empty list when valid)."""
    out = []
    for err in sorted(validator(name).iter_errors(document), key=lambda e: list(e.path)):
        where = "/".join(str(p) for p in err.path) or "<root>"
        out.append(f"{where}: {err.message}")
    return out
