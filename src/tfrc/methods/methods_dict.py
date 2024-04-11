from .implementations import _fls_wrapper, _swgm_wrapper, _lt_wrapper

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