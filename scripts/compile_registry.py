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
    "PASS": 59,
    "CONDITIONAL": 27,
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
            "limitations": [row["caveat"]] if row.get("caveat") else [],
        }
    return mappings


def compile_registry(canonical_markdown: str) -> dict[str, Any]:
    baseline_rows = _load_rows(BASELINE_PATH)
    override_rows = _load_rows(OVERRIDE_PATH)
    baseline = {row[0]: {"checker": row[1], "status": row[2]} for row in baseline_rows}
    overrides = {row[0]: {"checker": row[1], "status": row[2]} for row in override_rows}
    if len(baseline) != len(baseline_rows):
        raise ValueError("Duplicate canonical IDs in baseline registry")
    unknown_overrides = sorted(set(overrides) - set(baseline))
    if unknown_overrides:
        raise ValueError(f"Overrides reference unknown IDs: {unknown_overrides}")

    canonical = parse_canonical_markdown(canonical_markdown)
    missing_canonical = sorted(set(baseline) - set(canonical))
    if missing_canonical:
        raise ValueError(f"Canonical equation document is missing IDs: {missing_canonical}")

    metadata = (_load_yaml(VERIFICATION_METADATA_PATH) or {}).get("objects", {})
    assumption_doc = _load_yaml(ASSUMPTION_PATH) or {}
    assumption_objects = assumption_doc.get("assumptions", {})
    assumption_links = assumption_doc.get("object_links", {})
    lean = _lean_mappings()
    claims_doc = _load_yaml(CLAIMS_PATH) or {"claims": {}}

    objects: list[dict[str, Any]] = []
    for object_id, baseline_entry in baseline.items():
        effective_entry = overrides.get(object_id, baseline_entry)
        changed = effective_entry != baseline_entry
        object_metadata = metadata.get(object_id, {})
        kind = object_metadata.get(
            "verification_kind",
            infer_verification_kind(effective_entry["checker"], effective_entry["status"]),
        )
        scope = object_metadata.get("scope", _default_scope(effective_entry["status"], kind))
        empirical_status = object_metadata.get(
            "empirical_status", _default_empirical_status(effective_entry["status"], kind)
        )
        canonical_entry = canonical[object_id]
        formalization = lean.get(
            object_id,
            {
                "status": "OPEN",
                "relationship": None,
                "declaration_type": "unmapped",
                "declarations": [],
                "source": None,
                "limitations": [],
            },
        )
        object_assumptions = list(assumption_links.get(object_id, []))
        objects.append(
            {
                "canonical_id": object_id,
                "aliases": [],
                "name": canonical_entry["name"],
                "object_type": "definition" if effective_entry["status"] == "DEFINITION" else "equation",
                "family": canonical_entry["family"],
                "formula": canonical_entry["formula"],
                "definition": canonical_entry["definition"],
                "status": {
                    "baseline": baseline_entry["status"],
                    "effective": effective_entry["status"],
                    "changed": changed,
                    "changed_by": (
                        f"derived_overrides.yaml:{effective_entry['checker']}" if changed else None
                    ),
                    "source_file": (
                        "equations/derived_overrides.yaml"
                        if changed
                        else "equations/full_registry.yaml"
                    ),
                },
                "verification": {
                    "outcome": effective_entry["status"],
                    "kind": kind,
                    "scope": scope,
                    "checker": [effective_entry["checker"]],
                    "baseline_checker": baseline_entry["checker"],
                    "meaning": object_metadata.get(
                        "meaning",
                        "The assigned executable classification is reported under its declared assumptions.",
                    ),
                    "limitations": object_metadata.get("limitations", []),
                },
                "assumptions": object_assumptions,
                "formalization": formalization,
                "empirical_validation": {
                    "status": empirical_status,
                    "evidence_ids": object_metadata.get("evidence_ids", []),
                    "independent_replication": object_metadata.get(
                        "independent_replication", "NONE"
                    ),
                },
                "dependencies": {
                    "equations": object_metadata.get("equation_dependencies", []),
                    "assumptions": object_assumptions,
                    "claims": object_metadata.get("claims", []),
                    "papers": object_metadata.get("papers", []),
                },
                "sources": {
                    "canonical_equation": {
                        "repository": "geometry_of_resonance",
                        "path": "WCT_FULL_EQUATION_LIST_CORRECTED.md",
                        "fragment": object_id,
                        "url": canonical_entry["source"],
                    },
                    "symbolic_registry": {
                        "repository": "wct-sympy",
                        "path": "equations/full_registry.yaml",
                    },
                    "derived_override": (
                        {
                            "repository": "wct-sympy",
                            "path": "equations/derived_overrides.yaml",
                        }
                        if changed
                        else None
                    ),
                },
            }
        )

    counts = Counter(obj["status"]["effective"] for obj in objects)
    for status in VALID_STATUSES:
        counts.setdefault(status, 0)

    generated_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    artifact = {
        "schema_version": "2.0.0",
        "registry_id": "wct-effective-registry",
        "generated_at": generated_at,
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
        "counts": {status: counts[status] for status in ("PASS", "CONDITIONAL", "DEFINITION", "OPEN", "FAIL")},
        "total": len(objects),
        "assumptions": [
            {"assumption_id": assumption_id, **details}
            for assumption_id, details in assumption_objects.items()
        ],
        "claims": [
            {"claim_id": claim_id, **details}
            for claim_id, details in claims_doc.get("claims", {}).items()
        ],
        "objects": objects,
        "provenance": {
            "registry_version": "2.0.0",
            "source_commits": {
                "wct-sympy": _git_sha(),
                "geometry_of_resonance": os.environ.get("WCT_GEOMETRY_SHA"),
                "wct-lean": os.environ.get("WCT_LEAN_SHA"),
            },
            "generator": "scripts/compile_registry.py",
        },
    }
    return artifact


