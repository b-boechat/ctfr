Simple binwise methods
======================

Combination methods based on simple binwise operations are designed to be simple and very fast to compute, though they may not provide the best results in terms of time-frequency resolution. The table below lists the simple binwise methods available in the package, as well as the function they compute for each entry :math:`X_{k, m}`.

.. list-table:: Description of simple binwise methods
   :header-rows: 1

   * - Method key
     - Binwise function
     - Description
   * - `mean`
     - :math:`\frac{1}{P}\sum_{p = 1}^P X_{k, m}[p]`
     - Arithmetic mean
   * - `hmean`
     - :math:`\left(\prod_{p = 1}^P X_{k, m}[p]\right)^{\frac{1}{P}}`
     - Harmonic mean
   * - `gmean`
     - :math:`\left(\frac{1}{P}\sum_{p = 1}^P \frac{1}{X_{k, m}[p]} \right)^{-1}`
     - Geometric mean
   * - `min`
     - :math:`\min_{p = 1, 2, \hdots, P} X_{k, m}[p]`
     - Minimum

.. include:: further_reading.rst

.. include:: calling.rst
