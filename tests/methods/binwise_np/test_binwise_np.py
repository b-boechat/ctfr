import pytest
import numpy as np
from ctfr.methods import mean_from_specs, hmean_from_specs, gmean_from_specs, min_from_specs
from tests.utils.base import BaseTestParameterValidation

class TestParameterValidationMean(BaseTestParameterValidation):
    def test_correct_arguments(self):
        assert np.allclose(mean_from_specs(self.X), self.X)

    def test_invalid_arguments(self):
        with pytest.raises(TypeError):
            mean_from_specs(self.X, _invalid_argument = 5)

    def test_incorrect_arguments(self):
        assert True

    def test_parameter_changes(self):
        assert True


class TestParameterValidationHmean(BaseTestParameterValidation):
    def test_correct_arguments(self):
        assert np.allclose(hmean_from_specs(self.X), self.X)

    def test_invalid_arguments(self):
        with pytest.raises(TypeError):
            hmean_from_specs(self.X, _invalid_argument = 5)

    def test_incorrect_arguments(self):
        assert True

    def test_parameter_changes(self):
        assert True

class TestParameterValidationGmean(BaseTestParameterValidation):
    def test_correct_arguments(self):
        assert np.allclose(gmean_from_specs(self.X), self.X)

    def test_invalid_arguments(self):
        with pytest.raises(TypeError):
            gmean_from_specs(self.X, _invalid_argument = 5)

    def test_incorrect_arguments(self):
        assert True

    def test_parameter_changes(self):
        assert True

class TestParameterValidationMin(BaseTestParameterValidation):
    def test_correct_arguments(self):
        assert np.allclose(min_from_specs(self.X), self.X)

    def test_invalid_arguments(self):
        with pytest.raises(TypeError):
            min_from_specs(self.X, _invalid_argument = 5)

    def test_incorrect_arguments(self):
        assert True

    def test_parameter_changes(self):
        assert True