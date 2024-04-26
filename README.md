# tfrc
![Licence](https://img.shields.io/github/license/b-boechat/tfrc-lib)

#### Efficient toolbox for computing combined time-frequency representations of audio signals.

Status: in construction. [Testpypi link](https://test.pypi.org/project/tfrc/).

# Table of Contents

- [Quickstart](#quickstart)
- [Documentation](#documentation)
- [Installation](#installation)
  - [Using PyPI](#using-pypi)
  - [Development mode](#development-mode)
- [Adding methods](#adding-methods)
    - [Installation](#installation-1)
    - [Writing a simple method](#writing-a-simple-method)
    - [Adding parameters](#adding-parameters)
        - [Parameter validation](#parameter-validation)
    - [Adding Cython modules](#adding-cython-modules)
    - [Note about names](#note-about-names)
        - [Validating methods](#validating-methods)
- [Citing](#citing)

---

[Back to top ↥](#tfrc)
## Quickstart

Todo.

---

[Back to top ↥](#tfrc)
## Documentation

Todo.

---

[Back to top ↥](#tfrc)
## Installation

### Using PyPI

The latest stable release is available on PyPI, and can be installed with the following command:

```shell
pip install tfrc
```

### Development mode

If you want to make changes to tfrc, you can install it in editable mode with development dependencies by cloning or downloading the repository and running:

```shell
make dev
```

or

```shell
CYTHONIZE=1 pip install -e .[dev]
```

When installing in this mode, Cython is a build dependency. If you have trouble running this command, see [this guide](https://docs.cython.org/en/stable/src/quickstart/install.html).

---

[Back to top ↥](#tfrc)
## Adding methods

tfrc is designed to be easily extensible with new combination methods written in Python or Cython. This section explains how to do so.

### Installation

First, make sure you've installed tfrc in editable mode with development dependencies. See [the installation guide](README.md#development-mode) for more details.

### Writing a simple method

Let's create as an example a combination method *max* that computes a binwise maximum, written in Python using NumPy. First, create a file named ```max.py``` under ```src/tfrc/methods/implementations```:

```
├── src
│   ├── tfrc
│   │   ├── methods
│   |   │   ├── implementations
│   |   │   |   ├── ...
|   |   |   |   └── max.py
```

Then, implement the combination algorithm in a function called ```_max```. We'll call it the *implementation function*. It must accept as first argument a TFRs tensor with the same specifications as ```tfrc_from_specs``` (see documentation for more details). We'll call this argument *X*, a convention used by this package's methods.

```python
# content of max.py
import numpy as np

def _max(X):
    return np.max(X, axis=0)
```

Then, add this function to the methods dictionary. Open ```src/tfrc/methods/methods_dict.py```. Now, add a line to import your function:

```python
from .implementations.max import _max
```


Then, add the following entry to ```_methods_dict```:

```python
_methods_dict = {
    ...
    "max": {
        "name": "Binwise Maximum",
        "function": _max
    }
}
```

And its's done! Your combination method is fully integrated into the package. You can now use it just as any included method by calling ```tfrc.max``` or ```tfrc.max_from_specs``` or by providing ```method="max"``` to ```tfrc.tfrc``` or ```tfrc.tfrc_from_specs``` (see documentation for more details). You can verify that your method works by running the following code in an interactive Python session:

```python
>>> import tfrc
>>> import numpy as np
>>> X = np.array([ [[0, 5], [5, 0]], [[10, 0], [0, 10]]  ])
>>> tfrc.max_from_specs(X, normalize_input=False, normalize_output=False)
array([[10,  5],
       [ 5, 10]])
```

### Adding parameters

You can freely add parameters to your implementation function, as long as the TFRs tensor *X* remains as the first parameter. Any parameters you add will be treated as keyword-only parameters. It's highly recommended for default values to be implemented for all aditional parameters.

#### Parameter validation

If you add parameters to your method, it is good practice to create a *wrapper* function to perform parameter validation. For example, let's add a parameter called *offset* to the *max* method, which is added to every element before computing the binwise maximum. This argument is required to be a positive number. Let's change our ```max.py``` file: (TODO add validation for being a number)

```python
# content of max.py
import numpy as np

def _max_wrapper(X, offset=0.0):
    if offset < 0.0:
        raise ValueError("'offset' argument must be a positive number.")
    return _max(X, offset)

def _max(X, offset):
    return np.max(X + offset, axis=0)
```

Then, we must change all ```_max``` references to ```_max_wrapper``` in ```methods_dict.py```.

Instead of raising an error when an invalid value for a parameter is provided, you can choose instead to just issue a warning and invoke the method anyway with a corrected value. This package provides an ```ArgumentChangeWarning``` for this purpose. To default to ```offset = 0.0``` when a negative value is specified, add the following imports

```python
from warnings import warn
from tfrc.warning import ArgumentChangeWarning
```

and replace the Exception line:

```diff
if offset < 0.0:
-   raise ValueError("'offset' argument must be a positive number.")
+   offset = 0.0
+   warn(f"'offset' parameter must be a positive number. Setting offset = {offset}.", ArgumentChangeWarning)
```

### Adding Cython modules

Most tfrc combination methods are written as Cython modules, resulting in significant performance improvements over pure Python. You can read more about Cython [here](https://cython.readthedocs.io/en/stable/index.html). Source ```[filename].pyx``` files located under ```src/tfrc/methods/implementations``` are automatically compiled during installation, and the built modules can be imported in ```methods_dict.py``` with

```python
from .implementations.[filename] import [wrapper_name]
```

Cython's "pure Python" mode is not yet supported, but contributions are welcome.

Note: when developing, ```.pyx``` files need to be recompiled in order for changes to take place. This can be done by running

```shell
make ext
```

or

```shell
python setup.py build_ext --inplace
```


### Note about names

A combination method name (as specified by its key in ```methods_dict```) must not clash with other tfrc module-level function names. See documentation for a complete list of functions. They also must not start with a trailing underscore or end with *_from_specs*, as that could mean additional clashes.

Parameter names (aside from the TFRs tensor) must not clash with ```tfrc``` or ```tfrc_from_specs``` parameter names, otherwise they will not be received by the combination function. See documentation for a complete list of those parameters.

#### Validating methods

TODO function to validate methods and parameter names.

---

[Back to top ↥](#tfrc)
### Citing

If you use tfrc for your work, please cite the paper (TODO)

```
"TODO" in TODO.
```