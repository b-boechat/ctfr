import numpy as np
from typing import Any, Iterable
from ctfr.exception import InvalidSpecError
from .core_utils import (
    _normalize_specs_tensor,
    _get_specs_tensor_energy_array,
    _normalize_spec,
)
from ctfr.utils.private import _get_method_function

def ctfr_from_specs(
    specs: Iterable[np.ndarray],
    method: str,
    *,
    normalize_input: bool = True,
    normalize_output: bool = True,
    energy: float = None,
    **kwargs: Any
) -> np.ndarray:
    """Computes a combined time-frequency representation (CTFR) from input spectrograms.

    This function is similar to :func:`ctfr`, but offers more control to the user by allowing them to provide the input spectrograms directly.

    Parameters
    ----------
    specs : Iterable[np.ndarray [shape=(K, M)], values >= 0]
        input spectrograms, assumed to be magnitude-squared time-frequency representations (TFRs) of the same signal and with the same shape and time-frequency alignment.
    method : str
        combination method to use, as specified by their id string. See :ref:`combination methods`. User-defined methods are also supported if they are properly installed (see :ref:`adding methods`). A list of all available methods can also be obtained with :func:`ctfr.show_methods` or :func:`ctfr.get_methods_list`.
    normalize_input : bool, default=True
        whether to normalize the input spectrograms to have the same total energy. This is highly recommended for a quality CTFR, though can be skipped if the input spectrograms are already normalized.
    normalize_output : bool, default=True
        whether to normalize the output CTFR's total energy to match the input energy. This is highly recommended for a quality CTFR, though can be skipped for output testing purposes.
    energy : float, optional
        energy to normalize the input spectrograms to, if ``normalize_input`` is `True`, and the output CTFR to, if ``normalize_output`` is `True`. If not provided, the mean energy of the input spectrograms is used.
    **kwargs
        additional keyword arguments to pass to the combination method function. These are specified in their respective pages in :ref:`combination methods`.

    Returns
    -------
    np.ndarray [shape=(K, M)]
        matrix of dimensions ``K * M`` containing a squared-magnitude CTFR of the input signal, where ``K`` is the number of frequency bins and ``M`` is the number of time frames.

    Raises
    ------
    InvalidCombinationMethodError
        If the value provided for ``method`` is not the id of an installed combination method.

    See Also
    --------
    ctfr.ctfr
    """

    # Stacks the input spectrograms into a contiguous tensor
    specs_tensor = _stack_specs(specs)

    # If not provided and a normalization is requested, sets the energy to the mean energy of the input spectrograms.
    if (normalize_input or normalize_output) and energy is None:
        energy = np.mean(_get_specs_tensor_energy_array(specs_tensor))

    # Normalizes the input spectrograms to have the same total energy, if requested
    if normalize_input: 
        _normalize_specs_tensor(specs_tensor, energy)
    
    # Computes the combined spectrogram using the specified method.
    comb_spec = _get_method_function(method)(specs_tensor, **kwargs)

    # Normalizes the output spectrogram to match the input energy, if requested.
    if normalize_output:
        _normalize_spec(comb_spec, energy)

    return comb_spec

# =============================================================================

def _stack_specs(specs):
    """Stacks the input spectrograms into a contiguous tensor."""
    specs_tensor = np.ascontiguousarray(np.stack(specs, axis=0)).astype(np.double)
    if specs_tensor.ndim != 3:
        raise InvalidSpecError("Input spectrograms must be 2-dimensional.")
    return specs_tensor