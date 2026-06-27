"""Load and validate the compact full-corpus equation registry."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

import yaml

from .models import AuditStatus, EquationSpec

ROOT = Path(__file__).resolve().parent.parent
REGISTRY_PATH = ROOT / "equations" / "full_registry.yaml"


def load_full_registry(path: str | Path | None = None) -> list[EquationSpec]:
    target = Path(path) if path else REGISTRY_PATH
    raw = yaml.safe_load(target.read_text(encoding="utf-8")) or []
    if not isinstance(raw, list):
        raise ValueError("full registry must be a YAML list")

    specs: list[EquationSpec] = []
    for row in raw:
        if not isinstance(row, list) or len(row) != 3:
            raise ValueError(f"invalid compact registry row: {row!r}")
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
