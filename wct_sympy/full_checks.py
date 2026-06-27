"""Public checker registry assembled from the full audit modules."""

from .full_checks_core import *  # noqa: F401,F403
from .full_checks_geometry import *  # noqa: F401,F403
from .full_checks_analysis import *  # noqa: F401,F403
from .full_checks_mid_a import *  # noqa: F401,F403
from .full_checks_mid_b import *  # noqa: F401,F403
from .full_checks_tail import *  # noqa: F401,F403

CHECKERS = {
    name: obj
    for name, obj in list(globals().items())
    if callable(obj) and (name.startswith("check_") or name.startswith("classify_"))
}
