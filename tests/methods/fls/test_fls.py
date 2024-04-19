import pytest
import numpy as np
from tfrc import fls_from_specs
from tfrc.warning import ArgumentChangeWarning
from tests.utils.base import BaseTestParameterValidation

class TestParameterValidationFls(BaseTestParameterValidation):
    def test_correct_arguments(self):
        assert np.allclose(fls_from_specs(self.X), self.X)
        assert np.allclose(fls_from_specs(self.X, freq_width = 11), self.X)
        assert np.allclose(fls_from_specs(self.X, freq_width = 11, time_width = 31), self.X)
        assert np.allclose(fls_from_specs(self.X, freq_width = 11, time_width = 31, gamma = 20), self.X)

    def test_invalid_arguments(self):
        with pytest.raises(TypeError):
            fls_from_specs(self.X, _invalid_argument = 5)

    def test_incorrect_arguments(self):
        with pytest.raises(ValueError):
            fls_from_specs(self.X, freq_width = "string")
        with pytest.raises(ValueError):
            fls_from_specs(self.X, time_width = "string")
        with pytest.raises(ValueError):
            fls_from_specs(self.X, gamma = "string")

    def test_parameter_changes(self):
        with pytest.warns(ArgumentChangeWarning):
            fls_from_specs(self.X, freq_width = -5)
        with pytest.warns(ArgumentChangeWarning):
            fls_from_specs(self.X, freq_width = 12)
        with pytest.warns(ArgumentChangeWarning):
            fls_from_specs(self.X, time_width = -5)
        with pytest.warns(ArgumentChangeWarning):
            fls_from_specs(self.X, time_width = 12)
        with pytest.warns(ArgumentChangeWarning):
            fls_from_specs(self.X, gamma = -5.0)