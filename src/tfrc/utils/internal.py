import numpy as np

def _normalize_specs_tensor(specs_tensor, signal_energy):
    # TODO better normalization.
    specs_tensor = specs_tensor * signal_energy / _get_specs_tensor_energy_array(specs_tensor)

def _get_signal_energy(signal):
    return np.sum(np.square(signal))

def _get_spec_energy(spec):
    return np.sum(spec)

def _get_specs_tensor_energy_array(specs_tensor):
    return np.sum(specs_tensor, axis=(1, 2), keepdims=True)

def _normalize_spec(spec, signal_energy):
    # TODO better normalization.
    spec = spec * signal_energy / np.sum(spec)

def _round_to_power_of_two(number, mode):
    if mode == "ceil":
        return 2 ** np.ceil(np.log2(number))
    elif mode == "floor":
        return 2 ** np.floor(np.log2(number))
    elif mode == "round":
        return 2 ** np.round(np.log2(number))
    else:
        raise ValueError(f"Invalid mode: {mode}")