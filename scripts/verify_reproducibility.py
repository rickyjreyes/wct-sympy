#!/usr/bin/env python3
"""Verify pinned symbolic inputs and semantic registry regeneration."""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
EXPECTED_COUNTS = {"PASS": 59, "CONDITIONAL": 27, "DEFINITION": 26, "OPEN": 30, "FAIL": 0}


def git_blob_sha1(path: Path) -> str:
    content = path.read_bytes()
    header = f"blob {len(content)}\0".encode("ascii")
    return hashlib.sha1(header + content).hexdigest()


def canonical_json_sha256(value: Any) -> str:
    data = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(data).hexdigest()


def normalize_registry(document: dict[str, Any]) -> dict[str, Any]:
    normalized = copy.deepcopy(document)
    normalized.pop("generated_at", None)
    provenance = normalized.get("provenance")
    if isinstance(provenance, dict):
        provenance.pop("source_commits", None)
    return normalized


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--expected", type=Path, default=ROOT / "reproducibility" / "expected-source-hashes.json")
    parser.add_argument("--committed-registry", type=Path, default=ROOT / "compiled-registry.json")
    parser.add_argument("--generated-registry", type=Path)
    parser.add_argument("--report", type=Path, default=ROOT / "reproducibility-report.json")
    args = parser.parse_args()

    expected = json.loads(args.expected.read_text(encoding="utf-8"))
    failures: list[str] = []
    actual_sources: dict[str, str] = {}
    for relative, wanted in sorted(expected["files"].items()):
        path = ROOT / relative
        if not path.is_file():
            failures.append(f"missing source file: {relative}")
            continue
        got = git_blob_sha1(path)
        actual_sources[relative] = got
        if got != wanted:
            failures.append(f"{relative}: expected git blob {wanted}, got {got}")

    committed = json.loads(args.committed_registry.read_text(encoding="utf-8"))
    if committed.get("counts") != EXPECTED_COUNTS:
        failures.append(f"committed counts differ: {committed.get('counts')}")
    committed_semantic_hash = canonical_json_sha256(normalize_registry(committed))

    generated_semantic_hash = None
    if args.generated_registry:
        generated = json.loads(args.generated_registry.read_text(encoding="utf-8"))
        if generated.get("counts") != EXPECTED_COUNTS:
            failures.append(f"generated counts differ: {generated.get('counts')}")
        generated_semantic_hash = canonical_json_sha256(normalize_registry(generated))
        if generated_semantic_hash != committed_semantic_hash:
            failures.append(
                "generated registry differs semantically from the committed registry: "
                f"expected {committed_semantic_hash}, got {generated_semantic_hash}"
            )

    report = {
        "schema_version": "1.0.0",
        "source_hash_algorithm": "git-blob-sha1",
        "source_hashes": actual_sources,
        "committed_registry_semantic_sha256": committed_semantic_hash,
        "generated_registry_semantic_sha256": generated_semantic_hash,
        "status": "PASS" if not failures else "FAIL",
        "failures": failures,
    }
    args.report.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))
    if failures:
        raise SystemExit("Symbolic reproducibility verification failed:\n- " + "\n- ".join(failures))


if __name__ == "__main__":
    main()
