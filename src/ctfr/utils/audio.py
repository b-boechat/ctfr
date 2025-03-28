import librosa
try:
    from librosa.display import specshow as specshow_librosa
except ImportError:
    _has_display = False
else:
    _has_display = True

import numpy as np

def load(path, *, sr=None, mono=True, offset=0.0, duration=None, dtype=np.double, res_type="soxr_hq"):
    """Loads an audio file as a floating point time series.

    This function is a wrapper for :external:func:`librosa.load`. The default values for ``sr`` and ``dtype`` are changed.
    """
    return librosa.load(path, sr=sr, mono=mono, offset=offset, duration=duration, dtype=dtype, res_type=res_type)

def stft(signal, *, n_fft=2048, hop_length=None, win_length=None, window="hann", center=True, dtype=None, pad_mode="constant", out=None):
    """Computes the short-time Fourier transform (STFT) of a signal.

    This function is a wrapper for :external:func:`librosa.stft`. The default value for ``n_fft`` is changed to match :func:`ctfr.ctfr` for a signal with a sampling rate of 22050 Hz.

    See Also
    --------
    ctfr.stft_spec
    """
    return librosa.stft(signal, n_fft=n_fft, hop_length=hop_length, win_length=win_length, window=window, center=center, dtype=dtype, pad_mode=pad_mode, out=out)

def cqt(signal, *, sr=22050, hop_length=512, fmin=None, n_bins=288, bins_per_octave=36, tuning=0.0, filter_scale=1, norm=1, sparsity=0.01, window="hann", scale=True, pad_mode="constant", res_type="soxr_hq", dtype=None):
    """Computes the constant-Q transform (CQT) of a signal.

    This function is a wrapper for :external:func:`librosa.cqt`. The default values for ``n_bins`` and ``bins_per_octave`` are changed to match :func:`ctfr.ctfr`. 

    See Also
    --------
    ctfr.cqt_spec
    """
    return librosa.cqt(signal, sr=sr, hop_length=hop_length, fmin=fmin, n_bins=n_bins, bins_per_octave=bins_per_octave, tuning=tuning, filter_scale=filter_scale, norm=norm, sparsity=sparsity, window=window, scale=scale, pad_mode=pad_mode, res_type=res_type, dtype=dtype)

def stft_spec(signal, *, n_fft=2048, hop_length=None, win_length=None, window="hann", center=True, pad_mode="constant", dtype=np.double, stft_dtype=None):
    """Computes the squared magnitude of the short-time Fourier transform (STFT) of a signal.

    This function is equivalent to:

    >>> np.square(np.abs(ctfr.stft(signal, ...), dtype=dtype))

    Notes
    -----
    The `dtype` parameter refers to the data type of the output array. In order to pass a data type to :func:`stft`, use the `stft_dtype` parameter.

    Unlike :func:`stft`, this function does not include an `out` parameter and always returns a new array.

    See Also
    --------
    ctfr.stft
    """
    return np.square(np.abs(stft(signal, n_fft=n_fft, hop_length=hop_length, win_length=win_length, window=window, center=center, dtype=stft_dtype, pad_mode=pad_mode, out=None), dtype=dtype))

def cqt_spec(signal, *, sr=22050, hop_length=512, fmin=None, n_bins=288, bins_per_octave=36, tuning=0.0, filter_scale=1, norm=1, sparsity=0.01, window="hann", scale=True, pad_mode="constant", res_type="soxr_hq", dtype=np.double, cqt_dtype=None):
    """Computes the squared magnitude of the constant-Q transform (CQT) of a signal.

    This function is equivalent to:

    >>> np.square(np.abs(ctfr.cqt(signal, ...), dtype=dtype))

    Notes
    -----
    The `dtype` parameter refers to the data type of the output array. In order to pass a data type to :func:`cqt`, use the `cqt_dtype` parameter.

    See Also
    --------
    ctfr.cqt
    """
    return np.square(np.abs(cqt(signal, sr=sr, hop_length=hop_length, fmin=fmin, n_bins=n_bins, bins_per_octave=bins_per_octave, tuning=tuning, filter_scale=filter_scale, norm=norm, sparsity=sparsity, window=window, scale=scale, pad_mode=pad_mode, res_type=res_type, dtype=cqt_dtype), dtype=dtype))

def specshow(data, *, x_coords=None, y_coords=None, x_axis=None, y_axis=None, sr=22050, hop_length=512, n_fft=None, win_length=None, fmin=None, fmax=None, tempo_min=16, tempo_max=480, tuning=0.0, bins_per_octave=12, key="C:maj", Sa=None, mela=None, thaat=None, auto_aspect=True, htk=False, unicode=True, intervals=None, unison=None, ax=None, **kwargs):
    """Displays a spectrogram, chromagram or similar plot.
    
    This function is a wrapper for :external:func:`librosa.display.specshow`.

    Notes
    -----
    This function is not installed with `ctfr` by default. To use it, you must install ``ctfr`` with the ``[display]`` extra. See :doc:`/getting_started/installation` for more information.
    """
    if not _has_display:
        raise ImportError("Matplotlib is not available. Please reinstall ctfr with the 'display' extra by running:\n\npip install ctfr[display]")
    return specshow_librosa(data, x_coords=x_coords, y_coords=y_coords, x_axis=x_axis, y_axis=y_axis, sr=sr, hop_length=hop_length, n_fft=n_fft, win_length=win_length, fmin=fmin, fmax=fmax, tempo_min=tempo_min, tempo_max=tempo_max, tuning=tuning, bins_per_octave=bins_per_octave, key=key, Sa=Sa, mela=mela, thaat=thaat, auto_aspect=auto_aspect, htk=htk, unicode=unicode, intervals=intervals, unison=unison, ax=ax, **kwargs)

def power_to_db(S, ref=1.0, amin=1e-10, top_db=80.0):
    """Converts a power spectrogram (amplitude squared) to decibel (dB) units.
    
    This function is a wrapper for :external:func:`librosa.power_to_db`.
    """
    return librosa.power_to_db(S, ref=ref, amin=amin, top_db=top_db)

    