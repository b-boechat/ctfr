from .methods.methods_utils import _get_method_citation, get_method_name
from .exception import CitationNotImplementedError
from ctfr import __version__

def cite():
    """Prints the citation information for the package.

    Raises
    ------
    ctfr.exception.CitationNotImplementedError 
        If the citation for the package is not available.

    See Also
    --------
    cite_method : Prints the citation information for a combination method.
    """
    raise CitationNotImplementedError("Package citation not available.")

def cite_method(method: str, mode: str = None):
    """Prints the citation information for a combination method.

    Parameters
    ----------
    method : str
        The combination method to get the citation information.
    mode : str, optional
        The mode of the citation, by default None

    Raises
    ------
    ctfr.exception.InvalidCombinationMethodError
        If the combination method is invalid.
    ctfr.exception.CitationNotImplementedError
        If a citation for the method is not available.

    See Also
    --------
    cite : Prints the citation information for the package.
    """
    print(_get_method_citation(method, mode=mode))

def show_version():
    """Prints the version of the package."""
    print(f"ctfr version: {__version__}")