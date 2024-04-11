import numpy as np
from scipy.signal import correlate
from libc.math cimport exp, sqrt
from warnings import warn
from tfrc.warning import ParameterChangeWarning
cimport cython

def _fls_wrapper(X, freq_width = 21, time_width = 11, gamma = 20.0):
    """ Calculate the "Fast Local Sparsity" (FLS) combination of spectrograms. 
        
        :param X (Ndarray <double> [P x K x M]): Spectrograms tensor. 
            Dimensions: spectrograms P x frequency bins K x time frames M.
        :param freq_width (Odd integer): Local sparsity window length in frequency.
        :param time_width (Odd integer): Local sparsity window length in time.
        :param gamma (Double >= 0): Parameter for calculating combination weights. Example value: gamma = 20.0.
        :return combined_tfr (Ndarray <double> [K x M]): Combined spectrogram, not yet with normalized energy.
        
        References: (Placeholder)
    """
    freq_width = int(freq_width)
    if freq_width % 2 == 0:
        freq_width += 1
        warn(f"The 'freq_width' parameter should be an odd integer. Changing to the nearest odd integer {freq_width}.", ParameterChangeWarning)

    time_width = int(time_width)
    if time_width % 2 == 0:
        time_width += 1
        warn(f"The 'time_width' parameter should be an odd integer. Changing to the nearest odd integer {time_width}.", ParameterChangeWarning)
    
    gamma = float(gamma)

    return _fls_cy(X, freq_width, time_width, gamma)

@cython.boundscheck(False)
@cython.wraparound(False) 
@cython.nonecheck(False)
@cython.cdivision(True)
cdef _fls_cy(double[:,:,::1] X, Py_ssize_t freq_width, Py_ssize_t time_width, double gamma):

    cdef:
        Py_ssize_t P = X.shape[0] # Spectrograms axis.
        Py_ssize_t K = X.shape[1] # Frequency axis.
        Py_ssize_t M = X.shape[2] # Time axis.

        double epsilon = 1e-10 # Small value used to avoid 0 in some computations.
        double window_size_sqrt = sqrt(<double> freq_width * time_width)

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
    combination_weight_ndarray = np.empty((P, K, M), dtype=np.double)
    cdef double[:, :, :] combination_weight = combination_weight_ndarray

    # Generate the 2D window for local sparsity calculation.
    hamming_window = np.outer(np.hamming(freq_width), np.hamming(time_width))

    ############ Local suitability calculation (using local Hoyer sparsity): {{{

    for p in range(P):
        # Calculate L1 and L2 local energy matrixes and element-wise square root of the L1 matrix.
        local_energy_l1_ndarray = correlate(X_ndarray[p], hamming_window, mode='same') + epsilon
        local_energy_l2_ndarray = np.sqrt(correlate(X_ndarray[p] * X_ndarray[p], hamming_window * hamming_window, mode='same') + epsilon)
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


# Temporary testing function.
def foo():
    print("Working!")