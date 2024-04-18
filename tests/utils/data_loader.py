import pytest
import numpy as np
import json
from tfrc import load

_specs_tensor_samples_dict = {
    "sample_stft_specs": {
        "path": "tests/data/sample_stft_specs.json"
    }
}

def load_sample_specs_tensor(sample_id):
    with open(_specs_tensor_samples_dict[sample_id]) as f:
        return np.array(json.load(f), dtype=np.double)