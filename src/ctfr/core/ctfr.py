import numpy as np
from ctfr.exception import InvalidRepresentationTypeError, InvalidSpecError
from ctfr.utils.external import stft_spec, cqt_spec
from ctfr.utils.internal import _normalize_spec, _normalize_specs_tensor, _get_specs_tensor_energy_array, _round_to_power_of_two
from ctfr.methods.methods_utils import _get_method_function
from typing import List, Optional, Any

def ctfr(
    signal: np.ndarray,
    sr: float,
    method: str,
    *,
    representation_type: str = "stft",
    win_length_list: Optional[List[int]] = None,
    hop_length: Optional[int] = None,
    n_fft: Optional[int] = None,
    filter_scale_list: Optional[List[float]] = None,
    bins_per_octave: Optional[int] = None,
    fmin: Optional[float] = None,
    n_bins: Optional[int] = None,
    **kwargs: Any
) -> np.ndarray:


    if representation_type == "stft":
        params = _get_stft_params(
            sr = sr,
            win_length_list = win_length_list, 
            hop_length = hop_length, 
            n_fft = n_fft
        )
        return _ctfr_stfts(
            signal = signal,
            method = method,
            **params,
            **kwargs
        )

    if representation_type == "cqt":
        params = _get_cqt_params(
            sr = sr,
            filter_scale_list = filter_scale_list,
            bins_per_octave = bins_per_octave,
            fmin = fmin,
            n_bins = n_bins,
            hop_length = hop_length
        )
        return _ctfr_cqts(
            signal = signal,
            method = method,
            **params,
            **kwargs
        )

    raise InvalidRepresentationTypeError(f"Invalid value for parameter 'representation_type': {representation_type}")

def ctfr_from_specs(
    specs: tuple[np.ndarray],
    method: str,
    *,
    normalize_input: bool = True,
    input_energy: float = None,
    normalize_output: bool = True,
    **kwargs: Any
) -> np.ndarray:

    validate_specs(specs)

    # np.ascontiguous array is not strictly needed here, as validate_specs already converts the input arrays to C-contiguous and this is preserved by np.stack.
    specs_tensor = np.ascontiguousarray(np.stack(specs, axis=0)).astype(np.double)

    if (normalize_input or normalize_output) and input_energy is None:
        input_energy = np.mean(_get_specs_tensor_energy_array(specs_tensor))

    if normalize_input: 
        _normalize_specs_tensor(specs_tensor, input_energy)

    comb_spec = _get_method_function(method)(specs_tensor, **kwargs)

    if normalize_output:
        _normalize_spec(comb_spec, input_energy)

    return comb_spec


# =============================================================================

def _ctfr_stfts(
    signal,
    method,
    win_length_list,
    hop_length,
    n_fft,
    **kwargs
):

    specs_tensor = np.array(
        [
            stft_spec(
                signal, 
                n_fft = n_fft,
                hop_length = hop_length,
                win_length = win_length,
                center = True
            )
            for win_length in win_length_list
        ]
    )
    input_energy = np.mean(_get_specs_tensor_energy_array(specs_tensor))
    _normalize_specs_tensor(specs_tensor, input_energy)
    comb_spec = _get_method_function(method)(specs_tensor, **kwargs)
    _normalize_spec(comb_spec, input_energy)
    return comb_spec

def _ctfr_cqts(
    signal,
    method,
    filter_scale_list,
    bins_per_octave,
    fmin,
    n_bins,
    hop_length,
    **kwargs
):
    specs_tensor = np.array(
        [
            cqt_spec(
                signal,
                filter_scale = filter_scale,
                bins_per_octave = bins_per_octave,
                fmin = fmin,
                n_bins = n_bins,
                hop_length = hop_length
            )
            for filter_scale in filter_scale_list
        ]
    )
    input_energy = np.mean(_get_specs_tensor_energy_array(specs_tensor))
    _normalize_specs_tensor(specs_tensor, input_energy)
    comb_spec = _get_method_function(method)(specs_tensor, **kwargs)
    _normalize_spec(comb_spec, input_energy)
    return comb_spec

def _get_stft_params(sr, win_length_list, hop_length, n_fft):
    if win_length_list is None:
        # Default middle window length is 50ms seconds in samples, rounded to the nearest power of 2.
        # For sr = 22050, this is 1024 samples.
        # For sr = 44100, this is 2048 samples.
        middle_length =  _round_to_power_of_two(int(sr * 0.05), mode="round")
        win_length_list = [middle_length // 2, middle_length, middle_length * 2]

    else:
        win_length_list = sorted(win_length_list)

    if hop_length is None:
        hop_length = win_length_list[0] // 2

    if n_fft is None:
        n_fft = win_length_list[-1]

    return {
        "win_length_list": win_length_list,
        "hop_length": hop_length,
        "n_fft": n_fft,
    }

def _get_cqt_params(sr, filter_scale_list, bins_per_octave, fmin, n_bins, hop_length):
    if filter_scale_list is None:
        filter_scale_list = [1/3, 2/3, 1]
    else:
        filter_scale_list = sorted(filter_scale_list)
    
    if bins_per_octave is None:
        bins_per_octave = 36

    if fmin is None:
        fmin = 32.7

    if n_bins is None:
        n_bins = bins_per_octave * 8

    if hop_length is None:
        hop_length = _round_to_power_of_two(int(sr * 0.05), mode="round") // 4
    
    return {
        "filter_scale_list": filter_scale_list,
        "bins_per_octave": bins_per_octave,
        "fmin": fmin,
        "n_bins": n_bins,
        "hop_length": hop_length
    }

def validate_specs(specs):
    try:
        specs = tuple(np.ascontiguousarray(spec) for spec in specs)
    except Exception:
        raise InvalidSpecError("Invalid specs: all specs must be convertible to numpy arrays.")

    if not all([spec.ndim == 2 for spec in specs]):
        raise InvalidSpecError("Invalid specs: all specs must have 2 dimensions.")

    if not len(set([spec.shape for spec in specs])) == 1:
        raise InvalidSpecError("Invalid specs: all specs must have the same shape.")

    return specs