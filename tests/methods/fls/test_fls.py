import pytest
import numpy as np
from ctfr.methods import fls_from_specs
from ctfr.warning import ArgumentChangeWarning
from tests.utils.base import BaseTestParameterValidation

class TestParameterValidationFls(BaseTestParameterValidation):
    def test_correct_arguments(self):
        assert np.allclose(fls_from_specs(self.X), self.X)
        assert np.allclose(fls_from_specs(self.X, lk = 11), self.X)
        assert np.allclose(fls_from_specs(self.X, lk = 11, lm = 31), self.X)
        assert np.allclose(fls_from_specs(self.X, lk = 11, lm = 31, gamma = 20), self.X)

    def test_invalid_arguments(self):
        with pytest.raises(TypeError):
            fls_from_specs(self.X, _invalid_argument = 5)

    def test_incorrect_arguments(self):
        with pytest.raises(ValueError):
            fls_from_specs(self.X, lk = "string")
        with pytest.raises(ValueError):
            fls_from_specs(self.X, lm = "string")
        with pytest.raises(ValueError):
            fls_from_specs(self.X, gamma = "string")

    def test_parameter_changes(self):
        with pytest.warns(ArgumentChangeWarning):
            fls_from_specs(self.X, lk = -5)
        with pytest.warns(ArgumentChangeWarning):
            fls_from_specs(self.X, lk = 12)
        with pytest.warns(ArgumentChangeWarning):
            fls_from_specs(self.X, lm = -5)
        with pytest.warns(ArgumentChangeWarning):
            fls_from_specs(self.X, lm = 12)
        with pytest.warns(ArgumentChangeWarning):
            fls_from_specs(self.X, gamma = -5.0)