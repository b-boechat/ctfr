from ctfr.exception import (
    InvalidCombinationMethodError,
    CitationNotImplementedError, 
    InvalidCitationModeError
)
from .methods_dict import _methods_dict
from ctfr.warning import DoiNotAvailableWarning
from warnings import warn

def show_methods():
    """Prints information for all installed combination methods.
    
    See Also
    --------
    get_methods_list : Instead of printing, returns a list of combination methods' keys.
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
    show_methods : Instead of returning, prints information for all installed combination methods.
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

def _get_method_function(key):
    try:
        return _methods_dict[key]["function"]
    except KeyError:
        raise InvalidCombinationMethodError(f"Invalid combination method: {key}")

def _get_method_citation(method, mode):
    try:
        entry = _methods_dict[method]
    except KeyError:
        raise InvalidCombinationMethodError(f"Invalid combination method: {method}")

    if mode is None or mode == "doi":
        try:
            return entry["doi"]
        except KeyError:
            if mode == "doi":
                warn(DoiNotAvailableWarning(f"DOI not available for method '{entry['name']}'. Trying citation instead."))
            mode = "citation"
    
    if mode == "citation":
        try:
            citation = entry["citation"]
            if citation is None:
                return f"No citation available for method '{entry['name']}'."
            else:
                return citation
        except KeyError:
            raise CitationNotImplementedError(f"Citation for method '{method}' not implemented")

    raise InvalidCitationModeError(f"Invalid citation mode: {mode}")
