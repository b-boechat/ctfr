import numpy as np
from scipy.signal import correlate
from itertools import chain
cimport cython
from libc.math cimport INFINITY, exp, pow
from ctfr.utils.arguments_check import _enforce_nonnegative, _enforce_odd_positive_integer

DEF DEBUGPRINT = 1

def _sls_i_wrapper(X, freq_width_energy=11, freq_width_sparsity=21, time_width_energy=11, time_width_sparsity=11, beta = 80):

    freq_width_energy = _enforce_odd_positive_integer(freq_width_energy, "freq_width_energy", 11)
    freq_width_sparsity = _enforce_odd_positive_integer(freq_width_sparsity, "freq_width_sparsity", 21)
    time_width_energy = _enforce_odd_positive_integer(time_width_energy, "time_width_energy", 11)
    time_width_sparsity = _enforce_odd_positive_integer(time_width_sparsity, "time_width_sparsity", 11)
    beta = _enforce_nonnegative(beta, "beta", 80.0)

    return _sls_i_cy(X, freq_width_energy, freq_width_sparsity, time_width_energy, time_width_sparsity, beta)

@cython.boundscheck(False)
@cython.wraparound(False) 
@cython.nonecheck(False)
@cython.cdivision(True)
cdef _sls_i_cy(double[:,:,::1] X_orig, Py_ssize_t freq_width_energy, Py_ssize_t freq_width_sparsity, Py_ssize_t time_width_energy, Py_ssize_t time_width_sparsity, double beta):

    cdef:
        Py_ssize_t P = X_orig.shape[0] # Spectrograms axis
        Py_ssize_t K = X_orig.shape[1] # Frequency axis
        Py_ssize_t M = X_orig.shape[2] # Time axis
        
        Py_ssize_t freq_width_energy_lobe = (freq_width_energy-1)//2
        Py_ssize_t freq_width_sparsity_lobe = (freq_width_sparsity-1)//2
        Py_ssize_t time_width_sparsity_lobe = (time_width_sparsity-1)//2
        Py_ssize_t time_width_energy_lobe = (time_width_energy-1)//2
        Py_ssize_t p, m, k, i, j

        double epsilon = 1e-10
        Py_ssize_t combined_size_sparsity = time_width_sparsity * freq_width_sparsity
    
    X_orig_ndarray = np.asarray(X_orig)
    # Zero-pad spectrograms for windowing.
    X_ndarray = np.pad(X_orig, ((0, 0), (freq_width_sparsity_lobe, freq_width_sparsity_lobe), (time_width_sparsity_lobe, time_width_sparsity_lobe)))
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
    sparsity_ndarray = np.zeros((P, K, M), dtype=np.double)
    cdef double[:,:,:] sparsity = sparsity_ndarray
    cdef double arr_norm, gini

    # Container for the local energy.
    energy_ndarray = np.empty((P, K, M), dtype=np.double)
    cdef double[:,:,:] energy = energy_ndarray

    # ----------- CHANGE THIS <<

    # Armazena o passo de interpolação em cada direção. i_steps[i, j] -> Interpolações para p = i. j = 0: na frequência; j = 1: no tempo
    i_steps_ndarray = np.array([[4, 1], [2, 2], [1, 4]], dtype=np.intp)
    cdef Py_ssize_t[:,:] i_steps = i_steps_ndarray

    # Variáveis referentes à combinação dos espectrogramas.
    cdef double[:,:] min_energy
    cdef Py_ssize_t[:,:] choosen_p
    cdef double[:, :, :] log_sparsity
    cdef double[:, :] sum_log_sparsity

    combination_weight_ndarray = np.empty((P, K, M), dtype=np.double)
    cdef double[:, :, :] combination_weight = combination_weight_ndarray

    # ------------ >>

    ############ Calculate local energy {{{ 

    for p in range(P):
        energy_ndarray[p] = correlate(X_orig_ndarray[p], hamming_energy, mode='same')

    energy = energy_ndarray

    ############ }}}

    ############ Compute local sparsity in non-interpolated region. {{{

    for p in range(P):
    
        # Itera pelas janelas de cálculo, levando em conta os passos de interpolação. TODO comment
        for red_k in chain(
                range(0, K, i_steps[p, 0]),
                range( (K - 1) // i_steps[p, 0] * i_steps[p, 0] + 1, K)
        ):
            for red_m in chain(
                    range(0, M, i_steps[p, 1]),
                    range( (M - 1) // i_steps[p, 1] * i_steps[p, 1] + 1, M)
            ):      
                k, m = red_k + freq_width_sparsity_lobe, red_m + time_width_sparsity_lobe

                # Copy the windowed region to the calculation vector, multiplying by the Hamming windows (horizontal and vertical).
                for i in range(freq_width_sparsity):
                    for j in range(time_width_sparsity):
                        calc_vector[i*time_width_sparsity + j] = X[p, k - freq_width_sparsity_lobe + i, m - time_width_sparsity_lobe + j] * \
                                hamming_freq_sparsity[i] * hamming_time[j]        
                
                # Calculate the local sparsity (Gini index)
                calc_vector_ndarray.sort()
                arr_norm = 0.0
                gini = 0.0
                
                for i in range(combined_size_sparsity):
                    arr_norm = arr_norm + calc_vector[i]
                    gini = gini - 2*calc_vector[i] * (combined_size_sparsity - i - 0.5)/ (<double> combined_size_sparsity)
                gini = 1 + gini/(arr_norm + epsilon)
                sparsity[p, red_k, red_m] = epsilon + gini

        # First interpolation (along k axis).
        for red_k in range(0, K, i_steps[p, 0]):
            for red_m in chain(
                    range(0, M, i_steps[p, 1]),
                    range( (M - 1) // i_steps[p, 1] * i_steps[p, 1] + 1, M)
            ):
                sparsity_step = (sparsity[p, red_k + i_steps[p, 0], red_m] - sparsity[p, red_k, red_m]) / i_steps[p, 0]
                for i in range(1, i_steps[p, 0]):
                    sparsity[p, red_k + i, red_m] = sparsity[p, red_k, red_m] + i * sparsity_step

        # Second interpolation (along m axis).
        for red_m in range(0, M, i_steps[p, 1]):
            for red_k in range(K):
                sparsity_step = (sparsity[p, red_k, red_m + i_steps[p, 1]] - sparsity[p, red_k, red_m]) / i_steps[p, 1]
                for j in range(1, i_steps[p, 1]):
                    sparsity[p, red_k, red_m + j] = sparsity[p, red_k, red_m] + j * sparsity_step  

    ############ }}}

    ### COMPLETE THIS FUNCTION AND CHECK BELOW. ###

    # ############ Combinação por Esparsidade Local e compensação por Energia Local {{
     
    if beta < 0: # Local Sparsity Method (not smoothed)
        
        min_energy_ndarray = np.min(energy_ndarray, axis=0)
        min_energy = min_energy_ndarray

        choosen_p_ndarray = np.argmax(sparsity_ndarray, axis=0)
        choosen_p = choosen_p_ndarray

        for k in range(K): 
            for m in range(M):
                result[k, m] = X_orig[choosen_p[k, m], k, m] * min_energy[k, m] / energy[p, k, m]

    else: # Smoothed Local Sparsity Method

        log_sparsity_ndarray = np.log(sparsity_ndarray)
        sum_log_sparsity_ndarray = np.sum(log_sparsity_ndarray, axis=0)

        log_sparsity = log_sparsity_ndarray
        sum_log_sparsity = sum_log_sparsity_ndarray

        for p in range(P):
            for k in range(K): 
                for m in range(M):
                    combination_weight[p, k, m] = exp( (2*log_sparsity[p, k, m] - sum_log_sparsity[k, m]) * beta)

        result_ndarray = np.average(X_orig_ndarray * np.min(energy_ndarray, axis=0)/energy_ndarray, axis=0, weights=combination_weight_ndarray)

    ############ }} Combinação por Esparsidade Local e compensação por Energia Local

    IF DEBUGPRINT:
        print("Energia")
        for p in range(P):
            print(f"Energia. p = {p}")
            print_arr(energy_ndarray[p])


    IF DEBUGTIMER:
        print(f"Time copy: {timer_copy/CLOCKS_PER_SEC}\nTime sort: {timer_sort/CLOCKS_PER_SEC}")

    return result_ndarray
                
