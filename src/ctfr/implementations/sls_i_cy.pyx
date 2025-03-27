import numpy as np
from scipy.signal import correlate
from itertools import chain
cimport cython
from libc.math cimport exp
from ctfr.utils.arguments_check import _enforce_nonnegative, _enforce_odd_positive_integer
from ctfr.exception import InvalidArgumentError, ArgumentRequiredError

def _sls_i_wrapper(
        X, 
        lek = 11, 
        lsk = 21, 
        lem = 11, 
        lsm = 11, 
        beta = 80,
        interp_steps = None,
        _info = None
):

    lek = _enforce_odd_positive_integer(lek, "lek", 11)
    lsk = _enforce_odd_positive_integer(lsk, "lsk", 21)
    lem = _enforce_odd_positive_integer(lem, "lem", 11)
    lsm = _enforce_odd_positive_integer(lsm, "lsm", 11)
    beta = _enforce_nonnegative(beta, "beta", 80.0)

    interp_steps = _get_interp_steps(X.shape[0], _info, interp_steps)

    return _sls_i_cy(X, lek, lsk, lem, lsm, beta, interp_steps)

def _get_interp_steps(num_specs, _info, user_interp_steps):

    if user_interp_steps is not None:
        interp_steps = np.ascontiguousarray(user_interp_steps, dtype=int)
        if interp_steps.shape[0] != num_specs or interp_steps.shape[1] != 2:
            raise InvalidArgumentError("The dimensions of 'interp_steps' must be P x 2, where P is the number of spectrograms to combine.")
        return interp_steps

    if _info is not None:
        if _info["representation_type"] == "stft":
            n_fft, hop_length = _info["n_fft"], _info["hop_length"]
            return np.clip(
                np.array(
                    [[n_fft//l, l//(2*hop_length)] for l in _info["win_lengths"]], 
                    dtype=int
                ), 
            a_min=1, a_max=None)
        else: # "cqt"
            # This might change in the future.
            raise ArgumentRequiredError("When performing SLS-I with CQT spectrograms, specifying 'interp_steps' is required. Note that SLS-I is not recommended for combining CQT spectrograms and you should probably use another combination method.")
            
    raise ArgumentRequiredError("When calling SLS-I directly from spectrograms, specifying 'interp_steps' is required.")

@cython.boundscheck(False)
@cython.wraparound(False) 
@cython.nonecheck(False)
@cython.cdivision(True)
cdef _sls_i_cy(double[:,:,::1] X_orig, Py_ssize_t lek, Py_ssize_t lsk, Py_ssize_t lem, Py_ssize_t lsm, double beta, long[:,::1] interp_steps):

    cdef:
        Py_ssize_t P = X_orig.shape[0] # Spectrograms axis
        Py_ssize_t K = X_orig.shape[1] # Frequency axis
        Py_ssize_t M = X_orig.shape[2] # Time axis
        
        Py_ssize_t lek_lobe = (lek-1)//2
        Py_ssize_t lsk_lobe = (lsk-1)//2
        Py_ssize_t lsm_lobe = (lsm-1)//2
        Py_ssize_t lem_lobe = (lem-1)//2
        Py_ssize_t p, m, k, i, j, red_k, red_m

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

    # Containers and variables related to local sparsity calculation.
    sparsity_ndarray = np.zeros((P, K, M), dtype=np.double) # TODO change to empty.
    cdef double[:,:,:] sparsity = sparsity_ndarray
    cdef double arr_norm, gini

    # Container for the local energy.
    energy_ndarray = np.zeros((P, K, M), dtype=np.double)
    cdef double[:,:,:] energy = energy_ndarray


    # Armazena o passo de interpolação em cada direção. i_steps[i, j] -> Interpolações para p = i. j = 0: na frequência; j = 1: no tempo
    cdef long[:,:] i_steps = interp_steps

    # Variables related to the last step (spectrograms combination).
    cdef double[:, :, :] log_sparsity
    cdef double[:, :] sum_log_sparsity
    combination_weight_ndarray = np.zeros((P, K, M), dtype=np.double)
    cdef double[:, :, :] combination_weight = combination_weight_ndarray

    # ------------ >>

    ############ Calculate local energy {{{ 

    for p in range(P):
        energy_ndarray[p] = np.clip(correlate(X_orig_ndarray[p], hamming_energy, mode="same")/np.sum(hamming_energy, axis=None), a_min=epsilon, a_max=None)

    energy = energy_ndarray

    ############ }}}

    ############ Compute local sparsity {{{

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
                k, m = red_k + lsk_lobe, red_m + lsm_lobe

                # Copy the windowed region to the calculation vector, multiplying by the Hamming windows (horizontal and vertical).
                for i in range(lsk):
                    for j in range(lsm):
                        calc_vector[i*lsm + j] = X[p, k - lsk_lobe + i, m - lsm_lobe + j] * \
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
        red_k = i_steps[p, 0]
        while red_k < K: # Loop equivalent to "for red_k in range(i_steps[p, 0], K, i_steps[p, 0])". The current variant produces a faster code in Cython.
            for red_m in chain(
                    range(0, M, i_steps[p, 1]),
                    range( (M - 1) // i_steps[p, 1] * i_steps[p, 1] + 1, M)
            ):
                sparsity_step = (sparsity[p, red_k, red_m] - sparsity[p, red_k - i_steps[p, 0], red_m]) / i_steps[p, 0]
                for i in range(1, i_steps[p, 0]):
                    sparsity[p, red_k - i, red_m] = sparsity[p, red_k - i + 1, red_m] - sparsity_step
            
            red_k = red_k + i_steps[p, 0]

        # Second interpolation (along m axis).
        red_m = i_steps[p, 1]
        while red_m < M: # Loop equivalent to "for red_m in range(i_steps[p, 1], M, i_steps[p, 1])". The current variant produces a faster code in Cython.
            for red_k in range(K):
                sparsity_step = (sparsity[p, red_k, red_m] - sparsity[p, red_k, red_m - i_steps[p, 1]]) / i_steps[p, 1]
                for j in range(1, i_steps[p, 1]):
                    sparsity[p, red_k, red_m - j] = sparsity[p, red_k, red_m - j + 1] - sparsity_step  

            red_m = red_m + i_steps[p, 1]


    ############ }}}

    ############ Smoothed local sparsity combination {{
     

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

    return result_ndarray
                
