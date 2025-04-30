import pytest
from ctfr.utils.private import _get_method_function
from .base import BaseMethodTest
from ctfr.warning import ArgumentChangeWarning

@pytest.fixture
def func():
    return _get_method_function("fls")

class TestFls(BaseMethodTest):
    def test_incorrect_arguments(self, func):
        with pytest.raises(ValueError):
            func(self.X, lk="string")
        with pytest.raises(ValueError):
            func(self.X, lm="string")
        with pytest.raises(ValueError):
            func(self.X, gamma="string")

    def test_parameter_changes(self, func):
        with pytest.warns(ArgumentChangeWarning):
            func(self.X, lk=20) # lk not odd
        with pytest.warns(ArgumentChangeWarning):
            func(self.X, lm=10) # lm not odd
        with pytest.warns(ArgumentChangeWarning):
            func(self.X, gamma=-1) # gamma negative 