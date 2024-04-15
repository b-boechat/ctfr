from tfrc.exception import InvalidCombinationMethodError
from .methods_dict import _methods_dict

def _get_method_function(key):
    try:
        return _methods_dict[key]["function"]
    except KeyError:
        raise InvalidCombinationMethodError(f"Invalid combination method: {key}")

def get_methods():
    return list(_methods_dict.keys())

def list_methods():
    print("Listing installed methods:", end="\n\n")
    for key, val in _methods_dict.items():
        print(f"- {val['name']} -- {key}")