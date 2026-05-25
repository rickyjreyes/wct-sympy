"""Registry loader for equations/registry.yaml."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Dict

import yaml

REGISTRY_PATH = Path(__file__).resolve().parent.parent / "equations" / "registry.yaml"


def load_registry(path: os.PathLike | str | None = None) -> Dict[str, Any]:
    """Load the YAML equation registry. Returns a dict keyed by check ID."""
    p = Path(path) if path is not None else REGISTRY_PATH
    if not p.exists():
        raise FileNotFoundError(f"Registry not found: {p}")
    with p.open("r", encoding="utf-8") as fh:
        data = yaml.safe_load(fh) or {}
    if not isinstance(data, dict):
        raise ValueError(f"Registry must be a mapping at top level, got {type(data)!r}")
    return data


def get_entry(check_id: str, registry: Dict[str, Any] | None = None) -> Dict[str, Any]:
    reg = registry if registry is not None else load_registry()
    if check_id not in reg:
        raise KeyError(f"Check ID not in registry: {check_id!r}")
    return reg[check_id]
