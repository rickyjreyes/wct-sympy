from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "check_closed_results.py"
SPEC = spec_from_file_location("check_closed_results", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
MODULE = module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def test_closed_results_all_pass() -> None:
    results = MODULE.run_checks()
    assert results
    assert all(results.values()), results
