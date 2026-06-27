"""Load and validate the compact full-corpus equation registry."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

import yaml

from .models import AuditStatus, EquationSpec

ROOT = Path(__file__).resolve().parent.parent
REGISTRY_PATH = ROOT / "equations" / "full_registry.yaml"
DERIVED_OVERRIDES_PATH = ROOT / "equations" / "derived_overrides.yaml"


def _load_compact_rows(path: Path) -> list[list[object]]:
    raw = yaml.safe_load(path.read_text(encoding="utf-8")) or []
    if not isinstance(raw, list):
        raise ValueError(f"{path.name} must be a YAML list")
    for row in raw:
        if not isinstance(row, list) or len(row) != 3:
            raise ValueError(f"invalid compact registry row in {path.name}: {row!r}")
    return raw


def _apply_derived_overrides(
    rows: list[list[object]], override_path: Path
) -> list[list[object]]:
    if not override_path.exists():
        return rows

    overrides = _load_compact_rows(override_path)
    override_map: dict[str, list[object]] = {}
    for row in overrides:
        equation_id = str(row[0])
        if equation_id in override_map:
            raise ValueError(f"duplicate derived override: {equation_id}")
        override_map[equation_id] = row

    base_ids = {str(row[0]) for row in rows}
    unknown = sorted(set(override_map) - base_ids)
    if unknown:
        raise ValueError(f"derived overrides reference unknown IDs: {unknown}")

    return [override_map.get(str(row[0]), row) for row in rows]


def load_full_registry(path: str | Path | None = None) -> list[EquationSpec]:
    target = Path(path) if path else REGISTRY_PATH
    raw = _load_compact_rows(target)

    override_path = (
        DERIVED_OVERRIDES_PATH
        if target == REGISTRY_PATH
        else target.with_name("derived_overrides.yaml")
    )
    raw = _apply_derived_overrides(raw, override_path)

    specs: list[EquationSpec] = []
    for row in raw:
        equation_id, checker, status_text = map(str, row)
        status = AuditStatus(status_text)
        source = "MASTER_EQUATIONS.md" if equation_id.startswith("M") else "EQUATIONS.md"
        specs.append(
            EquationSpec(
                equation_id=equation_id,
                title=f"Equation {equation_id}",
                family="Master equations" if equation_id.startswith("M") else "Canonical equations",
                source_document=source,
                source_heading=equation_id,
                source_start_line=0,
                source_end_line=0,
                checker=checker,
                expected_status=status,
                claim_class=status.value.lower(),
                audit_mode="classification" if checker.startswith("classify_") else "symbolic-audit",
            )
        )

    validate_registry(specs)
    return specs


def validate_registry(specs: Iterable[EquationSpec]) -> None:
    items = list(specs)
    ids = [spec.equation_id for spec in items]
    duplicates = sorted({equation_id for equation_id in ids if ids.count(equation_id) > 1})
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
        if spec.checker == "":
            raise ValueError(f"{spec.equation_id}: no checker assigned")
        if not (ROOT / spec.source_document).exists():
            raise FileNotFoundError(f"{spec.equation_id}: missing {spec.source_document}")
