import numpy as np

def _normalize_specs_tensor(specs_tensor, signal_energy):
    # TODO better normalization.
    specs_tensor *= signal_energy / np.sum(specs_tensor, axis=(1, 2), keepdims=True)

def _get_signal_energy(signal):
    return np.sum(np.square(signal))

def _normalize_spec(spec, signal_energy):
    # TODO better normalization.
    spec *= signal_energy / np.sum(spec)