import numpy as np

def _normalize_specs_tensor(specs_tensor, target_energy):
    """Normalizes the input spectrograms to have the same total energy."""
    specs_tensor = specs_tensor * target_energy / _get_specs_tensor_energy_array(specs_tensor)

def _get_specs_tensor_energy_array(specs_tensor):
    """Computes the total energy of each spectrogram in the tensor."""
    return np.sum(specs_tensor, axis=(1, 2), keepdims=True)

def _normalize_spec(spec, target_energy):
    """Normalizes spectrogram to the specified total energy."""
    spec = spec * target_energy / np.sum(spec)