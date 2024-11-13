__version__ = "0.0.0.7"

from warnings import warn as _warn
from ctfr.utils import load, stft, cqt, stft_spec, cqt_spec, specshow, power_to_db
from ctfr.core import ctfr, ctfr_from_specs
from ctfr.meta import cite, cite_method, show_version
from ctfr.warning import FunctionNotBuiltWarning

from ctfr.methods.methods_dict import _methods_dict
from ctfr.methods import get_methods, list_methods, validate_method, get_method_name

def _export_all_method_functions(_methods_dict):
    for key in _methods_dict:
        _from_audio_function_export(key)
        _from_specs_function_export(key)

def _from_audio_function_export(key):
    function_name = key
    if not validate_function_name(function_name):
        # Move this warning message to a default message in ctfr.warning.
        _warn(f"Function name already exists in module and thus was not built: {function_name}. This probably means that a combination method was defined with the same name as a module function.", FunctionNotBuiltWarning)
    globals()[function_name] = lambda signal, **kwargs: ctfr(signal, method = key, **kwargs)

def _from_specs_function_export(key):
    function_name = key + "_from_specs"
    if not validate_function_name(function_name):
        _warn(f"Function name already exists in module and thus was not built: {function_name}. This probably means that a combination method was defined with the same name as a module function.", FunctionNotBuiltWarning)
    globals()[function_name] = lambda specs_tensor, **kwargs: ctfr_from_specs(specs_tensor, method = key, **kwargs)

def validate_function_name(function_name):
    return not function_name in globals()


_export_all_method_functions(_methods_dict)