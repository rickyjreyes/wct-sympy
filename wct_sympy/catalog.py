"""Load and validate the generated full-corpus equation registry."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

import yaml

from .models import AuditStatus, EquationSpec

ROOT = Path(__file__).resolve().parent.parent
REGISTRY_PATH = ROOT / "equations" / "full_registry.yaml"


def _tuple(value: object) -> tuple[str, ...]:
    if value is None:
        return ()
    if isinstance(value, str):
        return (value,)
    return tuple(str(item) for item in value)  # type: ignore[arg-type]


def load_full_registry(path: str | Path | None = None) -> list[EquationSpec]:
    target = Path(path) if path else REGISTRY_PATH
    raw = yaml.safe_load(target.read_text(encoding="utf-8")) or []
    if not isinstance(raw, list):
        raise ValueError("full registry must be a YAML list")
    specs: list[EquationSpec] = []
    for item in raw:
        specs.append(
            EquationSpec(
                equation_id=str(item["equation_id"]),
                title=str(item["title"]),
                family=str(item.get("family", "")),
                source_document=str(item["source_document"]),
                source_heading=str(item.get("source_heading", "")),
                source_start_line=int(item.get("source_start_line", 0)),
                source_end_line=int(item.get("source_end_line", 0)),
                latex=_tuple(item.get("latex")),
                claim_class=str(item.get("claim_class", "definition")),
                audit_mode=str(item.get("audit_mode", "classification")),
                checker=str(item.get("checker", "classify_definition")),
                expected_status=AuditStatus(str(item.get("expected_status", "DEFINITION"))),
                assumptions=_tuple(item.get("assumptions")),
                notes=str(item.get("notes", "")),
            )
        )
    validate_registry(specs)
    return specs


def validate_registry(specs: Iterable[EquationSpec]) -> None:
    items = list(specs)
    ids = [spec.equation_id for spec in items]
    duplicates = sorted({eqid for eqid in ids if ids.count(eqid) > 1})
    if duplicates:
        raise ValueError(f"duplicate equation IDs: {duplicates}")

    required = {f"E{i}" for i in range(2, 83)} | {"E1A", "E1B"}
    required |= {f"CLE{i}" for i in range(1, 11)}
    required |= {f"CM{i}" for i in range(1, 21)}
    required |= {"M1", "M2", "M3", "M4", "M5", "M6A", "M6B", "M7", "M8"}
    required |= {"G1", "EX", "EY", "EZ", "FA"}
    missing = sorted(required - set(ids))
    if missing:
        raise ValueError(f"registry missing canonical IDs: {missing}")

    for spec in items:
        if not spec.title:
            raise ValueError(f"{spec.equation_id}: empty title")
        if not spec.checker:
            raise ValueError(f"{spec.equation_id}: no checker assigned")
        source = ROOT / spec.source_document
        if not source.exists():
            raise FileNotFoundError(f"{spec.equation_id}: missing source document {source}")
