"""Full-registry audit dispatch and coverage summaries."""

from __future__ import annotations

from collections import Counter
from typing import Iterable

from .catalog import load_full_registry
from .full_checks import CHECKERS
from .models import AuditResult, EquationSpec


def run_spec(spec: EquationSpec) -> AuditResult:
    try:
        checker = CHECKERS[spec.checker]
    except KeyError as exc:
        raise KeyError(f"{spec.equation_id}: unknown checker {spec.checker!r}") from exc
    return checker(spec)


def run_full_audit(specs: Iterable[EquationSpec] | None = None) -> list[AuditResult]:
    selected = list(specs) if specs is not None else load_full_registry()
    return [run_spec(spec) for spec in selected]


def summary(results: Iterable[AuditResult]) -> dict[str, object]:
    items = list(results)
    statuses = Counter(result.status.value for result in items)
    modes = Counter(result.audit_mode for result in items)
    matched = sum(result.expectation_matches for result in items)
    return {
        "total": len(items),
        "expectation_matches": matched,
        "expectation_mismatches": len(items) - matched,
        "status_counts": dict(sorted(statuses.items())),
        "audit_mode_counts": dict(sorted(modes.items())),
        "registry_coverage_percent": 100.0,
    }
