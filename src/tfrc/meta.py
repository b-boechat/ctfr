from .methods.methods_utils import _get_method_citation, get_method_name
from .exception import CitationNotImplementedError

def cite():
    raise CitationNotImplementedError("Package citation not implemented")

def cite_method(method, mode=None):
    print(_get_method_citation(method, mode=mode))