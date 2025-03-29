import numpy as np
from ctfr.exception import InvalidRepresentationTypeError
from ctfr.utils.audio import stft_spec, cqt_spec
from .core_utils import (
    _normalize_specs_tensor,
    _get_specs_tensor_energy_array,
    _normalize_spec,
)
from ctfr.utils.private import (
    _round_to_power_of_two, 
    _get_method_function,
    _request_tfrs_info
)
from typing import Any, Iterable

def ctfr(
    signal: np.ndarray,
    sr: float,
    method: str,
    *,
    representation_type: str = "stft",
    win_lengths: Iterable[int] = None,
    hop_length: int = None,
    n_fft: int = None,
    filter_scales: Iterable[float] = None,
    bins_per_octave: int = None,
    fmin: float = None,
    n_bins: int = None,
    **kwargs: Any
) -> np.ndarray:
    """Computes a combined time-frequency representation (CTFR) of a waveform signal.

    A CTFR represents a signal in the time-frequency domain by computing an average (in a generalized sense) of multiple magnitude-squared time-frequency representations (TFRs) of the signal.

    Parameters
    ----------
    signal : np.ndarray [shape=(n)], real-valued
        input signal.
    sr : float
        sampling rate of the input signal.
    method : str
        combination method to use, as specified by their id string. See :ref:`combination methods`. User-defined methods are also supported if they are properly installed (see :ref:`adding methods`). A list of all available methods can also be obtained with :func:`ctfr.show_methods` or :func:`ctfr.get_methods_list`.
    representation_type : {"stft", "cqt"}
        type of time-frequency representation to use, by default `"stft"`.
    win_lengths : Iterable[int], optional
        iterable of window lengths in samples to use for the STFTs. If ``representation_type`` is `"stft"` and this parameter is not provided, the default window lengths are ``[top_length // 4, top_length // 2, top_length]``, where ``top_length`` is either 100ms in samples, rounded to the nearest power of 2, or ``n_fft`` (if provided), whichever is the lowest. If ``representation_type`` is `"cqt"`, this parameter is ignored. 
    hop_length : int > 0, optional
        the hop length in samples to use for the TFRs. If not provided when ``representation_type`` is `"stft"`, defaults to half of the smallest window length. If not provided when ``representation_type`` is `"cqt"`, defaults to 12.5ms in samples, rounded to the nearest power of 2.
    n_fft : int > 0, optional
        number of FFT points to use for the STFTs. If not provided when ``representation_type`` is `"stft"`, defaults to the largest window length. If both ``n_fft`` and ``win_lengths`` are provided, ``n_fft`` must be greater than or equal to the largest window length. If ``representation_type`` is `"cqt"`, this parameter is ignored.
    filter_scales : Iterable[float], values in range: (0, 1], optional
        iterable of filter scales to use for the CQTs. If ``representation_type`` is `"cqt"` and this parameter is not provided, the default filter scales are ``[1/3, 2/3, 1]``. If ``representation_type`` is `"stft"`, this parameter is ignored.
    bins_per_octave : int > 0, optional
        number of bins per octave to use for the CQTs. If ``representation_type`` is `"cqt"` and this parameter is not provided, the default number of bins per octave is 36. If ``representation_type`` is `"stft"`, this parameter is ignored.
    fmin : float > 0, optional
        minimum frequency to use for the CQTs. If ``representation_type`` is `"cqt"` and this parameter is not provided, the default minimum frequency is 32.7 Hz. If ``representation_type`` is `"stft"`, this parameter is ignored.
    n_bins : int > 0, optional
        number of frequency bins to use for the CQTs. If ``representation_type`` is `"cqt"` and this parameter is not provided, the default number of bins is ``bins_per_octave * 8``. If ``representation_type`` is `"stft"`, this parameter is ignored.
    **kwargs
        additional keyword arguments to pass to the combination method function. These are specified in their respective pages in :ref:`combination methods`.

    Returns
    -------
    np.ndarray [shape=(K, M)]
        matrix of dimensions ``K * M`` containing a squared-magnitude CTFR of the input signal, where ``K`` is the number of frequency bins and ``M`` is the number of time frames.

    Raises
    ------
    InvalidRepresentationTypeError
        If the value of provided for ``representation_type`` is invalid.
    InvalidCombinationMethodError
        If the value provided for ``method`` is not the id of an installed combination method.
    :external:class:`ValueError`
        If ``n_fft`` is less than the largest window length.


    See Also
    --------
    ctfr.ctfr_from_specs
    """

    if representation_type == "stft":
        params = _get_stft_params(
            sr = sr,
            win_lengths = win_lengths, 
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
            filter_scales = filter_scales,
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

# =============================================================================

def _ctfr_stfts(
    signal,
    method,
    win_lengths,
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
            for win_length in win_lengths
        ]
    )
    input_energy = np.mean(_get_specs_tensor_energy_array(specs_tensor))
    _normalize_specs_tensor(specs_tensor, input_energy)

    if _request_tfrs_info(method):
        info = {
            "representation_type": "stft",
            "win_lengths": win_lengths,
            "hop_length": hop_length,
            "n_fft": n_fft
        }
        comb_spec = _get_method_function(method)(specs_tensor, _info = info, **kwargs)
    else:
        comb_spec = _get_method_function(method)(specs_tensor, **kwargs)
    _normalize_spec(comb_spec, input_energy)
    return comb_spec

