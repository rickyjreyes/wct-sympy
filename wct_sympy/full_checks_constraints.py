"""Adversarial constraint checks for conditional WCT equations.

These checks deliberately do not promote the associated equations.  They expose
necessary corrections or counter-scaling regimes that any later theorem must
address.
"""

from .full_checks_core import *  # noqa: F401,F403


def check_effective_metric_reality_constraint(spec: EquationSpec) -> AuditResult:
    """E22: the unsymmetrized complex-gradient outer product is not a real metric."""
    ar, ai, br, bi = sp.symbols("a_r a_i b_r b_i", real=True)
    a = ar + sp.I * ai
    b = br + sp.I * bi

    g01 = sp.expand_complex(sp.conjugate(a) * b)
    g10 = sp.expand_complex(sp.conjugate(b) * a)
    hermitian_residual = sp.simplify(sp.conjugate(g01) - g10)
    symmetric_residual = sp.simplify(g01 - g10)

    # Explicit admissible complex derivatives: d_0 psi = 1, d_1 psi = i.
    sample_g01 = sp.simplify(g01.subs({ar: 1, ai: 0, br: 0, bi: 1}))
    sample_g10 = sp.simplify(g10.subs({ar: 1, ai: 0, br: 0, bi: 1}))
    sample_asymmetry = sp.simplify(sample_g01 - sample_g10)

    # The real part is automatically symmetric:
    # Re(conj(a)b) = a_r b_r + a_i b_i = Re(conj(b)a).
    corrected01 = sp.simplify(sp.re(g01))
    corrected10 = sp.simplify(sp.re(g10))
    corrected_residual = sp.simplify(corrected01 - corrected10)

    ok = (
        hermitian_residual == 0
        and sample_g01 == sp.I
        and sample_g10 == -sp.I
        and sample_asymmetry == 2 * sp.I
        and corrected_residual == 0
    )

    return result(
        spec,
        AuditStatus.CONDITIONAL if ok else AuditStatus.FAIL,
        value={
            "g01": g01,
            "g10": g10,
            "hermitian_residual": hermitian_residual,
            "symmetric_residual": symmetric_residual,
            "sample_g01": sample_g01,
            "sample_g10": sample_g10,
            "sample_asymmetry": sample_asymmetry,
            "real_symmetrized_entry": corrected01,
            "real_symmetry_residual": corrected_residual,
        },
        expected=(
            "for complex psi the raw derivative correction is Hermitian but not generally "
            "real symmetric; Re(conj(d_mu psi)d_nu psi) is symmetric"
        ),
        residual=0.0 if ok else None,
        reason=(
            "For complex psi, H_{mu nu}=conj(d_mu psi)d_nu psi satisfies "
            "conj(H_{mu nu})=H_{nu mu}, so it is Hermitian, not generally a real "
            "symmetric tensor.  The explicit derivatives d_0 psi=1 and d_1 psi=i give "
            "H_01=i and H_10=-i.  Replacing this term by its real part (equivalently the "
            "real symmetric part) fixes that obstruction.  E22 still needs coefficient "
            "dimensions plus a nondegeneracy/signature bound, so it remains conditional."
        ),
        assumptions=(
            "psi may be genuinely complex",
            "a spacetime metric is required to be a real symmetric nondegenerate bilinear form",
            "the remaining W_psi conformal correction is real after its own dimensional normalization",
        ),
    )


def check_localized_energy_concentration_constraint(spec: EquationSpec) -> AuditResult:
    """E68: the printed R^(n-2) estimate cannot be uniform on arbitrary H1 in n=3."""
    R, C, G = sp.symbols("R C G", positive=True)
    M = sp.symbols("M", nonnegative=True)

    # In n=3 take u_R(x)=R^(-1/2) phi(x/R), phi supported in B_1.
    # Then support(u_R) subset B_R,
    # ||grad u_R||_2^2 = G and ||u_R||_2^2 = R^2 M.
    local_gradient_energy = G
    h1_norm_sq = G + R**2 * M
    proposed_rhs = sp.simplify(C * R * h1_norm_sq)
    ratio = sp.simplify(local_gradient_energy / proposed_rhs)
    rhs_limit = sp.limit(proposed_rhs, R, 0, dir="+")
    ratio_limit = sp.limit(ratio, R, 0, dir="+")

    ok = rhs_limit == 0 and ratio_limit == sp.oo

    return result(
        spec,
        AuditStatus.CONDITIONAL if ok else AuditStatus.FAIL,
        value={
            "dimension": 3,
            "scaled_local_gradient_energy": local_gradient_energy,
            "scaled_L2_energy": R**2 * M,
            "scaled_H1_norm_squared": h1_norm_sq,
            "proposed_rhs": proposed_rhs,
            "rhs_limit_R_to_zero": rhs_limit,
            "lhs_over_rhs_limit_R_to_zero": ratio_limit,
        },
        expected=(
            "the universal n=3 estimate fails under H1 concentration; extra scale/domain "
            "hypotheses are necessary"
        ),
        residual=0.0 if ok else None,
        reason=(
            "Choose a nonconstant compactly supported phi in B_1 and set "
            "u_R(x)=R^(-1/2)phi(x/R) in three dimensions.  Its entire gradient energy "
            "lies in B_R and remains G>0, while ||u_R||_H1^2=G+R^2 M.  The proposed "
            "right side is C R(G+R^2 M), which tends to zero for fixed C.  Therefore no "
            "R-independent constant can make the printed E68 inequality hold for all H1 "
            "fields in n=3.  A restricted scaling class or a different local estimate is required."
        ),
        assumptions=(
            "the claimed constant C is independent of the localization radius R",
            "the estimate is intended to apply to arbitrary H1 fields in dimension three",
            "a nonconstant smooth compactly supported profile phi in B_1 is admissible",
        ),
    )
