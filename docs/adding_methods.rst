.. _adding methods:

Adding methods
==============

This tutorial explains how to easily extend ``ctfr`` with new TFR combination methods.

Installation
------------

First, make sure you have ``ctfr`` installed in editable mode with development dependencies. See :ref:`the installation guide <development mode>` for more details.

Writing a simple method
-----------------------

Let's create as an example a combination method `max` that computes a binwise maximum, written in Python using `NumPy`. First, create a file named ``max.py`` under ``src/ctfr/implementations``::

   ├── src
   │   ├── ctfr
   |   │   ├── implementations
   |   │   |   ├── ...
   |   |   |   └── max.py

.. highlight:: python

Then, implement the combination algorithm in a function called ``_max``. We'll call it the `implementation function`. It must accept as first argument an iterable of TFRs with the same specifications as :func:`ctfr.ctfr_from_specs`. We'll call this argument `X`, a convention used by this package's methods::

   # contents of max.py
   import numpy as np

   def _max(X):
      return np.max(X, axis=0)

Now, we need to install this function to the methods dictionary. Open ``src/ctfr/methods_dict.py``. First, add a line to import your function::

   from .implementations.max import _max

Then, add the following entry to ``_methods_dict``::

   _methods_dict = {
      ... # other methods...
      "max": {
         "name": "Binwise Maximum",
         "function": _max,
         "citation": None
      }
   }

And its's done! Your combination method is fully integrated into the package. You can now use it just as any included method by calling ``ctfr.methods.max`` or ``ctfr.methods.max_from_specs`` or by providing ``method="max"`` to :func:`ctfr.ctfr` or :func:`ctfr.ctfr_from_specs`. You can verify that your method works by running the following code in an interactive Python session::

   >>> import ctfr
   >>> import numpy as np
   >>> X = np.array([ [[0, 5], [5, 0]], [[10, 0], [0, 10]]  ])
   >>> ctfr.methods.max_from_specs(X, normalize_input=False, normalize_output=False)
   array([[10,  5],
         [ 5, 10]])

.. note::

   A combination method key (as specified in ``methods_dict``) must be unique from other methods. They also must not start with a trailing underscore or end with *_from_specs*.

Adding citation information
---------------------------

Entries in ``_methods_dict`` should have a ``citation`` field, which can be set to ``None`` if the method is not published. Otherwise, it should be a string with a citation for the method in IEEE citation style. Additionally, if a DOI is available, it can be optionally added as an url in a ``doi`` field.

For example, the entry for the *fls* method is as follows::

   "fls": {
      ... # name and function fields
      "citation": "M. V. M. da Costa and L. W. P. Biscainho, \"The fast local sparsity method: a low-cost combination of time-frequency representations based on the Hoyer sparsity\", Journal of the Audio Engineering Society, vol. 70, no. 9, pp. 698–707, 09 2022."
      "doi": "https://doi.org/10.17743/jaes.2022.0036"
   }

Adding parameters
-----------------

You can freely add parameters to your implementation function, as long as the iterable of TFRs remains as the first parameter. Any additional parameters will be treated as keyword-only parameters, and it's highly recommended for default values to be implemented.

.. note::
   Parameter names (aside from the TFRs tensor) must not clash with :func:`ctfr.ctfr` or :func:`ctfr.ctfr_from_specs` parameter names, otherwise they will not be received by the combination function.

Parameter validation
~~~~~~~~~~~~~~~~~~~~

If you add parameters to your method, it is good practice to create a `wrapper` function to perform parameter validation. For example, let's add a parameter called *offset* to the *max* method, which is added to every element before computing the binwise maximum. This argument is required to be a positive number. Let's change our ``max.py`` file::

   # content of max.py
   import numpy as np

   def _max_wrapper(X, offset=0.0):
      if offset < 0.0:
         raise ValueError("'offset' argument must be a positive number.")
      return _max(X, offset)

   def _max(X, offset):
      return np.max(X + offset, axis=0)

Then, we must change all ``_max`` references to ``_max_wrapper`` in ``methods_dict.py``.

Instead of raising an error when an invalid value for a parameter is provided, you can choose instead to just issue a warning and invoke the method anyway with a corrected value. This package provides an ``ArgumentChangeWarning`` for this purpose. To default to ``offset = 0.0`` when a negative value is specified, add the following imports::

   from warnings import warn
   from ctfr.warning import ArgumentChangeWarning

and replace the Exception line:

.. code-block:: diff

   if offset < 0.0:
   -   raise ValueError("'offset' argument must be a positive number.")
   +   offset = 0.0
   +   warn(f"'offset' parameter must be a positive number. Setting offset = {offset}.", ArgumentChangeWarning)

Adding Cython modules
---------------------

Most ``ctfr`` combination methods are written as Cython modules, resulting in significant performance improvements over pure Python. Source ``[filename].pyx`` files located under ``src/ctfr/implementations`` are automatically compiled during installation, and the built modules can be imported in ``methods_dict.py`` with::

   from .implementations.[filename] import [wrapper_name]

Cython's "pure Python" mode is not yet supported.

.. note::
   When developing, ``.pyx`` files need to be recompiled in order for changes to take place. This can be done by running ``make ext`` or ``python setup.py build_ext --inplace``.