import pytest
import numpy as np
from tfrc import fls_from_specs, swgm_from_specs, lt_from_specs
from tfrc.warning import ParameterChangeWarning

class TestMethodsParametersValidation:
    X = np.ones((2, 2, 2))

    def test_swgm(self):
        # Correct arguments.
        assert np.allclose(swgm_from_specs(self.X), self.X)
        assert np.allclose(swgm_from_specs(self.X, beta = 0.5), self.X)
        assert np.allclose(swgm_from_specs(self.X, beta = 0.5, max_gamma=20), self.X)

        # Invalid arguments.
        with pytest.raises(TypeError):
            swgm_from_specs(self.X, invalid_argument = 5)

        # Incorrect arguments.
        with pytest.raises(ValueError):
            swgm_from_specs(self.X, beta = "string")  
        with pytest.raises(ValueError):
            swgm_from_specs(self.X, max_gamma = "string")

        # Argument changes.
        with pytest.warns(ParameterChangeWarning):
            swgm_from_specs(self.X, beta = -1.0)
        with pytest.warns(ParameterChangeWarning):
            swgm_from_specs(self.X, max_gamma = 0.5)

    def test_fls(self):
        # Correct arguments.
        assert np.allclose(fls_from_specs(self.X), self.X)
        assert np.allclose(fls_from_specs(self.X, freq_width = 11), self.X)
        assert np.allclose(fls_from_specs(self.X, freq_width = 11, time_width = 31), self.X)
        assert np.allclose(fls_from_specs(self.X, freq_width = 11, time_width = 31, gamma = 20), self.X)

        # Invalid arguments.
        with pytest.raises(TypeError):
            fls_from_specs(self.X, invalid_argument = 5)

        # Incorrect arguments.
        with pytest.raises(ValueError):
            fls_from_specs(self.X, freq_width = "string")
        with pytest.raises(ValueError):
            fls_from_specs(self.X, time_width = "string")
        with pytest.raises(ValueError):
            fls_from_specs(self.X, gamma = "string")

        # Argument changes.
        with pytest.warns(ParameterChangeWarning):
            fls_from_specs(self.X, freq_width = -5)
        with pytest.warns(ParameterChangeWarning):
            fls_from_specs(self.X, freq_width = 12)
        with pytest.warns(ParameterChangeWarning):
            fls_from_specs(self.X, time_width = -5)
        with pytest.warns(ParameterChangeWarning):
            fls_from_specs(self.X, time_width = 12)
        with pytest.warns(ParameterChangeWarning):
            fls_from_specs(self.X, gamma = -5.0)


    def test_lt(self):

        # Correct arguments.
        assert np.allclose(lt_from_specs(self.X), self.X)
        assert np.allclose(lt_from_specs(self.X, freq_width = 11), self.X)
        assert np.allclose(lt_from_specs(self.X, freq_width = 11, time_width = 31), self.X)
        assert np.allclose(lt_from_specs(self.X, freq_width = 11, time_width = 31, eta = 0.5), self.X)

        # Invalid arguments.
        with pytest.raises(TypeError):
            lt_from_specs(self.X, invalid_argument = 5)

        # Incorrect arguments.
        with pytest.raises(ValueError):
            lt_from_specs(self.X, freq_width = "string")
        with pytest.raises(ValueError):
            lt_from_specs(self.X, time_width = "string")
        with pytest.raises(ValueError):
            lt_from_specs(self.X, eta = "string")
        # Argument changes.

        with pytest.warns(ParameterChangeWarning):
            lt_from_specs(self.X, freq_width = -5)
        with pytest.warns(ParameterChangeWarning):
            lt_from_specs(self.X, freq_width = 12)
        with pytest.warns(ParameterChangeWarning):
            lt_from_specs(self.X, time_width = -5)
        with pytest.warns(ParameterChangeWarning):
            lt_from_specs(self.X, time_width = 12)
        with pytest.warns(ParameterChangeWarning):
            lt_from_specs(self.X, eta = -0.5)