import numpy as np
from ctfr.exception import InvalidCombinationMethodError
from ctfr.methods_dict import _methods_dict

def _round_to_power_of_two(number, mode):
    if mode == "ceil":
        return int(2 ** np.ceil(np.log2(number)))
    elif mode == "floor":
        return int(2 ** np.floor(np.log2(number)))
    elif mode == "round":
        return int(2 ** np.round(np.log2(number)))
    else:
        raise ValueError(f"Invalid mode: {mode}")

def _get_method_entry(key):
    """Get the entry in the methods dictionary for a given key."""
    try:
        return _methods_dict[key]
    except KeyError:
        raise InvalidCombinationMethodError(f"Invalid combination method: {key}")

def _get_method_function(key):
    """Get the wrapper function for a given method key.""" 
    return _get_method_entry(key)["function"]

def _get_method_citations(key):
    return _get_method_entry(key).get("citations", [])

def _get_method_parameters(key):
    return _get_method_entry(key).get("parameters", None)

def _request_tfrs_info(key):
    return _get_method_entry(key).get("request_tfrs_info", False)