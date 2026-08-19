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
    "PASS": 68,
    "CONDITIONAL": 18,
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

    for index, line in enumerate(lines):
        if line.startswith("# ") and not line.startswith("## "):
            family = _clean_markdown(line[2:])
            continue
        match = ID_RE.match(line)
        if match:
            object_id, name = match.groups()
            current = {
                "id": object_id,
                "name": _clean_markdown(name),
                "family": family,
                "heading_line": index + 1,
                "formula_lines": [],
                "body_lines": [],
            }
            objects[object_id] = current
            continue
        if current is None:
            continue
        current["body_lines"].append(line)
        if "$$" in line or line.strip().startswith("\\[") or line.strip().endswith("\\]"):
            current["formula_lines"].append(line)

    for obj in objects.values():
        body = "\n".join(obj.pop("body_lines"))
        description_lines = []
        for raw in body.splitlines():
            text = _clean_markdown(raw)
            if not text or text.startswith("Current effective status:") or text.startswith("Baseline status:") or text.startswith("Status provenance:"):
                continue
            if text.startswith("$$") or raw.strip().startswith("\\[") or raw.strip().endswith("\\]"):
                continue
            description_lines.append(text)
            if len(description_lines) >= 3:
                break
        obj["description"] = " ".join(description_lines)
        obj["formula"] = "\n".join(obj.pop("formula_lines"))[:4000]
        obj["canonical_url"] = f"{CANONICAL_PAGE}#{_github_slug(obj['id'] + '-' + obj['name'])}"
    return objects


def _verification_kind(checker: str, status: str) -> str:
    if status == "DEFINITION":
        return "DEFINITION"
    if status == "OPEN":
        return "UNRESOLVED"
    lowered = checker.lower()
    if "dimension" in lowered or "units" in lowered:
        return "DIMENSIONAL_CHECK"
    if "counterexample" in lowered:
        return "COUNTEREXAMPLE"
    if "gradient_flow" in lowered or "lyapunov" in lowered:
        return "VARIATIONAL_DERIVATION"
    if "derived" in lowered or "identity" in lowered or "consistency" in lowered or "substitution" in lowered:
        return "SYMBOLIC_DERIVATION"
    if "bound" in lowered or "positivity" in lowered or "nonnegative" in lowered:
        return "INEQUALITY_CHECK"
    return "ALGEBRAIC_IDENTITY"


def _scope_for(status: str, checker: str) -> str:
    if status == "OPEN":
        return "OPEN_PROBLEM"
    if status == "DEFINITION":
        return "DEFINITIONAL"
    if status == "CONDITIONAL":
        return "MODEL_CONDITIONAL"
    if any(token in checker for token in ("dimension", "units")):
        return "DIMENSIONAL_CONSISTENCY"
    return "INTERNAL_CONSISTENCY"


