"""Public checker registry assembled from the full audit modules."""

from .full_checks_core import *  # noqa: F401,F403
from .full_checks_geometry import *  # noqa: F401,F403
from .full_checks_analysis import *  # noqa: F401,F403
from .full_checks_mid_a import *  # noqa: F401,F403
from .full_checks_mid_b import *  # noqa: F401,F403
from .full_checks_tail import *  # noqa: F401,F403
from .full_checks_resolved import *  # noqa: F401,F403
from .full_checks_derived import (
    check_bandpass_gradient_flow,
    check_cm9_first_order_equivalence,
    check_cm11_gaussian_damping,
    check_effective_wavenumber_chain_derived,
    check_green_kernel_bounded,
    check_lyapunov_gradient_flow,
    check_phase_flux_from_polar_field,
)
from .full_checks_derived_two import (
    check_flat_product_torus_laplacian_derived,
    check_modal_growth_bound_derived,
    check_topology_gradient_flow_descent_derived,
    check_torus_lowest_mode_selection_derived,
)
from .full_checks_derived_three import (
    check_alpha_drop_counting_bound_derived,
    check_gap_mass_consistency_constraint,
    check_phase_coherence_lower_gradient_bound_derived,
    check_subexponential_exploration_margin_derived,
    check_topology_curvature_energy_mass_constraint,
)
from .full_checks_derived_four import check_mean_amplitude_closure_error_bound_v2
from .full_checks_constraints import (
    check_effective_metric_reality_constraint,
    check_localized_energy_concentration_constraint,
)

CHECKERS = {
    name: obj
    for name, obj in list(globals().items())
    if callable(obj) and (name.startswith("check_") or name.startswith("classify_"))
}