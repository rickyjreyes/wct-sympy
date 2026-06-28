from __future__ import annotations

import importlib.util
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "compile_registry", ROOT / "scripts" / "compile_registry.py"
)
assert SPEC and SPEC.loader
compile_registry = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(compile_registry)


def _canonical_fixture() -> str:
    rows = yaml.safe_load((ROOT / "equations" / "full_registry.yaml").read_text())
    chunks = ["# Wave Confinement Theory — Test Registry"]
    for object_id, _checker, status in rows:
        chunks.extend(
            [
                f"## {object_id} — Equation {object_id}",
                "",
                f"**Status:** `{status}`",
                "",
                f"The canonical test description for {object_id}.",
                "",
                "$$x=x$$",
                "",
            ]
        )
    return "\n".join(chunks)


def test_compiler_applies_effective_overrides_and_preserves_baseline() -> None:
    artifact = compile_registry.compile_registry(_canonical_fixture())
    report = compile_registry.validate_artifact(artifact)
    assert report["valid"], report["errors"]
    assert artifact["total"] == 142
    assert artifact["counts"] == {
        "PASS": 59,
        "CONDITIONAL": 27,
        "DEFINITION": 26,
        "OPEN": 30,
        "FAIL": 0,
    }

    by_id = {obj["canonical_id"]: obj for obj in artifact["objects"]}
    assert by_id["E5"]["status"]["baseline"] == "CONDITIONAL"
    assert by_id["E5"]["status"]["effective"] == "PASS"
    assert by_id["E5"]["status"]["changed"] is True
    assert by_id["E5"]["verification"]["kind"] == "SYMBOLIC_DERIVATION"
    assert by_id["CM9"]["status"]["effective"] == "PASS"
    assert by_id["CM11"]["status"]["effective"] == "PASS"
    assert by_id["CM12"]["status"]["effective"] == "DEFINITION"
    assert by_id["CM13"]["status"]["effective"] == "DEFINITION"
    assert by_id["CM16"]["status"]["effective"] == "DEFINITION"
    assert by_id["CM18"]["status"]["effective"] == "DEFINITION"
    assert by_id["E70"]["status"]["effective"] == "CONDITIONAL"


def test_every_pass_has_checker_and_verification_kind() -> None:
    artifact = compile_registry.compile_registry(_canonical_fixture())
    for obj in artifact["objects"]:
        if obj["status"]["effective"] != "PASS":
            continue
        assert obj["verification"]["checker"], obj["canonical_id"]
        assert obj["verification"]["kind"] != "UNRESOLVED", obj["canonical_id"]


def test_claim_and_assumption_references_are_valid() -> None:
    artifact = compile_registry.compile_registry(_canonical_fixture())
    report = compile_registry.validate_artifact(artifact)
    assert not report["errors"]
