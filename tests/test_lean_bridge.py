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


def test_todo_and_definitions_are_not_counted_as_proved():
    _, mappings = load_lean_map()
    report = lean_coverage_summary(mappings)
    assert report["todo_mapping_count"] >= 1
    assert report["definition_mapping_count"] >= 1
    assert (
        report["proved_mapping_count"]
        + report["definition_mapping_count"]
        + report["todo_mapping_count"]
        == report["mapping_count"]
    )


def test_numeric_koide_claim_has_domain_only_caveat():
    _, mappings = load_lean_map()
    koide = next(item for item in mappings if item.sympy_id == "K1")
    assert koide.relationship == "domain_safety_only"
    assert "does not prove" in koide.caveat.lower()


def test_cosmology_definitions_are_not_reported_as_proofs():
    _, mappings = load_lean_map()
    by_id = {item.sympy_id: item for item in mappings}
    for object_id in ("CM12", "CM13", "CM16"):
        assert by_id[object_id].lean_status == "definition"
        assert by_id[object_id].relationship == "definition_only"


def test_new_canonical_reductions_have_narrow_explicit_scope():
    _, mappings = load_lean_map()
    by_id = {item.sympy_id: item for item in mappings}
    expected = {
        "E15": "complex Fourier coefficients",
        "CLE6": "toroidal PDE",
        "CLE7": "angular ODE",
    }
    for object_id, limitation in expected.items():
        item = by_id[object_id]
        assert item.registry == "full"
        assert item.lean_status == "proved"
        assert item.relationship == "supporting_lemma_only"
        assert item.lean_source == "WCTLean/Models/NarrowCanonicalCoverage.lean"
        assert item.lean_declarations
        assert limitation in item.caveat


def test_recent_canonical_closures_are_mapped_with_proof_scope():
    _, mappings = load_lean_map()
    by_id = {item.sympy_id: item for item in mappings if item.registry == "full"}
    required = {
        "TOP6": "top6_statistic_scales_inverse_square",
        "CM3": "cm3_potential_poisson_relation",
        "CM4": "cm4_decay_iff_nonpositive_logarithmic_rate",
        "CM10": "cm10_drag_contracts_difference",
        "CM15": "cm15_cm20_compatible_iff_energy_loss",
        "CM20": "cm15_cm20_compatible_iff_energy_loss",
        "E44": "e44_phase_rotated_eigenvalue_obstruction",
        "E60": "e60_real_stationary_iff",
        "E82": "e82_information_gram_quadratic_nonnegative",
    }
    for object_id, proof in required.items():
        item = by_id[object_id]
        assert item.lean_status == "proved"
        assert item.relationship == "supporting_lemma_only"
        assert item.lean_source == "WCTLean/Models/RegistryOnlyClosures.lean"
        assert proof in item.lean_declarations
        assert item.caveat and len(item.caveat) >= 30
        assert any(
            qualifier in item.caveat.lower()
            for qualifier in ("only", "not", "does not", "no ", "remains", "rather than")
        )
    assert len(by_id) == 92
