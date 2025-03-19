import numpy as np
from ctfr.exception import InvalidCombinationMethodError
from ctfr.methods_dict import _methods_dict

def _normalize_specs_tensor(specs_tensor, target_energy):
    specs_tensor = specs_tensor * target_energy / _get_specs_tensor_energy_array(specs_tensor)

def _get_signal_energy(signal):
    return np.sum(np.square(signal))

def _get_spec_energy(spec):
    return np.sum(spec)

def _get_specs_tensor_energy_array(specs_tensor):
    return np.sum(specs_tensor, axis=(1, 2), keepdims=True)

def _normalize_spec(spec, target_energy):
    spec = spec * target_energy / np.sum(spec)

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
    try:
        return _methods_dict[key]
    except KeyError:
        raise InvalidCombinationMethodError(f"Invalid combination method: {key}")


def _get_method_function(key):
    return _get_method_entry(key)["function"]

def _get_method_citations(key):
    return _get_method_entry(key).get("citations", [])

def _get_method_parameters(key):
    return _get_method_entry(key).get("parameters", None)

def _request_tfrs_info(key):
    return _get_method_entry(key).get("request_tfrs_info", False)