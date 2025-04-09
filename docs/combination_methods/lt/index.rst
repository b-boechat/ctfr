Lukin-Todd
==========

The Lukin-Todd (LT) is a combination method that employs an energy-smearing function as a local information measure. Each entry :math:`X_{k, m}` is computed as a weighted average of the samples :math:`X_{k, m}[p]`, where larger weights are given to samples on low-smearing neighborhoods. The LT method is computationally costly when compared to most other methods, as computing the smearing function requires sorting the samples in each neighborhood.

.. note::
   It's highly recommended to use `NumPy <https://numpy.org/doc/stable>`_ version 2.0 or higher for this combination method, as the performance of the sorting procedure is improved substantially.

.. include:: further_reading.rst

.. include:: calling.rst

