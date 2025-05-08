import pytest
import numpy as np
from ctfr.utils.private import _get_method_function
from .base import BaseMethodTest
from ctfr.warning import ArgumentChangeWarning
from ctfr.exception import ArgumentRequiredError

@pytest.fixture
def func():
    return _get_method_function("sls_i")

@pytest.fixture
def valid_steps():
    return np.array([[1, 1], [1, 1], [1, 1]])

class TestSlsI(BaseMethodTest):
    def test_base_output(self, func, valid_steps):
        # Override base test to include required interp_steps
        result = func(self.X, interp_steps=valid_steps)
        assert result.shape == (4, 5)
        assert result.dtype == np.double
        assert np.allclose(result, 0)

    def test_incorrect_arguments(self, func, valid_steps):
        with pytest.raises(ArgumentRequiredError):
            func(self.X) # missing required interp_steps
        with pytest.raises(ValueError):
            func(self.X, lek="string", interp_steps=valid_steps)
        with pytest.raises(ValueError):
            func(self.X, lsk="string", interp_steps=valid_steps)
        with pytest.raises(ValueError):
            func(self.X, lem="string", interp_steps=valid_steps)
        with pytest.raises(ValueError):
            func(self.X, lsm="string", interp_steps=valid_steps)
        with pytest.raises(ValueError):
            func(self.X, beta="string", interp_steps=valid_steps)
        with pytest.raises(ValueError):
            func(self.X, interp_steps="invalid")
        with pytest.raises(ValueError):
            func(self.X, interp_steps=np.array([[1, 1]])) # wrong shape for interp_steps
        with pytest.raises(ValueError):
            func(self.X, interp_steps=np.array([[1, 1], [1, 1], [1, 1, 1]])) # wrong shape for interp_steps
        with pytest.raises(ValueError):
            func(self.X, interp_steps=np.array([[-1, 1], [1, 1], [1, 1]])) # negative value in interp_steps
            
    def test_parameter_changes(self, func, valid_steps):
        with pytest.warns(ArgumentChangeWarning):
            func(self.X, lek=20, interp_steps=valid_steps) # lek not odd
        with pytest.warns(ArgumentChangeWarning):
            func(self.X, lsk=20, interp_steps=valid_steps) # lsk not odd
        with pytest.warns(ArgumentChangeWarning):
            func(self.X, lem=10, interp_steps=valid_steps) # lem not odd
        with pytest.warns(ArgumentChangeWarning):
            func(self.X, lsm=10, interp_steps=valid_steps) # lsm not odd
        with pytest.warns(ArgumentChangeWarning):
            func(self.X, beta=-1, interp_steps=valid_steps) # beta negative