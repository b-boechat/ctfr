from warnings import warn
from ctfr.warning import ArgumentChangeWarning

def _enforce_nonnegative(value, name, default):
    value = float(value)
    if value < 0:
        warn(f"The '{name}' parameter should be a nonnegative float. Setting {name} = {default}.", ArgumentChangeWarning)
        return default
    return value

def _enforce_greater_or_equal(value, name, target, default):
    value = float(value)
    if value < target:
        warn(f"The '{name}' parameter should be greater than or equal to {target}. Setting {name} = {default}.", ArgumentChangeWarning)
        return default
    return value

def _enforce_nonnegative_integer(value, name, default):
    value = int(value)
    if value < 0:
        warn(f"The '{name}' parameter should be a nonnegative integer. Setting {name} = {default}.", ArgumentChangeWarning)
        return default
    return value

def _enforce_odd_positive_integer(value, name, default):
    value = int(value)
    if value < 0:
        warn(f"The '{name}' parameter should be an odd positive integer. Setting {name} = {default}.", ArgumentChangeWarning)
        return default
    if value % 2 == 0:
        warn(f"The '{name}' parameter should be an odd positive integer. Setting {name} = {value}.", ArgumentChangeWarning)
        return value + 1
    return value