def _source_commit(repo_path: Path) -> str | None:
    try:
        return subprocess.check_output(
            ["git", "-C", str(repo_path), "rev-parse", "HEAD"],
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
    except Exception:
        return None


def compile_registry(canonical_markdown: str) -> dict[str, Any]:
    baseline_rows = _load_rows(BASELINE_PATH)
    override_rows = _load_rows(OVERRIDE_PATH)
    metadata = _load_yaml(VERIFICATION_METADATA_PATH) or {}
    assumptions = _load_yaml(ASSUMPTION_PATH) or []
    lean_map = _load_yaml(LEAN_MAP_PATH) or []
    claims = _load_yaml(CLAIMS_PATH) or []
    canonical = parse_canonical_markdown(canonical_markdown)

    baseline = {row[0]: row for row in baseline_rows}
    overrides = {row[0]: row for row in override_rows}
    lean_by_id: dict[str, list[dict[str, Any]]] = {}
    for item in lean_map:
        lean_by_id.setdefault(str(item.get("equation_id")), []).append(item)

    objects: list[dict[str, Any]] = []
    for object_id, (_id, base_checker, base_status) in baseline.items():
        override = overrides.get(object_id)
        checker = override[1] if override else base_checker
        effective_status = override[2] if override else base_status
        canonical_obj = canonical.get(object_id, {})
        item_metadata = metadata.get(object_id, {})
        checker_metadata = item_metadata.get("checkers", {}).get(checker, {}) if isinstance(item_metadata, dict) else {}
        object_assumptions = item_metadata.get("assumptions", []) if isinstance(item_metadata, dict) else []
        verification_kind = checker_metadata.get("kind") or _verification_kind(checker, effective_status)
        scope = checker_metadata.get("scope") or _scope_for(effective_status, checker)

        objects.append(
            {
                "canonical_id": object_id,
                "aliases": item_metadata.get("aliases", []) if isinstance(item_metadata, dict) else [],
                "name": canonical_obj.get("name", object_id),
                "family": canonical_obj.get("family", "Registry"),
                "canonical_url": canonical_obj.get("canonical_url"),
                "formula": canonical_obj.get("formula", ""),
                "definition": canonical_obj.get("description", ""),
                "status": {
                    "baseline": base_status,
                    "effective": effective_status,
                    "changed": bool(override and effective_status != base_status),
                    "changed_by": f"derived_overrides.yaml:{checker}" if override else None,
                    "source_file": "equations/derived_overrides.yaml" if override else "equations/full_registry.yaml",
                },
                "verification": {
                    "outcome": effective_status,
                    "kind": verification_kind,
                    "scope": scope,
                    "checker": [checker],
                    "baseline_checker": base_checker,
                    "meaning": "The assigned executable classification is reported under its declared assumptions.",
                },
                "assumption_ids": object_assumptions,
                "lean_support": lean_by_id.get(object_id, []),
                "empirical_validation": {
                    "status": item_metadata.get("empirical_status", "NOT_APPLICABLE" if effective_status in {"PASS", "DEFINITION"} else "NOT_TESTED") if isinstance(item_metadata, dict) else "NOT_TESTED",
                    "evidence_ids": item_metadata.get("evidence_ids", []) if isinstance(item_metadata, dict) else [],
                    "independent_replication": item_metadata.get("independent_replication", "NONE") if isinstance(item_metadata, dict) else "NONE",
                },
                "dependencies": item_metadata.get("dependencies", []) if isinstance(item_metadata, dict) else [],
                "claim_ids": item_metadata.get("claim_ids", []) if isinstance(item_metadata, dict) else [],
                "provenance": {
                    "canonical": {
                        "repository": "geometry_of_resonance",
                        "path": "WCT_FULL_EQUATION_LIST_CORRECTED.md",
                        "heading_line": canonical_obj.get("heading_line"),
                    },
                    "symbolic_registry": {
                        "repository": "wct-sympy",
                        "path": "equations/full_registry.yaml",
                    },
                    "derived_override": {
                        "repository": "wct-sympy",
                        "path": "equations/derived_overrides.yaml",
                    } if override else None,
                },
            }
        )

    counts = Counter(obj["status"]["effective"] for obj in objects)
    return {
        "schema_version": "2.0.0",
        "registry_id": "wct-effective-registry",
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "status_policy": {
            "PASS": "The assigned check succeeds under its declared assumptions.",
            "CONDITIONAL": "Additional mathematical, model, regularity, or empirical assumptions remain required.",
            "DEFINITION": "The object is a definition, ansatz, or bookkeeping object rather than a theorem.",
            "OPEN": "The assigned proof, derivation, simulation, or empirical test remains unresolved.",
            "FAIL": "The encoded statement is contradicted by its assigned checker.",
        },
        "status_precedence": [
            "equations/derived_overrides.yaml",
            "equations/full_registry.yaml",
            "canonical equation narrative",
        ],
        "counts": {status: counts.get(status, 0) for status in ("PASS", "CONDITIONAL", "DEFINITION", "OPEN", "FAIL")},
        "total": len(objects),
        "assumptions": assumptions,
        "claims": claims,
        "objects": objects,
        "provenance": {
            "registry_version": "2.0.0",
            "source_commits": {
                "wct-sympy": _source_commit(ROOT),
                "geometry_of_resonance": os.environ.get("WCT_GEOMETRY_SHA"),
                "wct-lean": os.environ.get("WCT_LEAN_SHA"),
            },
            "generator": "scripts/compile_registry.py",
        },
    }


def validate_artifact(document: dict[str, Any]) -> dict[str, Any]:
    errors: list[str] = []
    objects = document.get("objects", [])
    ids = [obj.get("canonical_id") for obj in objects]
    if len(objects) != 142:
        errors.append(f"expected 142 objects, got {len(objects)}")
    if len(set(ids)) != len(ids):
        errors.append("canonical IDs are not unique")
    if document.get("counts") != EXPECTED_COUNTS:
        errors.append(f"unexpected effective counts: {document.get('counts')}")
    for obj in objects:
        status = obj.get("status", {}).get("effective")
        if status == "PASS":
            verification = obj.get("verification", {})
            if not verification.get("checker"):
                errors.append(f"{obj.get('canonical_id')}: PASS lacks checker")
            if verification.get("kind") == "UNRESOLVED":
                errors.append(f"{obj.get('canonical_id')}: PASS cannot be unresolved")
    return {"valid": not errors, "errors": errors}


def _read_canonical(path: Path | None) -> str:
    if path:
        return path.read_text(encoding="utf-8")
    with urllib.request.urlopen(CANONICAL_URL, timeout=30) as response:
        return response.read().decode("utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--canonical-file", type=Path)
    parser.add_argument("--json-out", type=Path, default=DEFAULT_JSON_OUT)
    parser.add_argument("--yaml-out", type=Path, default=DEFAULT_YAML_OUT)
    parser.add_argument("--report-out", type=Path, default=DEFAULT_REPORT_OUT)
    args = parser.parse_args()

    canonical = _read_canonical(args.canonical_file)
    artifact = compile_registry(canonical)
    report = validate_artifact(artifact)
    args.json_out.write_text(json.dumps(artifact, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    args.yaml_out.write_text(yaml.safe_dump(artifact, sort_keys=False, allow_unicode=True), encoding="utf-8")
    args.report_out.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(
        "Compiled WCT registry: "
        f"{artifact['total']} objects; "
        + ", ".join(f"{key}={value}" for key, value in artifact["counts"].items())
    )
    if not report["valid"]:
        raise SystemExit("Registry validation failed:\n- " + "\n- ".join(report["errors"]))


if __name__ == "__main__":
    main()
