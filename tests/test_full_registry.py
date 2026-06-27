from collections import Counter

from wct_sympy.catalog import load_full_registry
from wct_sympy.full_checks import CHECKERS


def test_registry_has_all_canonical_families():
    specs = load_full_registry()
    ids = {spec.equation_id for spec in specs}
    assert {"E1A", "E1B"} <= ids
    assert {f"E{i}" for i in range(2, 83)} <= ids
    assert {f"CLE{i}" for i in range(1, 11)} <= ids
    assert {f"CM{i}" for i in range(1, 21)} <= ids
    assert {"M1", "M2", "M3", "M4", "M5", "M6A", "M6B", "M7", "M8"} <= ids
    assert {"G1", "EX", "EY", "EZ", "FA"} <= ids
    assert len(specs) == 142


def test_every_registry_entry_has_a_checker():
    for spec in load_full_registry():
        assert spec.checker in CHECKERS, (spec.equation_id, spec.checker)


def test_ids_are_unique():
    ids = [spec.equation_id for spec in load_full_registry()]
    counts = Counter(ids)
    assert [equation_id for equation_id, count in counts.items() if count != 1] == []
