#!/usr/bin/env python3
"""Compile the effective WCT registry from canonical, symbolic, and Lean sources.

This script is the only supported place where baseline statuses and derived
overrides are merged. Generated consumers must use ``compiled-registry.json``
rather than maintaining an independent status table.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import urllib.request
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
BASELINE_PATH = ROOT / "equations" / "full_registry.yaml"
OVERRIDE_PATH = ROOT / "equations" / "derived_overrides.yaml"
VERIFICATION_METADATA_PATH = ROOT / "equations" / "verification_metadata.yaml"
ASSUMPTION_PATH = ROOT / "equations" / "assumptions.yaml"
LEAN_MAP_PATH = ROOT / "interoperability" / "lean_map.yaml"
CLAIMS_PATH = ROOT / "claims" / "initial_claims.yaml"
DEFAULT_JSON_OUT = ROOT / "compiled-registry.json"
DEFAULT_YAML_OUT = ROOT / "compiled-registry.yaml"
DEFAULT_REPORT_OUT = ROOT / "validation-report.json"
CANONICAL_URL = (
    "https://raw.githubusercontent.com/rickyjreyes/geometry_of_resonance/"
    "main/WCT_FULL_EQUATION_LIST_CORRECTED.md"
)
CANONICAL_PAGE = (
    "https://github.com/rickyjreyes/geometry_of_resonance/blob/main/"
    "WCT_FULL_EQUATION_LIST_CORRECTED.md"
)
EXPECTED_COUNTS = {
    "PASS": 60,
    "CONDITIONAL": 26,
    "DEFINITION": 26,
    "OPEN": 30,
    "FAIL": 0,
}
VALID_STATUSES = set(EXPECTED_COUNTS)
ID_RE = re.compile(
    r"^##\s+((?:M|E|CLE|CM|TOP|CORR)\d+[A-Z]?|G1|EX|EY|EZ|FA)\s+[—-]\s+(.+?)\s*$"
)


def _load_yaml(path: Path) -> Any:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def _load_rows(path: Path) -> list[list[str]]:
    rows = _load_yaml(path) or []
    if not isinstance(rows, list):
        raise ValueError(f"{path} must contain a YAML list")
    normalized: list[list[str]] = []
    for row in rows:
        if not isinstance(row, list) or len(row) != 3:
            raise ValueError(f"Invalid compact registry row in {path}: {row!r}")
        equation_id, checker, status = map(str, row)
        if status not in VALID_STATUSES:
            raise ValueError(f"{equation_id}: unsupported status {status}")
        normalized.append([equation_id, checker, status])
    return normalized


def _clean_markdown(text: str) -> str:
    text = re.sub(r"\[([^\]]+)\]\([^\)]+\)", r"\1", text)
    text = re.sub(r"[*_`]+", "", text)
    return re.sub(r"\s+", " ", text).strip()


def _github_slug(text: str) -> str:
    value = text.lower().replace("—", " ").replace("–", " ")
    value = re.sub(r"[^a-z0-9\s-]", "", value)
    return re.sub(r"[-\s]+", "-", value).strip("-")


def parse_canonical_markdown(markdown: str) -> dict[str, dict[str, Any]]:
    """Extract canonical names, families, formulas, and bounded descriptions."""
    lines = markdown.splitlines()
    family = "Registry"
    current: dict[str, Any] | None = None
    objects: dict[str, dict[str, Any]] = {}
    paragraph: list[str] = []
    in_math = False
    math_buffer: list[str] = []

    def flush_paragraph() -> None:
        nonlocal paragraph
        if current is not None and paragraph:
            value = _clean_markdown(" ".join(paragraph))
            if value:
                current["paragraphs"].append(value)
        paragraph = []

    def flush_current() -> None:
        nonlocal current
        flush_paragraph()
        if current is None:
            return
        definition = " ".join(current.pop("paragraphs")[:2]).strip()
        current["definition"] = (definition or f"{current['name']}.")[:1200]
        current["formula"] = "\n\n".join(current.pop("formulas")[:4]).strip()
        current["source"] = f"{CANONICAL_PAGE}#{current['anchor']}"
        objects[current["canonical_id"]] = current
        current = None

    for line in lines:
        if line.startswith("# ") and not line.startswith("## "):
            flush_paragraph()
            heading = _clean_markdown(line[2:])
            if heading and not heading.startswith("Wave Confinement Theory"):
                family = heading
            continue

        match = ID_RE.match(line)
        if match:
            flush_current()
            object_id, title = match.groups()
            heading = f"{object_id} — {title}"
            current = {
                "canonical_id": object_id,
                "name": _clean_markdown(title),
                "family": family,
                "anchor": _github_slug(heading),
                "formulas": [],
                "paragraphs": [],
            }
            continue

        if current is None:
            continue

        if "$$" in line:
            parts = line.split("$$")
            for index, part in enumerate(parts):
                if index % 2 == 1:
                    formula = part.strip()
                    if formula:
                        current["formulas"].append(formula)
                elif part.strip() and in_math:
                    math_buffer.append(part.strip())
            if line.count("$$") % 2 == 1:
                in_math = not in_math
                if not in_math and math_buffer:
                    current["formulas"].append("\n".join(math_buffer))
                    math_buffer = []
            flush_paragraph()
            continue

        if in_math:
            math_buffer.append(line)
            continue

        stripped = line.strip()
        if not stripped:
            flush_paragraph()
            continue
        if stripped.startswith(("|", "---", "#", "**Status", "```")):
            flush_paragraph()
            continue
        if re.match(r"^(?:- |\d+\. )", stripped):
            flush_paragraph()
            continue
        paragraph.append(stripped)

    flush_current()
    return objects


def _fetch_canonical(canonical_file: Path | None) -> str:
    if canonical_file:
        return canonical_file.read_text(encoding="utf-8")
    request = urllib.request.Request(
        CANONICAL_URL, headers={"User-Agent": "wct-compiled-registry-builder"}
    )
    with urllib.request.urlopen(request, timeout=45) as response:
        return response.read().decode("utf-8")


def _git_sha() -> str | None:
    env_sha = os.environ.get("GITHUB_SHA")
    if env_sha:
        return env_sha
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True, stderr=subprocess.DEVNULL
        ).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def infer_verification_kind(checker: str, status: str) -> str:
    name = checker.lower()
    if status == "DEFINITION" or name.startswith("classify_definition"):
        return "DEFINITION_CHECK"
    if status in {"OPEN", "CONDITIONAL"} and name.startswith("classify_"):
        return "UNRESOLVED"
    if any(token in name for token in ("dimension", "units", "_dim", "embedding")):
        return "DIMENSIONAL_CHECK"
    if any(token in name for token in ("variation", "gradient_flow", "lyapunov")):
        return "VARIATIONAL_DERIVATION"
    if any(token in name for token in ("counterexample", "uniqueness")):
        return "COUNTEREXAMPLE_TEST"
    if any(token in name for token in ("residual", "numerical")):
        return "NUMERICAL_RESIDUAL"
    if any(token in name for token in ("limit", "bounded", "denominator", "green_kernel")):
        return "LIMIT_CHECK"
    if any(token in name for token in ("stationary", "sign", "threshold", "maximum", "minimum")):
        return "SIGN_OR_EXTREMUM_CHECK"
    if "consistency" in name:
        return "CONSISTENCY_CHECK"
    if any(token in name for token in ("identity", "reduction", "equivalence", "derived")):
        return "ALGEBRAIC_IDENTITY"
    if name.startswith("check_"):
        return "SYMBOLIC_DERIVATION"
    return "UNRESOLVED"


def _default_scope(status: str, kind: str) -> str:
    if status == "DEFINITION":
        return "DEFINITIONAL"
    if status == "OPEN":
        return "UNRESOLVED"
    if status == "CONDITIONAL":
        return "MODEL_CONDITIONAL"
    if kind in {"ALGEBRAIC_IDENTITY", "DIMENSIONAL_CHECK"}:
        return "INTERNAL_CONSISTENCY"
    return "MODEL_CONDITIONAL"


def _default_empirical_status(status: str, kind: str) -> str:
    if status == "DEFINITION" or kind in {"ALGEBRAIC_IDENTITY", "DIMENSIONAL_CHECK"}:
        return "NOT_APPLICABLE"
    return "NOT_TESTED"


def _lean_mappings() -> dict[str, dict[str, Any]]:
    raw = _load_yaml(LEAN_MAP_PATH) or {}
    mappings: dict[str, dict[str, Any]] = {}
    for row in raw.get("mappings", []):
        if row.get("registry") != "full":
            continue
        object_id = str(row["sympy_id"])
        status = str(row.get("lean_status", "open")).upper()
        if status == "PROVED" and not row.get("lean_declarations"):
            raise ValueError(f"{object_id}: Lean PROVED mapping has no declarations")
        mappings[object_id] = {
            "status": status,
            "relationship": row.get("relationship"),
            "declaration_type": row.get("relationship"),
            "declarations": row.get("lean_declarations", []),
            "source": row.get("lean_source"),
