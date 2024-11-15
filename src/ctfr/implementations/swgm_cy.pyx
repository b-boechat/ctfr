import numpy as np
from scipy.stats import gmean
cimport cython
from libc.math cimport exp
from warnings import warn
from ctfr.warning import ArgumentChangeWarning

def _swgm_wrapper(X, beta = 0.3, max_gamma = 20.0):
    
    beta = float(beta)
    if beta < 0:
        beta = 0.0
        warn("Beta parameter must be >= 0. Setting beta = 0.", ArgumentChangeWarning)

    max_gamma = float(max_gamma)
    if max_gamma < 1.0:
        max_gamma = 1.0
        warn("Max_gamma parameter must be >= 1. Setting max_gamma = 1.", ArgumentChangeWarning)

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
        double epsilon = 1e-10

    # Calculate spectrograms logarithm tensor.
    log_X_ndarray = np.log(np.asarray(X) + epsilon, dtype=np.double)
    cdef double[:, :, :] log_X = log_X_ndarray
    
    # Calculate spectrograms logarithm tensor sum along first dimension.
    sum_log_X_ndarray = np.sum(log_X_ndarray, axis=0) / (P - 1)
    cdef double[:, :] sum_log_X = sum_log_X_ndarray

    # Calculate weights tensor.
    gammas_ndarray = np.empty((P, K, M), dtype=np.double)
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