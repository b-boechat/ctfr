.. _combination methods:

Combination methods
===================

Time-frequency representations (TFRs) such as the short-time Fourier transform (STFT) or the constant-Q transform (CQT) can be computed with different resolutions. Notably, achieving a high frequency resolution requires long analysis windows, which in turn leads to a poor time resolution. Conversely, a high time resolution can be obtained with short windows, but at the expense of a poor frequency resolution. This tradeoff is a known challenge in signal processing and music information retrieval.

This package provides several methods that attempt to address this tradeoff by combining multiple TFRs (computed with different resolutions) into a single representation that preserves the best aspects of each individual TFR, achieving good localization in both time and frequency. We refer to these techniques as *combination methods*. If you are interested in learning more about combination methods, we recommend the following reading material:

- **Package release article**: `To be added.`

- **D.Sc. thesis on combination methods**: `M. do V. M. da Costa, Novel time-frequency representations for music information retrieval, D.Sc., Federal University of Rio de Janeiro, Rio de Janeiro, Brasil (2020 Apr.).`

The methods provided in this package are listed below. While we don't provide a detailed explanation of each method here, each section provides the information necessary to use the method with ``ctfr`` as well as additional references for further reading.

.. toctree::
   :maxdepth: 1

   binwise/index
   swgm/index
   lt/index
   sls/index
   fls/index