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

Adding parameters
-----------------

You can freely add parameters to your implementation function, as long as the iterable of TFRs remains as the first parameter. Any additional parameters will be treated as keyword-only parameters, and it's highly recommended for default values to be implemented.

.. note::
   Parameter names (aside from the TFRs tensor) must not clash with :func:`ctfr.ctfr` or :func:`ctfr.ctfr_from_specs` parameter names, otherwise they will not be received by the combination function. They should also not begin with an underscore, as this is reserved for internal use.

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


Advanced method entry
--------------------------

For a combination method to be functional, only the ``name`` and ``function`` fields are required in the entry in ``_methods_dict``. However, a method fully integrated into the package should have two additional fields: ``citations`` and ``parameters``. Both these fields are used to populate the method's documentation and to provide information to the user through the functions :func:`ctfr.cite_method` and :func:`ctfr.show_method_param`. Optionally, a field ``request_tfrs_info`` can be added, which is discussed below.

Citations field
~~~~~~~~~~~~~~~

If the method is published, the ``citations`` field should contain a list of strings with citations for one or more papers describing the method. The strings should be in IEEE citation style. If the method is not published, this field can be omitted or set to an empty list.

Parameters field
~~~~~~~~~~~~~~~~

The ``parameters`` field should contain a dictionary, which should be empty if the method has no specific parameters. Otherwise, each key must be a parameter name, and the value should be a dictionary with the fields ``type_and_info`` and ``description``. The ``type_and_info`` field should contain a string with the parameter type and possibly additional information (following the `NumPy docstrings style <https://numpydoc.readthedocs.io/en/latest/format.html#parameters>`_), and the ``description`` field should contain a string with a brief description of the parameter.

Request TFRs info field
~~~~~~~~~~~~~~~~~~~~~~~

Typically, the combination method receives only receives its parameters the TFRs tensor as input. However, when calling :func:`ctfr.ctfr` (or its `ctfr.methods` equivalent), methods can also receive additional data about the TFRs. This is done by setting the ``request_tfrs_info`` field to ``True`` (it's assumed to be ``False`` otherwise) and adding an argument named ``_info`` to the wrapper function, such as follows:

.. code-block:: diff

   - def _max_wrapper(X, offset=0.0):
   + def _max_wrapper(X, _info, offset=0.0):

The ``_info`` argument will be passed internally as a dictionary containing the key ``r_type`` with the value ``"stft"`` or ``"cqt"`` depending on the type of TFRs provided, and additional keys depending on the TFRs type. For ``_info["r_type"] == "stft"``, the keys ``"win_lengths"``, ``"hop_length"``, and ``"n_fft"`` will be present. For ``_info["r_type"] == "cqt"``, the keys ``"filter_scales"``, ``"bins_per_octave"``, ``"fmin"``, ``"n_bins"``, and ``"hop_length"`` will be present. These keys are compatible with their respective arguments in :func:`ctfr.ctfr`.

If ``request_tfrs_info`` is set to ``True`` and the method is called from :func:`ctfr.ctfr_from_specs` (or its `ctfr.methods` equivalent), ``_info`` will be passed as ``None``. In that case, the method should either provide a default behavior or raise `class:ctfr.exception.ArgumentRequiredError` if the information is necessary.

Example
~~~~~~~~

Here is an example of a complete entry in ``_methods_dict``::

   "fls": {
         "name": "Fast local sparsity (FLS)",
         "function": _fls_wrapper,
         "citations": ['M. d. V. M. da Costa and L. W. P. Biscainho, “The fast local sparsity method: A low-cost combination of time-frequency representations based on the hoyer sparsity,” Journal of the Audio Engineering Society, vol. 70, no. 9, pp. 698–707, Sep. 2022.'],
         "parameters": {
               "freq_width": {
                  "type_and_info": r"int > 0, odd",
                  "description": r"Width in frequency bins of the analysis window used in the local sparsity computation. Defaults to 21."
               },
               "time_width": {
                  "type_and_info": r"int > 0, odd",
                  "description": r"Width in time frames of the analysis window used in the local sparsity computation. Defaults to 11."
               },
               "gamma": {
                  "type_and_info": r"float >= 0",
                  "description": r"Factor used in the computation of combination weights. Defaults to 20."
               }
         }
      },