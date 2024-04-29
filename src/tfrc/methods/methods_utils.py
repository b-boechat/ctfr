from tfrc.exception import InvalidCombinationMethodError
from .methods_dict import _methods_dict
from tfrc.exception import CitationNotImplementedError

def _get_method_function(key):
    try:
        return _methods_dict[key]["function"]
    except KeyError:
        raise InvalidCombinationMethodError(f"Invalid combination method: {key}")

def _get_method_citation(method):
    try:
        citation = _methods_dict[method]["citation"]
        if citation is None:
            return f"No citation available for method '{_methods_dict[method]['name']}'."
        else:
            return citation
    except KeyError:
        raise CitationNotImplementedError(f"Citation for method '{method}' not implemented")

def get_method_name(key):
    try:
        return _methods_dict[key]["name"]
    except KeyError:
        raise InvalidCombinationMethodError(f"Invalid combination method: {key}")

def get_methods():
    return list(_methods_dict.keys())

def list_methods():
    print("Listing installed methods:", end="\n\n")
    for key, val in _methods_dict.items():
        print(f"- {val['name']} -- {key}")

def validate_method(method):
    try:
        func = _get_method_function(method)
    except InvalidCombinationMethodError:
        print(f"Method not installed: {method}")
        return False
    # finish writing validation.
    # starting _, ending with _to_specs, name clashes, parameter clashes, first parameter specs etc.
    return True
