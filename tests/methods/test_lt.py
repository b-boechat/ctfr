import pytest
from ctfr.utils.private import _get_method_function
from .base import BaseMethodTest
from ctfr.warning import ArgumentChangeWarning

@pytest.fixture
def func():
    return _get_method_function("lt")

class TestLt(BaseMethodTest):
    def test_incorrect_arguments(self, func):
        with pytest.raises(ValueError):
            func(self.X, lk="string")
        with pytest.raises(ValueError):
            func(self.X, lm="string")
        with pytest.raises(ValueError):
            func(self.X, eta="string")

    def test_parameter_changes(self, func):
        with pytest.warns(ArgumentChangeWarning):
            func(self.X, lk=20) # lk not odd
        with pytest.warns(ArgumentChangeWarning):
            func(self.X, lm=10) # lm not odd
        with pytest.warns(ArgumentChangeWarning):
            func(self.X, eta=-1) # eta negative 