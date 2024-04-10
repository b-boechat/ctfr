import librosa
import numpy as np
#from librosa.display import specshow

def load(path, **kwargs):
    return librosa.load(path, **kwargs)

def stft(signal, **kwargs):
    return librosa.stft(signal, **kwargs)

def cqt(signal, **kwargs):
    return librosa.cqt(signal, **kwargs)

def stft_spec(signal, **kwargs):
    return np.square(np.abs(stft(signal, **kwargs), dtype=np.double))

def cqt_spec(signal, **kwargs):
    return np.square(np.abs(cqt(signal, **kwargs), dtype=np.double))

#def specshow(**kwargs):
#    return specshow(**kwargs)