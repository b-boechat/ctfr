# Versão do Local Sparsity que realiza combinação por média geométrica nas regiões de menor energia, para diminuir o custo computacional.

import numpy as np
from scipy.signal import correlate
cimport cython
from libc.math cimport INFINITY, exp, log10


# Currently only hybrid.
def _ls_wrapper(X, freq_width_energy=11, freq_width_sparsity=21, time_width_energy=11, time_width_sparsity=11, beta = 80, double energy_criterium_db=-50):
    """ Calculate the "Hybrid Local Sparsity" (LS-H) combination of spectrograms. In low-energy regions the combination defaults to binwise minimax, in order to reduce the computational cost.
        
        :param X (Ndarray <double> [P x K x M]): Spectrograms tensor. 
            Dimensions: spectrograms P x frequency bins K x time frames M.
        :param freq_width_energy (Odd integer): Local energy window length in frequency.
        :param freq_width_sparsity (Odd integer): Local sparsity window length in frequency.
        :param time_width_energy (Odd integer): Local energy window length in time.
        :param time_width_sparsity (Odd integer): Local sparsity window length in time.
        :param beta (Double >= 0): Parameter for calculating combination weights. Example value: beta = 80.0.
        :param energy_criterium_db (Double): Local energy criterium that distinguishes high-energy regions (where LS is computed) from low-energy regions (where binwise minimax is computed).
        :return combined_tfr (Ndarray <double> [K x M]): Combined spectrogram, not yet with normalized energy.
        
        References: (Placeholder)
    """
    return local_sparsity_hybrid(X, freq_width_energy, freq_width_sparsity, time_width_energy, time_width_sparsity, beta, energy_criterium_db)

@cython.boundscheck(False)
@cython.wraparound(False) 
@cython.nonecheck(False)
@cython.cdivision(True)
cdef local_sparsity_hybrid(double[:,:,::1] X_orig, Py_ssize_t freq_width_energy, Py_ssize_t freq_width_sparsity, Py_ssize_t time_width_energy, Py_ssize_t time_width_sparsity, double beta, double energy_criterium_db):

    cdef:
        Py_ssize_t P = X_orig.shape[0] # Spectrograms axis
        Py_ssize_t K = X_orig.shape[1] # Frequency axis
        Py_ssize_t M = X_orig.shape[2] # Time axis
        
        Py_ssize_t freq_width_energy_lobe = (freq_width_energy-1)//2
        Py_ssize_t freq_width_sparsity_lobe = (freq_width_sparsity-1)//2
        Py_ssize_t max_freq_width_lobe
        Py_ssize_t time_width_sparsity_lobe = (time_width_sparsity-1)//2
        Py_ssize_t time_width_energy_lobe = (time_width_energy-1)//2
        Py_ssize_t p, m, k, i, j

        double epsilon = 1e-10
        Py_ssize_t combined_size_sparsity = time_width_sparsity * freq_width_sparsity

    max_freq_width_lobe = freq_width_energy_lobe
    if freq_width_sparsity_lobe > max_freq_width_lobe:
        max_freq_width_lobe = freq_width_sparsity_lobe  
    
    X_orig_ndarray = np.asarray(X_orig)
    # Zero-pad spectrograms for windowing.
    X_ndarray = np.pad(X_orig, ((0, 0), (max_freq_width_lobe, max_freq_width_lobe), (time_width_sparsity_lobe, time_width_sparsity_lobe)))
    cdef double[:, :, :] X = X_ndarray

    # Containers for the hamming window (local sparsity) and the asymmetric hamming window (local energy)
    hamming_freq_energy_ndarray = np.hamming(freq_width_energy)
    hamming_freq_sparsity_ndarray = np.hamming(freq_width_sparsity)
    hamming_time_ndarray = np.hamming(time_width_sparsity)
    hamming_asym_time_ndarray = np.hamming(time_width_energy)
    hamming_asym_time_ndarray[time_width_energy_lobe+1:] = 0

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
    sparsity_ndarray = epsilon * np.ones(P, dtype=np.double) # Note that only one bin of sparsity information is stored each time.
    cdef double[:] sparsity = sparsity_ndarray
    cdef double arr_norm, gini

    # Container for the local energy.
    energy_ndarray = epsilon * np.ones((P, K, M), dtype=np.double)
    cdef double[:,:,:] energy = energy_ndarray


    # Variables referring to the last step (spectrograms combination).
    cdef double[:] log_sparsity
    cdef double sum_log_sparsity
    combination_weight_ndarray = np.empty(P, dtype=np.double)
    cdef double[:] combination_weight = combination_weight_ndarray
    cdef double min_local_energy
    cdef double weights_sum

    # Variable related to energy criterium.
    cdef double max_local_energy_db

    ############ Calculate local energy {{{ 

    for p in range(P):
        energy_ndarray[p] = correlate(X_orig_ndarray[p], hamming_energy, mode='same')

    energy = energy_ndarray

    ############ }}}

    ############ Hybrid combination {{{

    # Iterates through bins.
    for k in range(max_freq_width_lobe, K + max_freq_width_lobe):
        for m in range(time_width_sparsity_lobe, M + time_width_sparsity_lobe):
            red_k, red_m = k - max_freq_width_lobe, m - time_width_sparsity_lobe

            # Find the highest local energy in dB.
            max_local_energy_db = -INFINITY
            for p in range(P):
                if 10*log10(energy[p, red_k, red_m]) > max_local_energy_db:
                    max_local_energy_db = 10*log10(energy[p, red_k, red_m])
            
            # If this energy is below threshold, use binwise minimax.
            if max_local_energy_db < energy_criterium_db:
                result[red_k, red_m] = INFINITY
                for p in range(P):
                    if X[p, k, m] < result[red_k, red_m]:
                        result[red_k, red_m] = X[p, k, m]

            # Otherwise, calculate LS combination.
            else:
                for p in range(P):
                    # Copies the windowed region to the calculation vector, multiplying by the Hamming windows (horizontal and vertical).
                    for i in range(freq_width_sparsity):
                        for j in range(time_width_sparsity):
                            calc_vector[i*time_width_sparsity + j] = X[p, k - freq_width_sparsity_lobe + i, m - time_width_sparsity_lobe + j] * \
                                    hamming_freq_sparsity[i] * hamming_time[j]        

                    calc_vector_ndarray.sort()

                    # Calculates the local sparsity (Gini index).
                    arr_norm = 0.0
                    gini = 0.0
                    
                    for i in range(combined_size_sparsity):
                        arr_norm = arr_norm + calc_vector[i]
                        gini = gini - 2*calc_vector[i] * (combined_size_sparsity - i - 0.5)/ (<double> combined_size_sparsity)

                    gini = 1 + gini/(arr_norm + epsilon)

                    # Index for the local sparsity matrix must be adjusted because it has no zero-padding.
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















                
