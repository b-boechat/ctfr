import numpy as np
from warnings import warn
from ctfr.exception import (
    InvalidCombinationMethodError,
    CitationNotImplementedError,
    InvalidCitationModeError,
)
from ctfr.warning import DoiNotAvailableWarning
from ctfr.methods_dict import _methods_dict

def _normalize_specs_tensor(specs_tensor, target_energy):
    # TODO better normalization.
    specs_tensor = specs_tensor * target_energy / _get_specs_tensor_energy_array(specs_tensor)

def _get_signal_energy(signal):
    return np.sum(np.square(signal))

def _get_spec_energy(spec):
    return np.sum(spec)

def _get_specs_tensor_energy_array(specs_tensor):
    return np.sum(specs_tensor, axis=(1, 2), keepdims=True)

def _normalize_spec(spec, target_energy):
    # TODO better normalization.
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

def _get_method_function(key):
    try:
        return _methods_dict[key]["function"]
    except KeyError:
        raise InvalidCombinationMethodError(f"Invalid combination method: {key}")

def _get_method_citation(method, mode):
    try:
        entry = _methods_dict[method]
    except KeyError:
        raise InvalidCombinationMethodError(f"Invalid combination method: {method}")

    if mode is None or mode == "doi":
        try:
            return entry["doi"]
        except KeyError:
            if mode == "doi":
                warn(DoiNotAvailableWarning(f"DOI not available for method '{entry['name']}'. Trying citation instead."))
            mode = "citation"
    
    if mode == "citation":
        try:
            citation = entry["citation"]
            if citation is None:
                return f"No citation available for method '{entry['name']}'."
            else:
                return citation
        except KeyError:
            raise CitationNotImplementedError(f"Citation for method '{method}' not implemented")

    raise InvalidCitationModeError(f"Invalid citation mode: {mode}")