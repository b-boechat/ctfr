import numpy as np
from tfrc.exception import InvalidRepresentationTypeError
from tfrc.utils import stft_spec, cqt_spec, _get_signal_energy, _normalize_spec, _normalize_specs_tensor
from tfrc.methods import _get_method_function
from typing import List, Optional, Any

def tfrc(
    signal: np.ndarray,
    method: str,
    representation_type: str = "stft",
    *,
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
        params = _set_stft_params(
            win_length_list = win_length_list, 
            hop_length = hop_length, 
            n_fft = n_fft
        )
        return _tfrc_stfts(
            signal = signal,
            method = method,
            **params,
            **kwargs
        )

    if representation_type == "cqt":
        params = _set_cqt_params(
            filter_scale_list = filter_scale_list,
            bins_per_octave = bins_per_octave,
            fmin = fmin,
            n_bins = n_bins,
            hop_length = hop_length
        )
        return _tfrc_cqts(
            signal = signal,
            method = method,
            **params,
            **kwargs
        )

    raise InvalidRepresentationTypeError(f"Invalid value for parameter 'representation_type': {representation_type}")

def tfrc_from_specs(
    specs_tensor: np.ndarray,
    method: str,
    target_energy: float = None,
    **kwargs: Any
) -> np.ndarray:

    if target_energy is None:
        target_energy = np.sum(specs_tensor[0])

    _normalize_specs_tensor(specs_tensor, target_energy)
    comb_spec = _get_method_function(method)(specs_tensor, **kwargs)
    _normalize_spec(comb_spec, target_energy)
    return comb_spec


# =============================================================================

def _tfrc_stfts(
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
    signal_energy = _get_signal_energy(signal)
    _normalize_specs_tensor(specs_tensor, signal_energy)
    comb_spec = _get_method_function(method)(specs_tensor, **kwargs)
    _normalize_spec(comb_spec, signal_energy)
    return comb_spec

def _tfrc_cqts(
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
    signal_energy = _get_signal_energy(signal)
    _normalize_specs_tensor(specs_tensor, signal_energy)
    comb_spec = _get_method_function(method)(specs_tensor, **kwargs)
    _normalize_spec(comb_spec, signal_energy)
    return comb_spec

def _set_stft_params(win_length_list, hop_length, n_fft):
    if win_length_list is None:
        win_length_list = [1024, 2048, 4096]
    else: # TODO catch exception.
        win_length_list = sorted(win_length_list)

    if hop_length is None:
        hop_length = int(win_length_list[0]/2)

    if n_fft is None:
        n_fft = win_length_list[-1]

    return {
        "win_length_list": win_length_list,
        "hop_length": hop_length,
        "n_fft": n_fft,
    }

def _set_cqt_params(filter_scale_list, bins_per_octave, fmin, n_bins, hop_length):
    if filter_scale_list is None:
        filter_scale_list = [1/3, 1/2, 1]
    else: # TODO catch exception
        filter_scale_list = sorted(filter_scale_list)
    
    if bins_per_octave is None:
        bins_per_octave = 36

    if fmin is None:
        fmin = 32.7

    if n_bins is None:
        n_bins = bins_per_octave * 8

    if hop_length is None:
        hop_length = 512
    
    return {
        "filter_scale_list": filter_scale_list,
        "bins_per_octave": bins_per_octave,
        "fmin": fmin,
        "n_bins": n_bins,
        "hop_length": hop_length
    }