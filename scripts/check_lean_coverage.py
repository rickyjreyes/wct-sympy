#!/usr/bin/env python3
"""Validate the wct-sympy to wct-lean metadata bridge.

No Lean executable is required. Formal proof checking remains the responsibility
of `lake build` in the separate rickyjreyes/wct-lean repository.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from wct_sympy.lean_bridge import lean_coverage_summary, load_lean_map  # noqa: E402


def main() -> int:
    metadata, mappings = load_lean_map()
    report = {
        "lean_repository": metadata["lean_repository"],
        "policy": metadata.get("policy", {}),
        "summary": lean_coverage_summary(mappings),
        "mappings": [
            {
                "sympy_id": item.sympy_id,
                "registry": item.registry,
                "relationship": item.relationship,
                "lean_status": item.lean_status,
                "lean_source": item.lean_source,
                "lean_declarations": list(item.lean_declarations),
                "caveat": item.caveat,
            }
            for item in mappings
        ],
    }

    output_dir = ROOT / "tables"
    output_dir.mkdir(exist_ok=True)
    output_path = output_dir / "lean_coverage.json"
    output_path.write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")

    summary = report["summary"]
    print("WCT SymPy / Lean bridge")
    print("=" * 64)
    print(f"repository: {report['lean_repository']}")
    print(f"mappings: {summary['mapping_count']}")
    print(f"proved support mappings: {summary['proved_mapping_count']}")
    print(f"stated TODO mappings: {summary['todo_mapping_count']}")
    print(f"report: {output_path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
