import numpy as np
from scipy.stats import gmean
cimport cython
from libc.math cimport exp
from ctfr.utils.arguments_check import _enforce_nonnegative, _enforce_greater_or_equal

def _swgm_wrapper(X, beta = 0.3, max_gamma = 20.0):

    beta = _enforce_nonnegative(beta, "beta", default=0.3)
    max_gamma = _enforce_greater_or_equal(max_gamma, "max_gamma", target=1.0, default=20.0)

    return _swgm_cy(X, beta, max_gamma)

@cython.boundscheck(False)
@cython.wraparound(False) 
@cython.nonecheck(False)
@cython.cdivision(True)
cdef _swgm_cy(double[:,:,::1] X, double beta, double max_gamma):
    cdef:
        Py_ssize_t P = X.shape[0] # Spectrograms axis.
        Py_ssize_t K = X.shape[1] # Frequency axis.
        Py_ssize_t M = X.shape[2] # Time axis.

        Py_ssize_t p, k, m
        double epsilon = 1e-15

    # Calculate spectrograms logarithm tensor.
    log_X_ndarray = np.log(np.asarray(X) + epsilon, dtype=np.double)
    cdef double[:, :, :] log_X = log_X_ndarray
    
    # Calculate spectrograms logarithm tensor sum along first dimension.
    sum_log_X_ndarray = np.sum(log_X_ndarray, axis=0) / (P - 1)
    cdef double[:, :] sum_log_X = sum_log_X_ndarray

    # Calculate weights tensor.
    gammas_ndarray = np.zeros((P, K, M), dtype=np.double)
    cdef double[:,:,:] gammas = gammas_ndarray
    
    # Calculate combination weights.
    for k in range(K):
        for m in range(M):
            for p in range(P):
                gammas[p, k, m] = sum_log_X[k, m] - log_X[p, k, m] * P / (P - 1)
                gammas[p, k, m] = exp(gammas[p, k, m] * beta)
                if gammas[p, k, m] > max_gamma:
                    gammas[p, k, m] = max_gamma

    # Calculate combined spectrogram as a binwise weighted geometric mean.
    return gmean(X, axis=0, weights=gammas_ndarray)