import numpy as np
cimport cython
from libc.math cimport sqrt
from warnings import warn
from ctfr.warning import ArgumentChangeWarning

def _baseline_lt_wrapper(X, freq_width = 21, time_width = 11, eta = 8.0):
    freq_width = int(freq_width)
    if freq_width < 0:
        freq_width = 21
        warn(f"The 'freq_width' parameter should be a positive integer. Setting freq_width = {freq_width}.", ArgumentChangeWarning)
    if freq_width % 2 == 0:
        freq_width += 1
        warn(f"The 'freq_width' parameter should be an odd integer. Setting freq_width = {freq_width}.", ArgumentChangeWarning)

    time_width = int(time_width)
    if time_width < 0:
        time_width = 11
        warn(f"The 'time_width' parameter should be a positive integer. Setting time_width = {time_width}.", ArgumentChangeWarning)
    if time_width % 2 == 0:
        time_width += 1
        warn(f"The 'time_width' parameter should be an odd integer. Setting time_width = {time_width}.", ArgumentChangeWarning)
    
    eta = float(eta)
    if eta < 0.0:
        eta = 8.0
        warn(f"The 'eta' parameter should be a non-negative float. Setting eta = {eta}.", ArgumentChangeWarning)

    return _baseline_lt_cy(X, freq_width, time_width, eta)

@cython.boundscheck(False)
@cython.wraparound(False) 
@cython.nonecheck(False)
@cython.cdivision(True)
cdef _baseline_lt_cy(double[:,:,::1] X_orig, Py_ssize_t freq_width, Py_ssize_t time_width, double eta):

    cdef:
        Py_ssize_t P = X_orig.shape[0]
        Py_ssize_t K = X_orig.shape[1]
        Py_ssize_t M = X_orig.shape[2]
        
        Py_ssize_t freq_width_lobe = (freq_width-1)//2
        Py_ssize_t time_width_lobe = (time_width-1)//2
        Py_ssize_t p, m, k, i, j

        double epsilon = 1e-10
        Py_ssize_t combined_size = time_width * freq_width

    X_ndarray = np.pad(X_orig, ((0, 0), (freq_width_lobe, freq_width_lobe), (time_width_lobe, time_width_lobe)))
    cdef double[:, :, :] X = X_ndarray


    calc_vector_ndarray = np.zeros(combined_size, dtype = np.double)
    cdef double[:] calc_vector = calc_vector_ndarray 
 
    result_ndarray = np.zeros((K, M), dtype=np.double)
    cdef double[:, :] result = result_ndarray

    smearing_ndarray = np.zeros((P, K, M), dtype=np.double)
    cdef double[:,:,:] smearing = smearing_ndarray
    cdef double smearing_numerator, smearing_denominator
    cdef Py_ssize_t o

    cdef double weight, weights_sum, result_acc


    for p in range(P):
        for k in range(freq_width_lobe, K + freq_width_lobe):
            for m in range(time_width_lobe, M + time_width_lobe):

                for i in range(freq_width):
                    for j in range(time_width):
                        calc_vector[i*time_width + j] = X[p, k - freq_width_lobe + i, m - time_width_lobe + j]                
                
                calc_vector_ndarray.sort()

                smearing_denominator = 0.0
                smearing_numerator = 0.0
                for o in range(combined_size):
                    smearing_denominator = smearing_denominator + calc_vector[o]
                    smearing_numerator = smearing_numerator + (combined_size-o)*calc_vector[o]
                smearing[p, k - freq_width_lobe, m - time_width_lobe] = smearing_numerator/(sqrt(smearing_denominator) + epsilon)
                

    for k in range(K):
        for m in range(M):
            weights_sum = 0.0
            result_acc = 0.0
            for p in range(P):
                weight = 1./(smearing[p, k, m] ** eta + epsilon)
                result_acc = result_acc + weight * X_orig[p, k, m]
                weights_sum = weights_sum + weight
            result[k, m] = result_acc / weights_sum

    return result_ndarray















                
