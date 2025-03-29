import numpy as np
from scipy.stats import gmean
from warnings import warn
from ctfr.warning import ArgumentChangeWarning
cimport cython
from libc.math cimport pow

def _baseline_swgm_wrapper(X, beta = 0.3, max_gamma = 20.0): 
    beta = float(beta)
    if beta < 0:
        beta = 0.0
        warn("Beta parameter must be >= 0. Setting beta = 0.", ArgumentChangeWarning)

    max_gamma = float(max_gamma)
    if max_gamma < 1.0:
        max_gamma = 1.0
        warn("Max_gamma parameter must be >= 1. Setting max_gamma = 1.", ArgumentChangeWarning)

    return _baseline_swgm_cy(X, beta, max_gamma)

@cython.boundscheck(False)
@cython.wraparound(False) 
@cython.nonecheck(False)
@cython.cdivision(True)
cdef _baseline_swgm_cy(double[:,:,::1] X, double beta, double max_gamma):
    cdef:
        Py_ssize_t P = X.shape[0]
        Py_ssize_t K = X.shape[1]
        Py_ssize_t M = X.shape[2]
        Py_ssize_t p, k, m, l
    
    gammas_ndarray = np.ones((P, K, M), dtype = np.double)
    cdef double[:, :, :] gammas = gammas_ndarray
    result_ndarray = np.ones((K, M), dtype=np.double)
    cdef double[:, :] result = result_ndarray

    for k in range(K):
        for m in range(M):
            for p in range(P):
                for l in range(P):
                    if l != p:
                        gammas[p, k, m] = gammas[p, k, m] * pow(X[l, k, m], 1./(P - 1)) 
                gammas[p, k, m] = (gammas[p, k, m]/X[p, k, m]) ** beta
                if gammas[p, k, m] > max_gamma:
                    gammas[p, k, m] = max_gamma

    # Calculate combined spectrogram as a binwise weighted geometric mean.
    return gmean(X, axis=0, weights=gammas_ndarray)