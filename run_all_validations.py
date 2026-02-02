#!/usr/bin/env python3
"""
WCT Validation Suite Runner
Runs all wct_validate_*.py scripts and reports pass/fail status.
"""

import subprocess
import sys
import os
from pathlib import Path
import time

def run_validation(script_path):
    """Run a single validation script and return (success, output, error)."""
    try:
        result = subprocess.run(
            [sys.executable, str(script_path)],
            capture_output=True,
            text=True,
            timeout=30,
            cwd=script_path.parent
        )
        success = result.returncode == 0
        return success, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return False, "", "TIMEOUT: Script took longer than 30 seconds"
    except Exception as e:
        return False, "", str(e)

def main():
    # Locate project directory
    project_dir = Path("/mnt/project")
    if not project_dir.exists():
        project_dir = Path(".")

    extended_dir = project_dir / "wct_validation_suite_extended"

    # Core validation scripts (assertive)
    validation_scripts = sorted(project_dir.glob("wct_validate_*.py"))

    # Other top-level scripts
    other_scripts = sorted(project_dir.glob("*.py"))
    other_scripts = [
        s for s in other_scripts
        if not s.name.startswith("wct_validate_")
        and s.name != "run_all_validations.py"
    ]

    # Extended diagnostics (non-assertive)
    extended_scripts = []
    if extended_dir.exists():
        extended_scripts = sorted(extended_dir.glob("*.py"))

    print("=" * 70)
    print("WAVE CONFINEMENT THEORY - VALIDATION SUITE")
    print("=" * 70)
    print(f"Found {len(validation_scripts)} validation scripts")
    print(f"Found {len(other_scripts)} other scripts")
    print(f"Found {len(extended_scripts)} extended diagnostic scripts")
    print()

    # --------------------------------------------------
    # Run core validation scripts
    # --------------------------------------------------
    print("VALIDATION SCRIPTS (wct_validate_*.py)")
    print("-" * 70)

    results = {"pass": 0, "fail": 0}

    for script in validation_scripts:
        start = time.time()
        success, stdout, stderr = run_validation(script)
        elapsed = time.time() - start

        status = "✓ PASS" if success else "✗ FAIL"
        if success:
            results["pass"] += 1
        else:
            results["fail"] += 1

        print(f"{status} | {script.name:<45} | {elapsed:.2f}s")

        if not success and stderr:
            print(f"       Error: {stderr[:120]}...")

    print()
    print("-" * 70)
    print(f"VALIDATION RESULTS: {results['pass']} passed, {results['fail']} failed")
    print("-" * 70)

    # --------------------------------------------------
    # Run other scripts (non-assertive utilities)
    # --------------------------------------------------
    print()
    print("OTHER SCRIPTS")
    print("-" * 70)

    for script in other_scripts:
        start = time.time()
        success, stdout, stderr = run_validation(script)
        elapsed = time.time() - start
        status = "✓ PASS" if success else "✗ FAIL"
        print(f"{status} | {script.name:<45} | {elapsed:.2f}s")

    # --------------------------------------------------
    # Run extended diagnostics (never affect pass/fail)
    # --------------------------------------------------
    if extended_scripts:
        print()
        print("EXTENDED DIAGNOSTICS (NON-ASSERTIVE)")
        print("-" * 70)

        for script in extended_scripts:
            start = time.time()
            success, stdout, stderr = run_validation(script)
            elapsed = time.time() - start
            status = "✓ PASS" if success else "✗ FAIL"
            print(f"{status} | {script.name:<45} | {elapsed:.2f}s")

        print("\nNOTE: Extended diagnostics do NOT affect validation status.")

    # --------------------------------------------------
    # Final summary
    # --------------------------------------------------
    print()
    print("=" * 70)
    if results["fail"] == 0:
        print("ALL VALIDATIONS PASSED ✓")
    else:
        print(f"WARNING: {results['fail']} validation(s) failed")
    print("=" * 70)

    return 0 if results["fail"] == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
