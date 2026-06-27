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

CHECKERS = {
    name: obj
    for name, obj in list(globals().items())
    if callable(obj) and (name.startswith("check_") or name.startswith("classify_"))
}
