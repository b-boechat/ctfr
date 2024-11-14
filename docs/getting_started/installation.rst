Installation
============

.. highlight:: shell

Using PyPI
----------

The latest stable release is available on PyPI, and can be installed with the following command::

   pip install ctfr

This will install the package and its runtime dependencies. Note that this doesn't install the plotting dependencies, which are optional. To install with plotting included, run::

   pip install ctfr[display]

Development mode
----------------

If you want to make changes to ctfr, you can install it in editable mode with development dependencies by cloning or downloading the repository and running::

   make dev

or::

   CYTHONIZE=1 pip install -e .[dev]

on a Linux system. On Windows, you can run instead::

   set CYTHONIZE=1
   pip install -e .[dev]

When installing in this mode, Cython is a build dependency. If you have trouble running Cython, see this guide.