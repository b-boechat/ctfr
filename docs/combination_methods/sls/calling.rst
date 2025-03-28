Calling signature
-----------------

.. function:: ctfr.methods.sls_h(signal, sr, *, <shared parameters>, lek, lsk, lem, lsm, beta, energy_criterium_db)
   :noindex:

.. function:: ctfr.methods.sls_h_from_specs(specs, *, <shared parameters>, lek, lsk, lem, lsm, beta, energy_criterium_db)
   :noindex:

.. function:: ctfr.methods.sls_i(signal, sr, *, <shared parameters>, lek, lsk, lem, lsm, beta, interp_steps)
   :noindex:

.. function:: ctfr.methods.sls_i_from_specs(specs, *, <shared parameters>, lek, lsk, lem, lsm, beta, interp_steps)
   :noindex:

.. note::
   As with all combination methods, you can also use :func:`ctfr.ctfr` or :func:`ctfr.ctfr_from_specs`.

See :func:`ctfr.ctfr` and :func:`ctfr.ctfr_from_specs` for more details on the shared parameters for computing CTFRs with this package. The parameters specific to this method (passed as keyword arguments) are described below.

Parameters
~~~~~~~~~~

**lem** (`int > 0, odd, optional`)

   Width in time frames of the analysis window used in the local energy computation. Defaults to 11.

**lsk** (`int > 0, odd, optional`)

   Width in frequency bins of the analysis window used in the local sparsity computation. Defaults to 21.

**lsm** (`int > 0, odd, optional`)

   Width in time frames of the analysis window used in the local sparsity computation. Defaults to 11.

**beta** (`float >= 0, optional`)

   Factor used in the computation of combination weights. Defaults to 0.3.

**lek** (`int > 0, odd, optional`)

   Width in frequency bins of the analysis window used in the local energy computation. Defaults to 21.

**energy_criterium_db** (`float, optional`)

   Local energy criterium (in decibels) that distinguishes high-energy regions (where LS is computed) from low-energy regions (where binwise minimum is computed). Defaults to -40. **Specific to sls_h**.

**interp_steps** (`ndarray of int, shape P x 2, optional`)

   Interpolation steps to use when computing the local sparsity. interp_steps[p, i] refers to the interpolation step of axis i (frequency is 0, time is 1) for spectrogram p. When calling :func:`ctfr.ctfr` (or :func:`ctfr.methods.sls_i`), ``interp_steps[p]`` defaults to ``[n_fft // l, l // (2 * hop_length)]``. When calling :func:`ctfr.ctfr_from_specs` (or :func:`ctfr.methods.sls_i_from_specs`), this argument must the provided by the user. **Specific to sls_i**.

