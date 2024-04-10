import librosa
import numpy as np
from librosa.display import specshow

def load(**kwargs):
    return librosa.load(**kwargs)

def stft(**kwargs):
    return librosa.stft(**kwargs)

def cqt(**kwargs):
    return librosa.cqt(**kwargs)

def stft_spec(**kwargs):
    return np.square(np.abs(stft(**kwargs), dtype=np.double))

def cqt_spec(**kwargs):
    return np.square(np.abs(cqt(**kwargs), dtype=np.double))

def specshow(**kwargs):
    return specshow(**kwargs)