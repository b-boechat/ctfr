# tfrc
![Licence](https://img.shields.io/github/license/b-boechat/tfrc-lib)

#### Efficient toolbox for computing combined time-frequency representations of audio signals.

Status: in construction. [Testpypi link](https://test.pypi.org/project/tfrc/).

---

## Quickstart

Todo.

---

## Documentation

Todo.

---

## Installation

### Using PyPI

The latest stable release is available on PyPI, and can be installed with the following command:

```
pip install tfrc
```

### Development mode

If you want to make changes to tfrc, you can install it in editable mode with development dependencies by cloning or downloading the repository and running:

```
make dev
```

or

```
CYTHONIZE=1 pip install -e .[dev]
```

When installing in this mode, Cython is a build dependency. If you have trouble running this command, see [this guide](https://docs.cython.org/en/stable/src/quickstart/install.html).

This package is designed to be easily extensible with new TFR combination methods. See [here](ADDING_METHODS.md) for a tutorial on adding new combination methods to tfrc.

---

### Citing

If you use tfrc for your work, please cite the paper (TODO)

```
"TODO" in TODO.
```