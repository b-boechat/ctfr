Calling signature
=================

.. function:: ctfr.ctfr(<other parameters>, method=swgm, beta, max_gamma)
   :noindex:

.. function:: ctfr.ctfr_from_specs(<other parameters>, method=swgm, beta, max_gamma)
   :noindex:

.. function:: ctfr.methods.swgm(<other parameters>, beta, max_gamma)
   :noindex:

.. function:: ctfr.methods.swgm_from_specs(<other parameters>, beta, max_gamma)
   :noindex:

See :func:`ctfr.ctfr` and :func:`ctfr.ctfr_from_specs` for more details on the general parameters. The parameters specific to this method (passed as keyword arguments) are described below.

Parameters
----------

**beta** (`float, range: [0, 1], optional`)

   Weighting factor for computing the weights for the geometric mean. When ``beta = 0``, the SWGM is equivalent to an unweighted geometric mean. When ``beta = 1``, the SWGM is equivalent to the minimum combination. Defaults to 0.3.

**max_gamma** (`float >= 1, optional`)

   Maximum weight for the geometric mean. This parameter is used to avoid numerical instability when the weights are too large. Defaults to 20.

