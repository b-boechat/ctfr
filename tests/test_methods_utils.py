import pytest
from ctfr.utils.methods import (
    show_methods,
    show_method_params,
    cite_method,
    get_methods_list,
    get_method_name
)
from ctfr.exception import InvalidCombinationMethodError
from ctfr.methods_dict import _methods_dict

def test_get_methods_list():
    """Test that get_methods_list returns the correct list of methods."""
    methods = get_methods_list()
    assert set(methods) == set(_methods_dict.keys())
    assert all(isinstance(m, str) for m in methods)

@pytest.mark.parametrize("key,expected_name", [
    ("mean", "Binwise mean"),
    ("swgm", "Sample-weighted geometric mean (SWGM)"),
    ("fls", "Fast local sparsity (FLS)")
])
def test_get_method_name_valid(key, expected_name):
    """Test that get_method_name returns correct names for valid methods."""
    assert get_method_name(key) == expected_name

def test_get_method_name_invalid():
    """Test that get_method_name raises error for invalid method."""
    with pytest.raises(InvalidCombinationMethodError):
        get_method_name("nonexistent_method")

def test_show_methods(capsys):
    """Test that show_methods displays all methods correctly."""
    show_methods()
    captured = capsys.readouterr()
    for key, val in _methods_dict.items():
        assert f"{val['name']} -- {key}" in captured.out

@pytest.mark.parametrize("method", [
    "mean",  # method with no parameters
    "swgm",  # method with parameters
    "fls"    # method with different parameters
])
def test_show_method_params(capsys, method):
    """Test that show_method_params displays parameters correctly."""
    show_method_params(method)
    captured = capsys.readouterr()
    
    if not _methods_dict[method].get("parameters"):
        assert "has no parameters" in captured.out
    else:
        for param in _methods_dict[method]["parameters"]:
            assert param in captured.out

@pytest.mark.parametrize("method", [
    "mean",    # method with single citation
    "gmean",   # method with multiple citations
    "swgm"     # method with different citation
])
def test_cite_method(capsys, method):
    """Test that cite_method displays citations correctly."""
    cite_method(method)
    captured = capsys.readouterr()
    citations = _methods_dict[method]["citations"]
    for citation in citations:
        assert citation in captured.out

def test_show_method_params_invalid():
    """Test that show_method_params raises error for invalid method."""
    with pytest.raises(InvalidCombinationMethodError):
        show_method_params("nonexistent_method")

def test_cite_method_invalid():
    """Test that cite_method raises error for invalid method."""
    with pytest.raises(InvalidCombinationMethodError):
        cite_method("nonexistent_method") 