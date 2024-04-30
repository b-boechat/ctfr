import librosa
from librosa.display import specshow as specshow_librosa
import numpy as np
#from librosa.display import specshow

def load(path, *, sr=22050, mono=True, offset=0.0, duration=None, dtype=np.double, res_type='soxr_hq'):
    return librosa.load(path, sr=sr, mono=mono, offset=offset, duration=duration, dtype=dtype, res_type=res_type)

def stft(signal, *, n_fft=2048, hop_length=None, win_length=None, window='hann', center=True, pad_mode='constant'):
    return librosa.stft(signal, n_fft=n_fft, hop_length=hop_length, win_length=win_length, window=window, center=center, pad_mode=pad_mode)

def cqt(signal, **kwargs):
    return librosa.cqt(signal, **kwargs)

def stft_spec(signal, *, n_fft=2048, hop_length=None, win_length=None, window='hann', center=True, dtype=np.double, pad_mode='constant'):
    # Wraps librosa.stft to return the squared magnitude of the STFT. The argument dtype refers to the function output, not the stft dtype (which is complex64 by default).
    return np.square(np.abs(librosa.stft(signal, n_fft=n_fft, hop_length=hop_length, win_length=win_length, window=window, center=center, pad_mode=pad_mode), dtype=dtype))

def cqt_spec(signal, **kwargs):
    return np.square(np.abs(cqt(signal, **kwargs), dtype=np.double))

# Librosa specshow with added x_lim and y_lim arguments.
def specshow(data, *, x_coords=None, y_coords=None, x_axis=None, y_axis=None, sr=22050, hop_length=512, n_fft=None, win_length=None, fmin=None, fmax=None, tempo_min=16, tempo_max=480, tuning=0.0, bins_per_octave=12, key='C:maj', Sa=None, mela=None, thaat=None, auto_aspect=True, htk=False, unicode=True, intervals=None, unison=None, ax=None, **kwargs):
    return specshow_librosa(data, x_coords=x_coords, y_coords=y_coords, x_axis=x_axis, y_axis=y_axis, sr=sr, hop_length=hop_length, n_fft=n_fft, win_length=win_length, fmin=fmin, fmax=fmax, tempo_min=tempo_min, tempo_max=tempo_max, tuning=tuning, bins_per_octave=bins_per_octave, key=key, Sa=Sa, mela=mela, thaat=thaat, auto_aspect=auto_aspect, htk=htk, unicode=unicode, intervals=intervals, unison=unison, ax=ax, **kwargs)

def power_to_db(S, ref=1.0, amin=1e-10, top_db=80.0):
    return librosa.power_to_db(S, ref=ref, amin=amin, top_db=top_db)

    