import numpy as np
from .exception import InvalidRepresentationType
from .utils import stft_spec, cqt_spec
from .methods import _get_method_function

def tfrc(
    method,
    signal,
    representation_type = "stft",
    win_length_list = None,
    hop_length = None,
    n_fft = None,
    filter_scale_list = None,
    bins_per_octave = None,
    minimum_frequency = None,
    num_bins = None,
    **kwargs
):

    if representation_type == "stft":
        params = _set_stft_params(
            win_length_list = win_length_list, 
            hop_length = hop_length, 
            n_fft = n_fft
        )
        return _tfrc_from_stfts(
            method = method,
            signal = signal,
            **params,
            **kwargs
        )

    if representation_type == "cqt":
        return _tfrc_from_cqts(
            method = method,
            signal = signal,
            filter_scale = filter_scale_list,
            bins_per_octave = bins_per_octave,
            minimum_frequency = minimum_frequency,
            num_bins = num_bins,
            hop_length = hop_length,
            **kwargs
        )

    raise InvalidRepresentationType(f"Invalid value for parameter 'representation_type': {representation_type}")


def _tfrc_from_stfts(
    method,
    signal,
    win_length_list,
    hop_length,
    n_fft,
    **kwargs
):
    print(locals())
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
    comb_spec = _get_method_function(method)(signal, **kwargs)
    _normalize_spec(comb_spec, signal_energy)
    return comb_spec


def _tfrc_from_cqts(
    method,
    signal,
    filter_scales,
    bins_per_octave,
    minimum_frequency,
    num_bins,
    hop_length,
    **kwargs
):
    pass

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


def _normalize_specs_tensor(specs_tensor, signal_energy):
    # TODO better normalization.
    specs_tensor *= signal_energy / np.sum(specs_tensor, axis=(1, 2), keepdims=True)

def _get_signal_energy(signal):
    return np.sum(np.square(signal))

def _normalize_spec(spec, signal_energy):
    # TODO better normalization.
    spec *= signal_energy / np.sum(spec)