from ctfr.exception import (
    InvalidCombinationMethodError,
)
from ctfr.methods_dict import _methods_dict
from warnings import warn

def show_methods():
    """Prints information for all installed combination methods.
    
    See Also
    --------
    get_methods_list
    """
    print("Available combination methods:")
    for key, val in _methods_dict.items():
        print(f"- {val['name']} -- {key}")

def get_methods_list():
    """Returns a list of all installed combination methods' keys.

    This function can be employed to iterate over installed methods.

    Returns
    -------
    list of str
        A list of all installed combination methods' keys.

    See Also
    --------
    show_methods
    """
    return list(_methods_dict.keys())

def get_method_name(key):
    """Returns the name for a given combination method key.

    This function can be useful for displaying and plotting purposes.

    Parameters
    ----------
    key : str
        The key of the combination method.

    Returns
    -------
    str
        The name of the combination method.

    Raises
    ------
    ctfr.exception.InvalidCombinationMethodError
        If the given key is not a valid combination method.
    """
    try:
        return _methods_dict[key]["name"]
    except KeyError:
        raise InvalidCombinationMethodError(f"Invalid combination method: {key}")
