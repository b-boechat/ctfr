import pytest
from tfrc import load

_samples_dict = {
    "guitarset": {
        "load_params": {
            "path": "tests/data/guitarset_sample/guitarset_sample.wav",
            "sr": 22050,
            "mono": True
        },
    }
}

@pytest.fixture
def load_sample(sample_id):
    return load(**_samples_dict[sample_id]["load_params"])