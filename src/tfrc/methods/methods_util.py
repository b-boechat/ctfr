from tfrc.exception import InvalidCombinationMethod
from .methods_dict import methods_dict

def _get_method_function(key):
    try:
        return methods_dict[key]["function"]
    except KeyError:
        raise InvalidCombinationMethod(f"Invalid combination method: {key}")

def get_valid_methods():
    return list(methods_dict.keys())