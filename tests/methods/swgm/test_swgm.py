import pytest
import numpy as np
from tfrc import swgm_from_specs
from tfrc.warning import ParameterChangeWarning
from tests.utils.base import BaseTestParameterValidation

class TestParameterValidationSwgm(BaseTestParameterValidation):
    def test_correct_arguments(self):
        assert np.allclose(swgm_from_specs(self.X), self.X)
        assert np.allclose(swgm_from_specs(self.X, beta = 0.5), self.X)
        assert np.allclose(swgm_from_specs(self.X, beta = 0.5, max_gamma=20), self.X)

    def test_invalid_arguments(self):
        with pytest.raises(TypeError):
            swgm_from_specs(self.X, _invalid_argument = 5)

    def test_incorrect_arguments(self):
        with pytest.raises(ValueError):
            swgm_from_specs(self.X, beta = "string")  
        with pytest.raises(ValueError):
            swgm_from_specs(self.X, max_gamma = "string")

    def test_parameter_changes(self):
        with pytest.warns(ParameterChangeWarning):
            swgm_from_specs(self.X, beta = -1.0)
        with pytest.warns(ParameterChangeWarning):
            swgm_from_specs(self.X, max_gamma = 0.5)