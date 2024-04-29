from .implementations.swgm_cy import _swgm_wrapper
from .implementations.fls_cy import _fls_wrapper
from .implementations.lt_cy import _lt_wrapper
from .implementations.ls_cy import _ls_wrapper
from .implementations.binwise_np import _mean_wrapper, _median_wrapper, _min_wrapper

_methods_dict = {
    "mean": {
        "name": "Binwise Mean",
        "function": _mean_wrapper,
        "citation": None
    },
    "median": {
        "name": "Binwise Median",
        "function": _median_wrapper,
        "citation": None
    },
    "min": {
        "name": "Binwise Minimum",
        "function": _min_wrapper,
        "citation": None
    },
    "swgm": {
        "name": "Sample Weighted Geometric Mean (SWGM)",
        "function": _swgm_wrapper,
        #"citation": "#TODO"
    },
    "fls": {
        "name": "Fast Local Sparsity (FLS)",
        "function": _fls_wrapper,
        #"citation": "#TODO"
    },
    "lt": {
        "name": "Lukin-Todd (LT)",
        "function": _lt_wrapper,
        #"citation": "#TODO"
    },
    "ls": {
        "name": "Local Sparsity (LS)",
        "function": _ls_wrapper,
        #"citation": "#TODO"
    }
}