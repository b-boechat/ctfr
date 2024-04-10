import pytest
import tfrc

def test_check():
    x, sr = tfrc.load("test/gtr-nylon22.wav")
    tfrc.tfrc(x, "swgm")
    tfrc.tfrc(x, "swgm", "cqt")
