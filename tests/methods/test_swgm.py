import pytest
from .base import BaseMethodTest
from ctfr.utils.private import _get_method_function
from ctfr.warning import ArgumentChangeWarning

@pytest.fixture
def func():
    return _get_method_function("swgm")

class TestSwgm(BaseMethodTest):

    def test_incorrect_arguments(self, func):
        with pytest.raises(ValueError):
            func(self.X, beta = "string")  
        with pytest.raises(ValueError):
            func(self.X, max_gamma = "string")

    def test_parameter_changes(self, func):
        with pytest.warns(ArgumentChangeWarning):
            func(self.X, beta = -1.0)
        with pytest.warns(ArgumentChangeWarning):
            func(self.X, max_gamma = 0.5)