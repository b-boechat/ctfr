import pytest
from ctfr.utils.private import _get_method_function
from .base import BaseMethodTest

@pytest.fixture
def func():
    return _get_method_function("hmean")

class TestHmean(BaseMethodTest):
    pass # inherits all tests from base class 