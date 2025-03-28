from ctfr.exception import (
    InvalidCombinationMethodError,
)
from ctfr.utils.private import _get_method_citations, _get_method_parameters
from ctfr.methods_dict import _methods_dict
from warnings import warn

def show_methods():
    """Prints information for all installed combination methods.
    
    See Also
    --------
    ctfr.get_methods_list
    """
    print("Available combination methods:")
    for key, val in _methods_dict.items():
        print(f"- {val['name']} -- {key}")

def show_method_params(method: str):
    """Prints parameters' information for a combination method.
    
    Parameters
    ----------
    method : str
        The combination method to get the parameter information.
        
    Raises
    ------
    ctfr.exception.InvalidCombinationMethodError
        If the combination method is invalid.
    """
    parameters = _get_method_parameters(method)
    if parameters is None:
        print("Parameter information is not available for this method.")
    elif parameters:
        for key, val in parameters.items():
            print(f"- {key} ({val['type_and_info']}, optional): {val['description']}")
    else:
        print(f"Method '{_methods_dict[method]['name']}' has no parameters.")

def cite_method(method: str):
    """Prints the citation information for a combination method.

    Parameters
    ----------
    method : str
        The combination method to get the citation information.

    Raises
    ------
    ctfr.exception.InvalidCombinationMethodError
        If the combination method is invalid.

    See Also
    --------
    ctfr.cite
    """
    citations = _get_method_citations(method)
    if citations:
        print("\n".join(citations))
    else:
        print(f"No citation available for method '{_methods_dict[method]['name']}'.")

def get_methods_list():
    """Returns a list of all installed combination methods' keys.

    This function can be employed to iterate over installed methods.

    Returns
    -------
    list of str
        A list of all installed combination methods' keys.

    See Also
    --------
    ctfr.show_methods
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
