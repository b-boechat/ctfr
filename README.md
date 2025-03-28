# ctfr

[![PyPI](https://img.shields.io/pypi/v/ctfr.svg)](https://pypi.python.org/pypi/ctfr) [![Python Versions](https://img.shields.io/pypi/pyversions/ctfr.svg)](https://pypi.python.org/pypi/ctfr) ![Licence](https://img.shields.io/github/license/b-boechat/ctfr) 

#### Efficient toolbox for computing combined time-frequency representations of audio signals.

# Table of contents
- [Documentation](#documentation)
- [Installation](#instalation)
    - [Using PyPI](#using-pypi)
    - [Development mode](#development-mode)
- [Citing](#citing)

---

[Back to top ↥](#ctfr)
## Documentation

See the ctfr [documentation](https://ctfr.readthedocs.io/en/latest/) for more information about the package, including usage examples and the API reference.

---

[Back to top ↥](#ctfr)
## Instalation

### Using PyPI

The latest stable release is available on PyPI, and can be installed with the following command:

```shell
pip install ctfr
```

Note that this doesn’t install the plotting dependencies. To install with plotting included, run

```shell
pip install ctfr[display]
```

### Development mode

If you want to make changes to ctfr, you can install it in editable mode with development dependencies by cloning or downloading the repository and running:

```shell
make dev
```

or

```shell
pip install -e .[dev]
```

When installing in this mode, Cython is a build dependency. If you have trouble running Cython, see [this guide](https://docs.cython.org/en/stable/src/quickstart/install.html).

Note: When developing, `.pyx` files need to be recompiled in order for changes in them to take place. This can be done by running 

```shell
make ext
```

or

```shell
python setup.py build_ext --inplace
```

---

[Back to top ↥](#ctfr)
## Citing

If you use ctfr in your work or research, please cite following paper:

```
To be added.
```

Also, if you use a speficic combination method, please cite the corresponding paper(s). You can find the references for a specific method by running:

```python
>>> ctfr.cite_method("fls")
M. do V. M. da Costa and L. W. P. Biscainho, “The fast local sparsity method: A low-cost combination of time-frequency representations based on the hoyer sparsity,” Journal of the Audio Engineering Society, vol. 70, no. 9, pp. 698–707, Sep. 2022.
```