def validate_artifact(artifact: dict[str, Any]) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    objects = artifact["objects"]
    ids = [obj["canonical_id"] for obj in objects]
    if len(objects) != 142:
        errors.append(f"Expected 142 objects, found {len(objects)}")
    duplicates = sorted({object_id for object_id in ids if ids.count(object_id) > 1})
    if duplicates:
        errors.append(f"Duplicate canonical IDs: {duplicates}")

    counts = artifact["counts"]
    if counts != EXPECTED_COUNTS:
        errors.append(f"Effective totals differ from expected totals: {counts}")

    known_ids = set(ids)
    known_assumptions = {row["assumption_id"] for row in artifact["assumptions"]}
    for obj in objects:
        object_id = obj["canonical_id"]
        verification = obj["verification"]
        if obj["status"]["effective"] == "PASS":
            if not verification["checker"]:
                errors.append(f"{object_id}: PASS has no checker")
            if verification["kind"] == "UNRESOLVED":
                errors.append(f"{object_id}: PASS has unresolved verification kind")
        if obj["status"]["changed"] and not obj["status"]["changed_by"]:
            errors.append(f"{object_id}: changed status lacks provenance")
        if obj["formalization"]["status"] == "PROVED" and not obj["formalization"]["declarations"]:
            errors.append(f"{object_id}: Lean PROVED has no named declaration")
        for assumption_id in obj["assumptions"]:
            if assumption_id not in known_assumptions:
                errors.append(f"{object_id}: unknown assumption {assumption_id}")

    for claim in artifact["claims"]:
        claim_id = claim["claim_id"]
        for object_id in claim.get("equations", []):
            if object_id not in known_ids:
                errors.append(f"{claim_id}: unknown equation {object_id}")
        for assumption_id in claim.get("assumptions", []):
            if assumption_id not in known_assumptions:
                errors.append(f"{claim_id}: unknown assumption {assumption_id}")
        if not claim.get("papers"):
            warnings.append(f"{claim_id}: no source-paper mapping yet")

    return {
        "schema_version": artifact["schema_version"],
        "generated_at": artifact["generated_at"],
        "valid": not errors,
        "errors": errors,
        "warnings": warnings,
        "counts": artifact["counts"],
        "total": artifact["total"],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--canonical-file", type=Path)
    parser.add_argument("--json-out", type=Path, default=DEFAULT_JSON_OUT)
    parser.add_argument("--yaml-out", type=Path, default=DEFAULT_YAML_OUT)
    parser.add_argument("--report-out", type=Path, default=DEFAULT_REPORT_OUT)
    args = parser.parse_args()

    artifact = compile_registry(_fetch_canonical(args.canonical_file))
    report = validate_artifact(artifact)
    if not report["valid"]:
        raise SystemExit("Compiled registry validation failed: " + "; ".join(report["errors"]))

    args.json_out.write_text(json.dumps(artifact, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    args.yaml_out.write_text(yaml.safe_dump(artifact, sort_keys=False, allow_unicode=True), encoding="utf-8")
    args.report_out.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(
        "Compiled WCT registry: "
        f"{artifact['total']} objects; "
        + ", ".join(f"{status}={count}" for status, count in artifact["counts"].items())
    )


if __name__ == "__main__":
    main()
