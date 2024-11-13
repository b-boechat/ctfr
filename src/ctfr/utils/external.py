import librosa
from librosa.display import specshow as specshow_librosa
import numpy as np
#from librosa.display import specshow

def load(path, *, sr=22050, mono=True, offset=0.0, duration=None, dtype=np.double, res_type="soxr_hq"):
    """Load an audio file as a floating point time series.

    This function is a wrapper for :func:`librosa.load` that changes the default dtype to np.double.
    """
    return librosa.load(path, sr=sr, mono=mono, offset=offset, duration=duration, dtype=dtype, res_type=res_type)

def stft(signal, *, n_fft=2048, hop_length=None, win_length=None, window="hann", center=True, pad_mode="constant"):
    return librosa.stft(signal, n_fft=n_fft, hop_length=hop_length, win_length=win_length, window=window, center=center, pad_mode=pad_mode)

def cqt(signal, **kwargs):
    return librosa.cqt(signal, **kwargs)

def stft_spec(signal, *, n_fft=2048, hop_length=None, win_length=None, window="hann", center=True, dtype=np.double, pad_mode="constant"):
    # Wraps librosa.stft to return the squared magnitude of the STFT. The argument dtype refers to the function output, not the stft dtype (which is complex64 by default).
    return np.square(np.abs(librosa.stft(signal, n_fft=n_fft, hop_length=hop_length, win_length=win_length, window=window, center=center, pad_mode=pad_mode), dtype=dtype))

def cqt_spec(signal, **kwargs):
    return np.square(np.abs(cqt(signal, **kwargs), dtype=np.double))

def specshow(data, **kwargs):
    return specshow_librosa(data, **kwargs)

def power_to_db(S, ref=1.0, amin=1e-10, top_db=80.0):
    return librosa.power_to_db(S, ref=ref, amin=amin, top_db=top_db)

    