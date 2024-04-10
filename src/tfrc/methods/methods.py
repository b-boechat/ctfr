from . import _fls_wrapper, _swgm_wrapper, _lt_wrapper
from tfrc.exception import InvalidCombinationMethod

methods_dict = {
    "swgm": {
        "function": _swgm_wrapper
    },
    "fls": {
        "function": _swgm_wrapper
    },
    "lt": {
        "function": _lt_wrapper
    },
}

def _get_method_function(key):
    try:
        return methods_dict[key]["function"]
    except KeyError:
        raise InvalidCombinationMethod(f"Invalid combination method: {key}")

def get_valid_methods():
    return list(methods_dict.keys())