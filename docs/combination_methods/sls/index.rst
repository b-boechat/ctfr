Smoothed local sparsity
========================

The smoothed local sparsity (SLS) is a combination method based local information. It employs a local sparsity measure (Gini index) and a local energy measure in its combination procedure. The SLS requires sorting samples in each neighborhood to compute the Gini index, which makes this method computationally costly, particularly because computational tricks used in the Lukin-Todd method to speed up the sorting process cannot be applied here. Instead of the SLS in its base form, this package provides two approximations that are computationally more efficient: the hybrid smoothed local sparsity (SLS-H) and the smoothed local sparsity with interpolation (SLS-I). The SLS-H uses a local energy criterium to compute the SLS only in high-energy regions, defaulting to a binwise minimum elsewhere. The SLS-I interpolates the local sparsity to reduce the number of neighborhoods that need to be sorted.

.. note::
   It's highly recommended to use `NumPy <https://numpy.org/doc/stable>`_ version 2.0 or higher for this combination method, as the performance of the sorting procedure is improved substantially.

.. include:: further_reading.rst

.. include:: calling.rst