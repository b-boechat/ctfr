Calling signature
-----------------

.. function:: ctfr.methods.lt(signal, sr, *, <shared parameters>, lk, lm, eta)
   :noindex:

.. function:: ctfr.methods.lt_from_specs(specs, *, <shared parameters>, lk, lm, eta)
   :noindex:

.. note::
   As with all combination methods, you can also use :func:`ctfr.ctfr` or :func:`ctfr.ctfr_from_specs`.

See :func:`ctfr.ctfr` and :func:`ctfr.ctfr_from_specs` for more details on the shared parameters for computing CTFRs with this package. The parameters specific to this method (passed as keyword arguments) are described below.

Parameters
~~~~~~~~~~

**lk** (`int > 0, odd, optional`)

   Width in frequency bins of the analysis window used in the local energy smearing computation. Defaults to 21.

**lm** (`int > 0, odd, optional`)

   Width in time frames of the analysis window used in the local energy smearing computation. Defaults to 11.

**eta** (`float >= 0, optional`)

   Factor used in the computation of combination weights. Defaults to 8.

