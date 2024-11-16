Installation
============

.. highlight:: shell

Using PyPI
----------

The latest stable release is available on PyPI, and can be installed with the following command::

   pip install ctfr

Note that this doesn't install the plotting dependencies. To install with plotting included, run::

   pip install ctfr[display]

.. _development mode:

Development mode
----------------

If you want to make changes to ctfr, you can install it in editable mode with development dependencies by cloning or downloading the repository and running::

   make dev

or::

   pip install -e .[dev]

When installing in this mode, Cython is a build dependency. If you have trouble running Cython, see this guide.

.. note::
   When developing, ``.pyx`` files need to be recompiled in order for changes in them to take place. This can be done by running ``make ext`` or ``python setup.py build_ext --inplace``.