import numpy as np
from scipy.signal import correlate
cimport cython
from libc.math cimport INFINITY, exp
from ctfr.utils.arguments_check import _enforce_nonnegative, _enforce_odd_positive_integer

def _sls_h_wrapper(X, 
        lek = 11, 
        lsk = 21, 
        lem = 11, 
        lsm = 11, 
        beta = 80, 
        double energy_criterium_db = -40
    ):

    lek = _enforce_odd_positive_integer(lek, "lek", 11)
    lsk = _enforce_odd_positive_integer(lsk, "lsk", 21)
    lem = _enforce_odd_positive_integer(lem, "lem", 11)
    lsm = _enforce_odd_positive_integer(lsm, "lsm", 11)
    beta = _enforce_nonnegative(beta, "beta", 80.0)

    return _sls_h_cy(X, lek, lsk, lem, lsm, beta, energy_criterium_db)

@cython.boundscheck(False)
@cython.wraparound(False) 
@cython.nonecheck(False)
@cython.cdivision(True)
cdef _sls_h_cy(double[:,:,::1] X_orig, Py_ssize_t lek, Py_ssize_t lsk, Py_ssize_t lem, Py_ssize_t lsm, double beta, double energy_criterium_db):

    cdef:
        Py_ssize_t P = X_orig.shape[0] # Spectrograms axis
        Py_ssize_t K = X_orig.shape[1] # Frequency axis
        Py_ssize_t M = X_orig.shape[2] # Time axis
        
        Py_ssize_t lek_lobe = (lek-1)//2
        Py_ssize_t lsk_lobe = (lsk-1)//2
        Py_ssize_t lsm_lobe = (lsm-1)//2
        Py_ssize_t lem_lobe = (lem-1)//2
        Py_ssize_t p, m, k, i, j

        double epsilon = 1e-10
        Py_ssize_t combined_size_sparsity = lsm * lsk
    
    X_orig_ndarray = np.asarray(X_orig)
    # Zero-pad spectrograms for windowing.
    X_ndarray = np.pad(X_orig, ((0, 0), (lsk_lobe, lsk_lobe), (lsm_lobe, lsm_lobe)))
    cdef double[:, :, :] X = X_ndarray

    # Containers for the hamming window (local sparsity) and the asymmetric hamming window (local energy)
    hamming_freq_energy_ndarray = np.hamming(lek)
    hamming_freq_sparsity_ndarray = np.hamming(lsk)
    hamming_time_ndarray = np.hamming(lsm)
    hamming_asym_time_ndarray = np.hamming(lem)
    hamming_asym_time_ndarray[lem_lobe+1:] = 0

    hamming_energy = np.outer(hamming_freq_energy_ndarray, hamming_asym_time_ndarray)
    cdef double[:] hamming_freq_sparsity = hamming_freq_sparsity_ndarray
    cdef double[:] hamming_time = hamming_time_ndarray
    
    
    # Container that stores a spectrogram windowed region flattened to a vector.
    calc_vector_ndarray = np.zeros(combined_size_sparsity, dtype = np.double)
    cdef double[:] calc_vector = calc_vector_ndarray 

    # Container that stores the result.
    result_ndarray = np.zeros((K, M), dtype=np.double)
    cdef double[:, :] result = result_ndarray

    # Containers and variables related to local sparsity calculation.
    sparsity_ndarray = np.zeros(P, dtype=np.double) # Note that only one bin of sparsity information is stored each time.
    cdef double[:] sparsity = sparsity_ndarray
    cdef double arr_norm, gini

    # Container for the local energy.
    energy_ndarray = np.zeros((P, K, M), dtype=np.double)
    cdef double[:,:,:] energy = energy_ndarray


    # Variables related to the last step (spectrograms combination).
    cdef double[:] log_sparsity
    cdef double sum_log_sparsity
    combination_weight_ndarray = np.zeros(P, dtype=np.double)
    cdef double[:] combination_weight = combination_weight_ndarray
    cdef double min_local_energy
    cdef double weights_sum

    # Variable related to energy criterium.
    cdef double max_local_energy_db

    ############ Calculate local energy and maximum local energy along dimension p {{{ 

    for p in range(P):
        energy_ndarray[p] = np.clip(correlate(X_orig_ndarray[p], hamming_energy, mode="same")/np.sum(hamming_energy, axis=None), a_min=epsilon, a_max=None)

    max_local_energy_ndarray = np.max(energy_ndarray, axis=0)

    energy = energy_ndarray
    max_local_energy = max_local_energy_ndarray

    ############ }}}

    # Energy criterium in regular units.
    cdef double energy_criterium = 10.0 ** (energy_criterium_db/10.0)

    ############ Hybrid combination {{{

    # Iterates through bins.
    for k in range(lsk_lobe, K + lsk_lobe):
        for m in range(lsm_lobe, M + lsm_lobe):
            red_k, red_m = k - lsk_lobe, m - lsm_lobe
            
            # If this energy is below threshold, use binwise minimax.
            if max_local_energy[red_k, red_m] < energy_criterium:
                result[red_k, red_m] = INFINITY
                for p in range(P):
                    if X[p, k, m] < result[red_k, red_m]:
                        result[red_k, red_m] = X[p, k, m]

            # Otherwise, calculate LS combination.
            else:
                for p in range(P):
                    # Copy the windowed region to the calculation vector, multiplying by the Hamming windows (horizontal and vertical).
                    for i in range(lsk):
                        for j in range(lsm):
                            calc_vector[i*lsm + j] = X[p, k - lsk_lobe + i, m - lsm_lobe + j] * \
                                    hamming_freq_sparsity[i] * hamming_time[j]        

                    # Calculate the local sparsity (Gini index).
                    calc_vector_ndarray.sort()
                    arr_norm = 0.0
                    gini = 0.0
                    
                    for i in range(combined_size_sparsity):
                        arr_norm = arr_norm + calc_vector[i]
                        gini = gini - 2*calc_vector[i] * (combined_size_sparsity - i - 0.5)/ (<double> combined_size_sparsity)
                    gini = 1 + gini/(arr_norm + epsilon)

                    sparsity[p] = epsilon + gini

                # Combination by smoothed local sparsity:
                log_sparsity_ndarray = np.log(sparsity_ndarray)
                sum_log_sparsity = np.sum(log_sparsity_ndarray)

                log_sparsity = log_sparsity_ndarray

                min_local_energy = INFINITY
                weights_sum = 0.0
                for p in range(P):
                    combination_weight[p] = exp( (2*log_sparsity[p] - sum_log_sparsity) * beta)
                    weights_sum += combination_weight[p]
                    if energy[p, red_k, red_m] < min_local_energy:
                        min_local_energy = energy[p, red_k, red_m]

                result[red_k, red_m] = 0.0
                for p in range(P):
                    result[red_k, red_m] = result[red_k, red_m] + X_orig[p, red_k, red_m] * combination_weight[p] * min_local_energy / energy[p, red_k, red_m]
                result[red_k, red_m] = result[red_k, red_m] / weights_sum


    return result_ndarray















                
