from tfrc.exception import InvalidCombinationMethodError
from .methods_dict import _methods_dict

def _get_method_function(key):
    try:
        return _methods_dict[key]["function"]
    except KeyError:
        raise InvalidCombinationMethodError(f"Invalid combination method: {key}")

def get_valid_methods():
    return list(_methods_dict.keys())