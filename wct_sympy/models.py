"""Typed models used by the full-corpus symbolic audit."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Mapping


class AuditStatus(str, Enum):
    """Scientific status of one equation-level audit.

    PASS
        The stated algebraic/dimensional claim follows under the listed assumptions.
    FAIL
        The stated claim is contradicted by symbolic algebra, dimensions, or a counterexample.
    CONDITIONAL
        Correct only after adding explicit assumptions not present in the bare equation.
    DEFINITION
        A definition or ansatz is syntactically represented but is not itself a theorem.
    OPEN
        A conjecture, empirical claim, or theorem obligation not decidable by SymPy alone.
    NOT_EXECUTABLE
        Source exists, but the current audit has no faithful executable semantics for it.
    """

    PASS = "PASS"
    FAIL = "FAIL"
    CONDITIONAL = "CONDITIONAL"
    DEFINITION = "DEFINITION"
    OPEN = "OPEN"
    NOT_EXECUTABLE = "NOT_EXECUTABLE"


@dataclass(frozen=True)
class EquationSpec:
    equation_id: str
    title: str
    family: str
    source_document: str
    source_heading: str
    source_start_line: int
    source_end_line: int
    latex: tuple[str, ...] = ()
    claim_class: str = "definition"
    audit_mode: str = "classification"
    checker: str = "classify_definition"
    expected_status: AuditStatus = AuditStatus.DEFINITION
    assumptions: tuple[str, ...] = ()
    notes: str = ""


@dataclass
class AuditResult:
    equation_id: str
    title: str
    status: AuditStatus
    expected_status: AuditStatus
    audit_mode: str
    value: Any = None
    expected: Any = None
    residual: float | None = None
    reason: str = ""
    assumptions: tuple[str, ...] = ()
    evidence: Mapping[str, Any] = field(default_factory=dict)

    @property
    def expectation_matches(self) -> bool:
        return self.status == self.expected_status

    def as_row(self) -> dict[str, str]:
        return {
            "equation_id": self.equation_id,
            "title": self.title,
            "status": self.status.value,
            "expected_status": self.expected_status.value,
            "expectation_matches": str(self.expectation_matches),
            "audit_mode": self.audit_mode,
            "value": "" if self.value is None else str(self.value),
            "expected": "" if self.expected is None else str(self.expected),
            "residual": "" if self.residual is None else f"{self.residual:.12e}",
            "assumptions": "; ".join(self.assumptions),
            "reason": self.reason,
        }