def _ctfr_cqts(
    signal,
    method,
    filter_scales,
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
            for filter_scale in filter_scales
        ]
    )
    input_energy = np.mean(_get_specs_tensor_energy_array(specs_tensor))
    _normalize_specs_tensor(specs_tensor, input_energy)

    if _request_tfrs_info(method):
        info = {
            "representation_type": "cqt",
            "filter_scales": filter_scales,
            "bins_per_octave": bins_per_octave,
            "fmin": fmin,
            "n_bins": n_bins,
            "hop_length": hop_length
        }
        comb_spec = _get_method_function(method)(specs_tensor, _info = info, **kwargs)
    else:
        comb_spec = _get_method_function(method)(specs_tensor, **kwargs)
    _normalize_spec(comb_spec, input_energy)
    return comb_spec

def _get_stft_params(sr, win_lengths, hop_length, n_fft):
    if win_lengths is None:
        # Default middle window length is 50ms seconds in samples, rounded to the nearest power of 2.
        # For sr = 22050, this is 1024 samples.
        # For sr = 44100, this is 2048 samples.
        if n_fft is not None:
            top_length = min(_round_to_power_of_two(int(sr * 0.1), mode="round"), n_fft)
        else:
            top_length =  _round_to_power_of_two(int(sr * 0.1), mode="round")
        win_lengths = [top_length // 4, top_length // 2, top_length]

    else:
        win_lengths = sorted(win_lengths)

    if hop_length is None:
        hop_length = win_lengths[0] // 2

    if n_fft is None:
        n_fft = win_lengths[-1]
    else:
        if n_fft < win_lengths[-1]:
            raise ValueError("n_fft must be greater than or equal to the largest window length.")

    return {
        "win_lengths": win_lengths,
        "hop_length": hop_length,
        "n_fft": n_fft,
    }

def _get_cqt_params(sr, filter_scales, bins_per_octave, fmin, n_bins, hop_length):
    if filter_scales is None:
        filter_scales = [1/3, 2/3, 1]
    else:
        filter_scales = sorted(filter_scales)
    
    if bins_per_octave is None:
        bins_per_octave = 36

    if fmin is None:
        fmin = 32.7

    if n_bins is None:
        n_bins = bins_per_octave * 8

    if hop_length is None:
        hop_length = _round_to_power_of_two(int(sr * 0.0125), mode="round")
    
    return {
        "filter_scales": filter_scales,
        "bins_per_octave": bins_per_octave,
        "fmin": fmin,
        "n_bins": n_bins,
        "hop_length": hop_length
    }