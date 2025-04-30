import pytest
from ctfr.utils.private import _get_method_function
from .base import BaseMethodTest
from ctfr.warning import ArgumentChangeWarning

@pytest.fixture
def func():
    return _get_method_function("sls_h")

class TestSlsH(BaseMethodTest):
    def test_incorrect_arguments(self, func):
        with pytest.raises(ValueError):
            func(self.X, lek="string")
        with pytest.raises(ValueError):
            func(self.X, lsk="string")
        with pytest.raises(ValueError):
            func(self.X, lem="string")
        with pytest.raises(ValueError):
            func(self.X, lsm="string")
        with pytest.raises(ValueError):
            func(self.X, beta="string")
        with pytest.raises(ValueError):
            func(self.X, energy_criterium_db="string")

    def test_parameter_changes(self, func):
        with pytest.warns(ArgumentChangeWarning):
            func(self.X, lek=20) # lek not odd
        with pytest.warns(ArgumentChangeWarning):
            func(self.X, lsk=20) # lsk not odd
        with pytest.warns(ArgumentChangeWarning):
            func(self.X, lem=10) # lem not odd
        with pytest.warns(ArgumentChangeWarning):
            func(self.X, lsm=10) # lsm not odd
        with pytest.warns(ArgumentChangeWarning):
            func(self.X, beta=-1) # beta negative 