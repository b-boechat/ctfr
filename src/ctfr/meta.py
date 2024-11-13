from .methods.methods_utils import _get_method_citation, get_method_name
from .exception import CitationNotImplementedError
from ctfr import __version__

def cite():
    """Prints the citation information for the package.

    :raises ctfr.exception.CitationNotImplementedError: If the citation for the package is not available.
    """
    raise CitationNotImplementedError("Package citation not available.")

def cite_method(method, mode=None):
    """Prints the citation information for a combination method.

    :param method: The combination method to get the citation information.
    :type method: str
    :raises ctfr.exception.InvalidCombinationMethodError: If the combination method is invalid.
    :raises ctfr.exception.CitationNotImplementedError: If a citation for the method is not available.
    """
    print(_get_method_citation(method, mode=mode))

def show_version():
    """Prints the version of the package."""
    print(f"ctfr version: {__version__}")