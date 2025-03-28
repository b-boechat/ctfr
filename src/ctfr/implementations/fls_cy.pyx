import numpy as np
from scipy.signal import correlate
from libc.math cimport exp, sqrt
from ctfr.utils.arguments_check import _enforce_nonnegative, _enforce_odd_positive_integer
cimport cython

def _fls_wrapper(X, lk = 21, lm = 11, gamma = 20.0):

    lk = _enforce_odd_positive_integer(lk, "lk", 21)
    lm = _enforce_odd_positive_integer(lm, "lm", 11)
    gamma = _enforce_nonnegative(gamma, "gamma", 20.0)

    return _fls_cy(X, lk, lm, gamma)

@cython.boundscheck(False)
@cython.wraparound(False) 
@cython.nonecheck(False)
@cython.cdivision(True)
cdef _fls_cy(double[:,:,::1] X, Py_ssize_t lk, Py_ssize_t lm, double gamma):

    cdef:
        Py_ssize_t P = X.shape[0] # Spectrograms axis.
        Py_ssize_t K = X.shape[1] # Frequency axis.
        Py_ssize_t M = X.shape[2] # Time axis.

        double epsilon = 1e-10 # Small value used to avoid 0 in some computations.
        double window_size_sqrt = sqrt(<double> lk * lm)

    X_ndarray = np.asarray(X)

    # Local energy containers.
    cdef: 
        double[:,:] local_energy_l1
        double[:,:] local_energy_l2
        double[:,:] local_energy_l1_sqrt

    # Local suitability container.
    suitability_ndarray = np.zeros((P, K, M), dtype=np.double)
    cdef double[:,:,:] suitability = suitability_ndarray

    # Containers related to combination.
    cdef double[:, :, :] log_suitability
    cdef double[:, :] sum_log_suitability
    combination_weight_ndarray = np.zeros((P, K, M), dtype=np.double)
    cdef double[:, :, :] combination_weight = combination_weight_ndarray

    # Generate the 2D window for local sparsity calculation.
    hamming_window = np.outer(np.hamming(lk), np.hamming(lm))

    ############ Local suitability calculation (using local Hoyer sparsity): {{{

    for p in range(P):
        # Calculate L1 and L2 local energy matrixes and element-wise square root of the L1 matrix.
        # Clipping is used because scipy correlate can return negative values for matrixes with very small positive elements.
        local_energy_l1_ndarray = np.clip(correlate(X_ndarray[p], hamming_window, mode="same"), a_min=epsilon, a_max=None)
        local_energy_l2_ndarray = np.sqrt(np.clip(correlate(X_ndarray[p] * X_ndarray[p], hamming_window * hamming_window, mode="same"), a_min=epsilon, a_max=None))
        local_energy_l1_sqrt_ndarray = np.sqrt(local_energy_l1_ndarray)

        # Point Cython memview to the calculated matrixes.
        local_energy_l1 = local_energy_l1_ndarray
        local_energy_l2 = local_energy_l2_ndarray
        local_energy_l1_sqrt = local_energy_l1_sqrt_ndarray

        # Calculate local suitability.
        for k in range(K):
            for m in range(M):
                suitability[p, k, m] = (window_size_sqrt - local_energy_l1[k, m]/local_energy_l2[k, m])/ \
                                        ((window_size_sqrt - 1) * local_energy_l1_sqrt[k, m]) + epsilon

    ############ }}}

    ############ Spectrograms combination {{{

    # Calculate spectrograms logarithm tensor and its sum along first dimension.
    log_suitability_ndarray = np.log(suitability_ndarray)
    sum_log_suitability_ndarray = np.sum(log_suitability_ndarray, axis=0)

    log_suitability = log_suitability_ndarray
    sum_log_suitability = sum_log_suitability_ndarray

    # Calculate combination weights based on local sparsity.
    for p in range(P):
        for k in range(K): 
            for m in range(M):
                combination_weight[p, k, m] = exp( (2*log_suitability[p, k, m] - sum_log_suitability[k, m]) * gamma)

    
    ############ Spectrograms combination }}}

    # Calculate spectrogram as a binwise weighted arithmetic mean.
    return np.average(X_ndarray, axis=0, weights=combination_weight_ndarray)