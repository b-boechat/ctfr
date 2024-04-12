from .implementations.swgm_cy import _swgm_wrapper
from .implementations.fls_cy import _fls_wrapper
from .implementations.lt_cy import _lt_wrapper
from .implementations.binwise_np import _mean_wrapper, _median_wrapper, _min_wrapper

_methods_dict = {
    "swgm": {
        "function": _swgm_wrapper
    },
    "fls": {
        "function": _fls_wrapper
    },
    "lt": {
        "function": _lt_wrapper
    },
    "mean": {
        "function": _mean_wrapper
    },
    "median": {
        "function": _median_wrapper
    },
    "min": {
        "function": _min_wrapper
    }
}