__version__ = "0.1.0.dev3"

from warnings import warn as _warn
from .utils.audio import load, stft, cqt, stft_spec, cqt_spec, specshow, power_to_db
from .utils.methods import show_methods, show_method_params, cite_method, get_methods_list, get_method_name
from .utils.data import list_samples, fetch_sample
from .core.ctfr import ctfr, ctfr_from_specs
from .meta import cite, show_version
from .warning import FunctionNotBuiltWarning

from . import methods
from .methods_dict import _methods_dict


def _export_all_method_functions(_methods_dict):
    """Export all method functions to ctfr.methods.
    """
    for key in _methods_dict:
        _from_audio_function_export(key)
        _from_specs_function_export(key)

def _from_audio_function_export(key):
    """Export a method function that takes an audio signal as input."""
    function_name = key
    if not validate_function_name(function_name):
        _warn(f"Function name already exists in module ctfr.methods and thus was not built: {function_name}.", FunctionNotBuiltWarning)
    def _func(signal, sr, **kwargs):
        return ctfr(signal, sr = sr, method = key, **kwargs)
    _func.__doc__ = f"Alias for ``ctfr.ctfr(signal, method={key}, sr=sr, **kwargs)``."
    setattr(methods, function_name, _func)

def _from_specs_function_export(key):
    """Export a method function that takes an iterable of spectrograms as input."""
    function_name = key + "_from_specs"
    if not validate_function_name(function_name):
        _warn(f"Function name already exists in module ctfr.methods and thus was not built: {function_name}.", FunctionNotBuiltWarning)
    def _func(specs_tensor, **kwargs):
        return ctfr_from_specs(specs_tensor, method = key, **kwargs)
    _func.__doc__ = f"Alias for ``ctfr.ctfr_from_specs(specs_tensor, method={key}, **kwargs)``."
    setattr(methods, function_name, _func)

def validate_function_name(function_name):
    return not function_name in globals()

_export_all_method_functions(_methods_dict)