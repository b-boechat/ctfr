import numpy as np
cimport cython
from libc.math cimport INFINITY, sqrt, pow
from warnings import warn
from tfrc.warning import ParameterChangeWarning

def _lt_wrapper(X, freq_width = 21, time_width = 11, eta = 0.8):
    """ Calculate the "Lukin-Todd" (LT) combination of spectrograms. 
        
        :param X (Ndarray <double> [P x K x M]): Spectrograms tensor. 
            Dimensions: spectrograms P x frequency bins K x time frames M.
        :param freq_width (Odd integer): Smearing window length in frequency.
        :param time_width (Odd integer): Smearing window length in time.
        :param eta (Double >= 0): Parameter for calculating combination weights. Example value: eta = 8.0.
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
    
    eta = float(eta)
    if eta < 0:
        eta = 0.0
        warn(f"The 'eta' parameter should be a non-negative float. Changing to 0.", ParameterChangeWarning)

    return _lt_cy(X, freq_width, time_width, eta)

@cython.boundscheck(False)
@cython.wraparound(False) 
@cython.nonecheck(False)
@cython.cdivision(True)
cdef _lt_cy(double[:,:,::1] X_orig, Py_ssize_t freq_width, Py_ssize_t time_width, double eta):

    cdef:
        Py_ssize_t P = X_orig.shape[0] # Spectrograms axis.
        Py_ssize_t K = X_orig.shape[1] # Frequency axis.
        Py_ssize_t M = X_orig.shape[2] # Time axis.
        
        Py_ssize_t freq_width_lobe = (freq_width-1)//2
        Py_ssize_t time_width_lobe = (time_width-1)//2
        Py_ssize_t p, m, k, i_sort, j_sort, i, j
        double key

        double epsilon = 1e-10 # Small value used to avoid 0 in some computations.

    # Zero-pad spectrograms for windowing.
    X_ndarray = np.pad(X_orig, ((0, 0), (freq_width_lobe, freq_width_lobe), (time_width_lobe, time_width_lobe)))
    cdef double[:, :, :] X = X_ndarray

    # Container that stores an horizontal segment of a spectrogram, with all frequency bins. Used to calculate smearing. 
    calc_region_ndarray = np.zeros((K + 2*freq_width_lobe, time_width), dtype = np.double)
    cdef double[:, :] calc_region = calc_region_ndarray 

    # Container that stores the result.
    result_ndarray = np.zeros((K, M), dtype=np.double)
    cdef double[:, :] result = result_ndarray

    # Variables related to creating and merging calculation vectors.
    cdef:
        Py_ssize_t num_vectors = freq_width
        Py_ssize_t len_vectors = time_width
        Py_ssize_t combined_size = freq_width*time_width
        Py_ssize_t j_parent, j_left_child, j_right_child, j_smaller_child, o
        Py_ssize_t element_origin, origin_index
        double inclusion_scalar, exclusion_scalar
        Py_ssize_t combined_index, previous_comb_index
        Py_ssize_t inclusion_index, exclusion_index

    # Containers related to the "merging" of sorted vectors using a heap. {

    # Heap that stores the smallest "nonconsumed" element of each vector in the merging.
    heap_elements_ndarray = np.empty(num_vectors, dtype=np.double)
    cdef double[:] heap_elements = heap_elements_ndarray 
    # Stores the vector of origin for each corresponding element in the heap.
    heap_origins_ndarray = np.empty(num_vectors, dtype=np.intp)
    cdef Py_ssize_t[:] heap_origins = heap_origins_ndarray 
    # Stores current index for each vector.
    array_indices_ndarray = np.empty(num_vectors, dtype=np.intp)
    cdef Py_ssize_t[:] array_indices = array_indices_ndarray 
    # Stores the combined vector on even iterations.
    combined_even_ndarray = np.empty(combined_size, dtype=np.double)  
    cdef double[:] combined_even = combined_even_ndarray
    # Stores the combined vector on odd iterations.
    combined_odd_ndarray = np.empty(combined_size, dtype=np.double)  
    cdef double[:] combined_odd = combined_odd_ndarray 

    # Memviews that point to either combined_even or combined_odd, alternating every iteration.
    cdef double[:] combined
    cdef double[:] previous_combined

    # }

    # Container that stores the local smearing.
    smearing_ndarray = np.zeros((P, K, M), dtype=np.double)
    cdef double[:,:,:] smearing = smearing_ndarray

    # Variables related to smearing calculation.
    cdef double smearing_numerator, smearing_denominator

    # Variables related to spectrogram combination.
    cdef double weight, weights_sum, result_acc

    ############ Local smearing calculation {{{

    for p in range(P):
        # Copies the initial horizontal segment to the container "calc_region".
        for k in range(freq_width_lobe, K + freq_width_lobe):
            for i in range(time_width):
                calc_region[k, i] = X[p, k, i]
        # Iterates through the segments.
        for m in range(time_width_lobe, M + time_width_lobe):
            if m == time_width_lobe:

                 ##### Sorts the horizontal vectors from scratch (only done once per spectrogram, for the leftmost segment vectors.) {{
                for k in range(freq_width_lobe, K + freq_width_lobe):
                    # Sort the horizontal vector. For usual values of time_width, it's faster to sort with this insertion sort code than using NumPy.
                    for i_sort in range(1, time_width):
                        key = calc_region[k, i_sort]
                        j_sort = i_sort - 1
                        while j_sort >= 0 and key < calc_region[k, j_sort]:
                            calc_region[k, j_sort + 1] = calc_region[k, j_sort]
                            j_sort = j_sort - 1
                        calc_region[k, j_sort + 1] = key
                    # NumPy alternative:
                    #calc_region_ndarray.sort()
                ##### }}

            else:

                #### Obtains the next horizontal vectors, including the element at m + time_width_lobe and excluding the one at m - time_width_lobe - 1 {{
                for k in range(freq_width_lobe, K + freq_width_lobe):
                    inclusion_scalar = X[p, k, m + time_width_lobe] #
                    exclusion_scalar = X[p, k, m - time_width_lobe - 1]
                    i_sort = time_width - 1
                    while calc_region[k, i_sort] != exclusion_scalar:
                        if inclusion_scalar > calc_region[k, i_sort]:
                            calc_region[k, i_sort], inclusion_scalar = inclusion_scalar, calc_region[k, i_sort]

                        i_sort = i_sort - 1
                    i_sort = i_sort - 1
                    while inclusion_scalar < calc_region[k, i_sort] and i_sort >= 0:
                        calc_region[k, i_sort + 1] = calc_region[k, i_sort]
                        i_sort = i_sort - 1
                    calc_region[k, i_sort + 1] = inclusion_scalar 
                ##### }}

            ##### Performs the first merge of sorted vectors, using a heap. {{
            combined = combined_odd
            previous_combined = combined_even
                
            for i in range(num_vectors):
                ### Initializes the heap with the first (i.e. the smallest) element of each vector {
                heap_elements[i] = calc_region[i, 0]
                heap_origins[i] = i
                array_indices[i] = 0
                ### }

                ### Heapify up. {
                j = i
                j_parent = (j - 1) // 2
                while j_parent >= 0 and heap_elements[j_parent] > heap_elements[j]:
                    heap_elements[j_parent], heap_elements[j] = heap_elements[j], heap_elements[j_parent]
                    heap_origins[j_parent], heap_origins[j] = i, heap_origins[j_parent]

                    j = j_parent
                    j_parent = (j - 1) // 2
                ### }
            for o in range(combined_size):
                ### Pops the first element from the heap {
                combined[o] = heap_elements[0]
                element_origin = heap_origins[0]
                array_indices[element_origin] += 1
                origin_index = array_indices[element_origin]
                if origin_index >= len_vectors:
                    heap_elements[0] = INFINITY
                else:
                    heap_elements[0] = calc_region[element_origin, origin_index]
                ### }

                ### Heapify down {           
                j = 0
                j_left_child = 2*j + 1
                while j_left_child < num_vectors:
                    j_smaller_child = j_left_child
                    j_right_child = j_left_child + 1
                    if j_right_child < num_vectors and heap_elements[j_right_child] < heap_elements[j_left_child]:
                        j_smaller_child = j_right_child

                    if heap_elements[j] <= heap_elements[j_smaller_child]:
                        break
                    
                    heap_elements[j], heap_elements[j_smaller_child] = heap_elements[j_smaller_child], heap_elements[j]
                    heap_origins[j], heap_origins[j_smaller_child] = heap_origins[j_smaller_child], heap_origins[j]

                    j = j_smaller_child
                    j_left_child = 2*j + 1
                ### }

            ##### }}

            ### Calculates the local smearing function. {{
            smearing_denominator = 0.0
            smearing_numerator = 0.0
            for o in range(combined_size):
                smearing_denominator = smearing_denominator + combined[o]
                smearing_numerator = smearing_numerator + (combined_size - o)*combined[o]
            smearing[p, 0, m - time_width_lobe] = smearing_numerator/(sqrt(smearing_denominator) + epsilon)
            ### }}

            # Iterates through frequency slices, except the first.
            for k in range(freq_width_lobe + 1, K + freq_width_lobe):
                ### Merge with exclusion. It's the most computationally intensive part of the algorithm. {{
                combined, previous_combined = previous_combined, combined

                previous_comb_index = 0
                combined_index = 0
                inclusion_index = 0
                exclusion_index = 0

                for o in range(combined_size + len_vectors):
                    if previous_comb_index >= combined_size:
                        # If the elements of "previous_combined" have already been exhausted, pop an element from "inclusion".
                        combined[combined_index] = calc_region[k + freq_width_lobe, inclusion_index]
                        combined_index = combined_index + 1
                        inclusion_index = inclusion_index + 1
                    elif exclusion_index < len_vectors and previous_combined[previous_comb_index] == calc_region[k - freq_width_lobe - 1, exclusion_index]:
                        # # Skip the element from previous_combined that belongs to "exclusion".
                        previous_comb_index = previous_comb_index + 1
                        exclusion_index = exclusion_index + 1
                    elif inclusion_index >= len_vectors or previous_combined[previous_comb_index] <= calc_region[k + freq_width_lobe, inclusion_index]:
                         # If the elements of "inclusion" have already been exhausted, or if the current element of "previous_combined" is smaller than that of "inclusion", pop an element from "previous_combined".
                        combined[combined_index] = previous_combined[previous_comb_index]
                        combined_index = combined_index + 1
                        previous_comb_index = previous_comb_index + 1
                    else:
                        # Lastly, if the current element of "inclusion" is smaller than that of "previous_combined", pop an element from "inclusion".
                        combined[combined_index] = calc_region[k + freq_width_lobe, inclusion_index]
                        combined_index = combined_index + 1
                        inclusion_index = inclusion_index + 1

                ### }}

                ### Calculate smearing function {{
                smearing_denominator = 0.0
                smearing_numerator = 0.0
                for o in range(combined_size):
                    smearing_denominator = smearing_denominator + combined[o]
                    smearing_numerator = smearing_numerator + (combined_size-o)*combined[o]
                smearing[p, k - freq_width_lobe, m - time_width_lobe] = smearing_numerator/(sqrt(smearing_denominator) + epsilon)
                
                ### }}
    
    ############ }}}

    ############ Spectrograms weighted combination {{{

    for k in range(K):
        for m in range(M):
            weights_sum = 0.0
            result_acc = 0.0
            for p in range(P):
                weight = 1./(pow(smearing[p, k, m], eta) + epsilon)
                result_acc = result_acc + weight * X_orig[p, k, m]
                weights_sum = weights_sum + weight
            result[k, m] = result_acc / weights_sum

    ############ }}}

    return result_ndarray















                
