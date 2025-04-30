import numpy as np
import pytest
from ctfr.utils.private import _get_method_function

# This fixture should be set in the method test file.
@pytest.fixture
def func():
    return None

class BaseMethodTest():
    X = np.zeros((3, 4, 5))

    def test_base_output(self, func):
        result = func(self.X)
        assert result.shape == (4, 5)
        assert result.dtype == np.double
        assert np.allclose(result, 0)

    def test_incorrect_arguments(self, func):
        """Test incorrect argument types/values. Override this in derived classes if the method has parameters."""
        pass

    def test_parameter_changes(self, func):
        """Test parameter value validation. Override this in derived classes if the method has parameters."""
        pass
    