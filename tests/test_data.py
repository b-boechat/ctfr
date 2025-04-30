import os
import pytest
from ctfr.utils.data import (
    list_samples,
    fetch_sample,
    _SAMPLES
)
from ctfr.exception import InvalidSampleError

def test_list_samples(capsys):
    """Test that list_samples displays all samples correctly."""
    list_samples()
    captured = capsys.readouterr()
    for key, sample in _SAMPLES.items():
        assert key in captured.out
        assert sample["description"] in captured.out

@pytest.mark.parametrize("sample_key", [
    "synthetic",
    "guitarset"
])
def test_fetch_sample_valid(sample_key):
    """Test that fetch_sample returns valid paths for existing samples."""
    path = fetch_sample(sample_key)
    assert isinstance(path, str)
    assert os.path.exists(path)
    assert os.path.isfile(path)
    assert os.path.basename(path) == _SAMPLES[sample_key]["filename"]

def test_fetch_sample_invalid():
    """Test that fetch_sample raises error for invalid sample."""
    with pytest.raises(InvalidSampleError):
        fetch_sample("nonexistent_sample") 