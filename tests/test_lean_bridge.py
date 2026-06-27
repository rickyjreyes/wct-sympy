from wct_sympy.lean_bridge import lean_coverage_summary, load_lean_map


def test_lean_map_is_valid_and_nonempty():
    metadata, mappings = load_lean_map()
    assert metadata["lean_repository"] == "rickyjreyes/wct-lean"
    assert mappings


def test_sympy_pass_is_not_lean_proof_policy():
    metadata, _ = load_lean_map()
    policy = metadata["policy"]
    assert "never" in policy["prohibition"].lower()
    assert "kernel-checked" in policy["lean_proved_means"]


def test_todo_is_not_counted_as_proved():
    _, mappings = load_lean_map()
    report = lean_coverage_summary(mappings)
    assert report["todo_mapping_count"] >= 1
    assert report["proved_mapping_count"] + report["todo_mapping_count"] == report["mapping_count"]


def test_numeric_koide_claim_has_domain_only_caveat():
    _, mappings = load_lean_map()
    koide = next(item for item in mappings if item.sympy_id == "K1")
    assert koide.relationship == "domain_safety_only"
    assert "does not prove" in koide.caveat.lower()
