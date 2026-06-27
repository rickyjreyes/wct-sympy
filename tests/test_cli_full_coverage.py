import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent


def test_full_coverage_cli_generates_reports():
    completed = subprocess.run(
        [sys.executable, "scripts/check_full_coverage.py"],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    assert completed.returncode == 0, completed.stdout + completed.stderr
    assert "registered: 142" in completed.stdout
    assert (ROOT / "tables" / "wct_full_coverage.csv").exists()
    assert (ROOT / "tables" / "wct_full_coverage.json").exists()
    assert (ROOT / "COVERAGE_MATRIX.md").exists()
