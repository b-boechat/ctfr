from ctfr.exception import CitationNotImplementedError
from ctfr import __version__

def cite():
    """Prints the citation information for the package.

    Raises
    ------
    ctfr.exception.CitationNotImplementedError 
        If the citation for the package is not available.

    See Also
    --------
    cite_method
    """
    raise CitationNotImplementedError("Package citation not available.")

def show_version():
    """Prints the version of the package."""
    print(f"ctfr version: {__version__}")