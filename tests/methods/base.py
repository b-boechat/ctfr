import numpy as np

class BaseTestParameterValidation:
    X = np.ones((2, 2, 2))

    def test_correct_arguments(self):
        assert False

    def test_invalid_arguments(self):
        assert False
    
    def test_incorrect_arguments(self):
        assert False

    def test_parameter_changes(self):
        assert False