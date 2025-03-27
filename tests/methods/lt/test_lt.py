import pytest
import numpy as np
from ctfr.methods import lt_from_specs
from ctfr.warning import ArgumentChangeWarning
from tests.utils.base import BaseTestParameterValidation

class TestParameterValidationLt(BaseTestParameterValidation):
    def test_correct_arguments(self):
        assert np.allclose(lt_from_specs(self.X), self.X)
        assert np.allclose(lt_from_specs(self.X, lk = 11), self.X)
        assert np.allclose(lt_from_specs(self.X, lk = 11, lm = 31), self.X)
        assert np.allclose(lt_from_specs(self.X, lk = 11, lm = 31, eta = 0.5), self.X)

    def test_invalid_arguments(self):
        with pytest.raises(TypeError):
            lt_from_specs(self.X, _invalid_argument = 5)

    def test_incorrect_arguments(self):
        with pytest.raises(ValueError):
            lt_from_specs(self.X, lk = "string")
        with pytest.raises(ValueError):
            lt_from_specs(self.X, lm = "string")
        with pytest.raises(ValueError):
            lt_from_specs(self.X, eta = "string")

    def test_parameter_changes(self):
        with pytest.warns(ArgumentChangeWarning):
            lt_from_specs(self.X, lk = -5)
        with pytest.warns(ArgumentChangeWarning):
            lt_from_specs(self.X, lk = 12)
        with pytest.warns(ArgumentChangeWarning):
            lt_from_specs(self.X, lm = -5)
        with pytest.warns(ArgumentChangeWarning):
            lt_from_specs(self.X, lm = 12)
        with pytest.warns(ArgumentChangeWarning):
            lt_from_specs(self.X, eta = -0.5)