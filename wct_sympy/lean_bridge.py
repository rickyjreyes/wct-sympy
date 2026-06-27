"""Validate metadata linking wct-sympy checks to wct-lean declarations.

This module never invokes Lean. It verifies IDs, relationship labels, and proof
status metadata so a SymPy PASS cannot be mistaken for a formal proof.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

from .catalog import load_full_registry

ROOT = Path(__file__).resolve().parent.parent
LEAN_MAP_PATH = ROOT / "interoperability" / "lean_map.yaml"
LEGACY_REGISTRY_PATH = ROOT / "equations" / "registry.yaml"

_ALLOWED_REGISTRIES = {"legacy", "full"}
_ALLOWED_RELATIONSHIPS = {
    "formalizes_same_claim",
    "dimensional_support",
    "domain_safety_only",
    "supporting_lemma_only",
    "adjacent_todo_only",
}
_ALLOWED_STATUSES = {"proved", "stated_todo"}


@dataclass(frozen=True)
class LeanMapping:
    sympy_id: str
    registry: str
    sympy_claim: str
    relationship: str
    lean_status: str
    lean_source: str
    lean_declarations: tuple[str, ...]
    caveat: str = ""


def _load_yaml(path: Path) -> dict[str, Any]:
    raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(raw, dict):
        raise ValueError("Lean map must be a YAML mapping")
    return raw


def _legacy_registry_ids() -> set[str]:
    raw = yaml.safe_load(LEGACY_REGISTRY_PATH.read_text(encoding="utf-8")) or {}
    if not isinstance(raw, dict):
        raise ValueError("legacy equation registry must be a YAML mapping")
    return {str(key) for key in raw}


def load_lean_map(path: str | Path | None = None) -> tuple[dict[str, Any], list[LeanMapping]]:
    target = Path(path) if path else LEAN_MAP_PATH
    raw = _load_yaml(target)
    items = raw.get("mappings", [])
    if not isinstance(items, list):
        raise ValueError("lean_map.yaml: mappings must be a list")

    mappings = [
        LeanMapping(
            sympy_id=str(item["sympy_id"]),
            registry=str(item["registry"]),
            sympy_claim=str(item["sympy_claim"]),
            relationship=str(item["relationship"]),
            lean_status=str(item["lean_status"]),
            lean_source=str(item["lean_source"]),
            lean_declarations=tuple(str(name) for name in item.get("lean_declarations", [])),
            caveat=str(item.get("caveat", "")),
        )
        for item in items
    ]
    validate_lean_map(raw, mappings)
    return raw, mappings


def validate_lean_map(metadata: dict[str, Any], mappings: list[LeanMapping]) -> None:
    if metadata.get("lean_repository") != "rickyjreyes/wct-lean":
        raise ValueError("lean_repository must be rickyjreyes/wct-lean")

    identities = [(item.registry, item.sympy_id) for item in mappings]
    duplicates = sorted({identity for identity in identities if identities.count(identity) > 1})
    if duplicates:
        raise ValueError(f"duplicate Lean mappings: {duplicates}")

    full_ids = {spec.equation_id for spec in load_full_registry()}
    legacy_ids = _legacy_registry_ids()

    for item in mappings:
        if item.registry not in _ALLOWED_REGISTRIES:
            raise ValueError(f"{item.sympy_id}: invalid registry {item.registry!r}")
        if item.relationship not in _ALLOWED_RELATIONSHIPS:
            raise ValueError(f"{item.sympy_id}: invalid relationship {item.relationship!r}")
        if item.lean_status not in _ALLOWED_STATUSES:
            raise ValueError(f"{item.sympy_id}: invalid Lean status {item.lean_status!r}")
        if not item.lean_declarations:
            raise ValueError(f"{item.sympy_id}: no Lean declaration named")
        if any(not name.strip() for name in item.lean_declarations):
            raise ValueError(f"{item.sympy_id}: blank Lean declaration")
        if item.registry == "full" and item.sympy_id not in full_ids:
            raise ValueError(f"{item.sympy_id}: not present in full registry")
        if item.registry == "legacy" and item.sympy_id not in legacy_ids:
            raise ValueError(f"{item.sympy_id}: not present in legacy registry")
        if item.lean_status == "stated_todo" and item.relationship != "adjacent_todo_only":
            raise ValueError(f"{item.sympy_id}: TODO declaration cannot be represented as a proof")


def lean_coverage_summary(mappings: list[LeanMapping]) -> dict[str, Any]:
    mapped_full = {item.sympy_id for item in mappings if item.registry == "full"}
    mapped_legacy = {item.sympy_id for item in mappings if item.registry == "legacy"}
    proved = [item for item in mappings if item.lean_status == "proved"]
    todos = [item for item in mappings if item.lean_status == "stated_todo"]
    return {
        "mapping_count": len(mappings),
        "proved_mapping_count": len(proved),
        "todo_mapping_count": len(todos),
        "full_registry_mapped": len(mapped_full),
        "full_registry_total": len(load_full_registry()),
        "legacy_registry_mapped": len(mapped_legacy),
        "legacy_registry_total": len(_legacy_registry_ids()),
        "note": "Mapping coverage is not theorem coverage; many WCT claims remain intentionally open.",
    }
