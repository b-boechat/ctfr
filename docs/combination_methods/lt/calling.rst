Calling signature
-----------------

.. function:: ctfr.ctfr(signal, sr, method="lt", *, <shared parameters>, freq_width, time_width, eta)
   :noindex:

.. function:: ctfr.ctfr_from_specs(specs, method="lt", *, <shared parameters>, freq_width, time_width, eta)
   :noindex:

.. function:: ctfr.methods.lt(signal, sr, *, <shared parameters>, freq_width, time_width, eta)
   :noindex:

.. function:: ctfr.methods.lt_from_specs(specs, *, <shared parameters>, freq_width, time_width, eta)
   :noindex:

See :func:`ctfr.ctfr` and :func:`ctfr.ctfr_from_specs` for more details on the shared parameters for computing CTFRs with this package. The parameters specific to this method (passed as keyword arguments) are described below.

Parameters
~~~~~~~~~~

**freq_width** (`int > 0, odd, optional`)

   Width in frequency bins of the analysis window used in the local energy smearing computation. Defaults to 21.

**time_width** (`int > 0, odd, optional`)

   Width in time frames of the analysis window used in the local energy smearing computation. Defaults to 11.

**eta** (`float >= 0, optional`)

   Factor used in the computation of combination weights. Defaults to 8.

