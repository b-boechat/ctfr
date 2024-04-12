from .implementations.swgm_cy import _swgm_wrapper
from .implementations.fls_cy import _fls_wrapper
from .implementations.lt_cy import _lt_wrapper

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
}