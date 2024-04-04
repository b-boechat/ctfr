import librosa

def load(**kwargs):
    return librosa.load(**kwargs)

def stft(**kwargs):
    return librosa.stft(**kwargs)

def cqt(**kwargs):
    return librosa.cqt(**kwargs)