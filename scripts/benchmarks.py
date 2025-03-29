import ctfr
import sys
import numpy as np
from scipy.signal import correlate
from itertools import chain
from time import perf_counter

def load_test_signal(sample="guitarset", sr=22050, offset=5.0, duration=4.0, win_lengths=[512, 1024, 2048], n_fft=2048, hop_length=256):
    """Load the test signal for the benchmark experiments."""

    filename = ctfr.fetch_sample(sample)
    signal, _ = ctfr.load(filename, sr=sr, offset=offset, duration=duration)

    n_fft = n_fft
    hop_length = hop_length

    specs_tensor = np.array(
        [
            ctfr.stft_spec(
                signal, 
                win_length=win_length, 
                n_fft=n_fft, 
                hop_length=hop_length
            ) 
            for win_length in win_lengths
        ], dtype=np.double
    )

    return {"specs": specs_tensor, "duration": duration}


def benchmark_method(specs, method, num_iter, **kwargs):
    """ Benchmark the specified method for a given number of iterations."""

    total_time = 0.0
    for _ in range(num_iter):
        start_time = perf_counter()
        swgm_spec = ctfr.ctfr_from_specs(specs, method=method, **kwargs)
        elapsed_time = perf_counter() - start_time
        total_time += elapsed_time
    average_time = total_time / num_iter
    return swgm_spec, average_time

def compute_max_local_energy(specs, freq_width=11, time_width=11):
    """ Compute the maximum local energy among the spectrograms for each time-frequency bin. """

    epsilon=1e-10
    hamming_freq = np.hamming(freq_width)
    hamming_asym_time = np.hamming(time_width)
    hamming_asym_time[(time_width-1)//2:] = 0
    energy_window = np.outer(hamming_freq, hamming_asym_time)
    energy_window = energy_window/np.sum(energy_window, axis=None)

    local_energy = np.array([
        np.clip(correlate(spec, energy_window, mode='same')/np.sum(energy_window, axis=None), a_min=epsilon, a_max=None) for spec in specs
    ], dtype=np.double)

    return np.max(local_energy, axis=0)

def criterium_share(max_local_energy, energy_criterium_db):
    """ Compute the share of time-frequency bins that exceed the specified energy criterium. """

    energy_criterium = 10.0 ** (energy_criterium_db/10.0)
    return np.sum(max_local_energy >= energy_criterium)/max_local_energy.size

def non_interp_share(specs_shape, interp_steps):
    """ Compute the share of time-frequency bins in which the sparsity computation of SLS-I is not interpolated, for a given specification of the interpolation steps. """

    P, K, M = specs_shape
    total_non_interp = 0
    for p in range(P):
        k_len = len(list(chain(range(0, K, interp_steps[p, 0]), range( (K - 1) // interp_steps[p, 0] * interp_steps[p, 0] + 1, K))))
        m_len = len(list(chain(range(0, M, interp_steps[p, 1]), range( (M - 1) // interp_steps[p, 1] * interp_steps[p, 1] + 1, M))))
        total_non_interp += k_len * m_len
    return total_non_interp / (P * K * M)


def time_all_pipeline(num_iter):
    """ Benchmark all methods and implementations. """
    
    test_sig_dict = load_test_signal()
    specs = test_sig_dict["specs"]
    duration = test_sig_dict["duration"]

    print("Execution time for each method and implementation:")

    print("\n==== Binwise minimum ====\n")
    _, average_time_ctfr = benchmark_method(specs, method='min', num_iter=num_iter)
    print(f"ctfr: {average_time_ctfr:0.3f} s -- {100*average_time_ctfr/duration:0.2f}% real-time")
    
    print("\n==== SWGM ====\n")
    cspec_base, average_time_base = benchmark_method(specs, method='baseline_swgm', num_iter=num_iter)
    print(f"Baseline: {average_time_base:0.3f} s -- {100*average_time_base/duration:0.2f}% real-time")
    cspec_ctfr, average_time_ctfr = benchmark_method(specs, method='swgm', num_iter=num_iter)
    print(f"ctfr: {average_time_ctfr:0.3f} s -- {100*average_time_ctfr/duration:0.2f}% real-time")
    assert np.allclose(cspec_base, cspec_ctfr)

    print("\n==== FLS ====\n")
    cspec_base, average_time_base = benchmark_method(specs, method='baseline_fls', num_iter=num_iter)
    print(f"Baseline: {average_time_base:0.3f} s -- {100*average_time_base/duration:0.2f}% real-time")
    cspec_ctfr, average_time_ctfr = benchmark_method(specs, method='fls', num_iter=num_iter)
    print(f"ctfr: {average_time_ctfr:0.3f} s -- {100*average_time_ctfr/duration:0.2f}% real-time")
    assert np.allclose(cspec_base, cspec_ctfr)

    print("\n==== SLS ====\n")
    cspec_base, average_time_base = benchmark_method(specs, method='baseline_sls', num_iter=num_iter)
    print(f"Baseline: {average_time_base:0.3f} s -- {100*average_time_base/duration:0.2f}% real-time")
    cspec_ctfr, average_time_ctfr = benchmark_method(specs, method='sls_h', num_iter=num_iter, energy_criterium_db=-200)

    max_local_energy = compute_max_local_energy(specs)

    cspec_ctfr, average_time_ctfr = benchmark_method(specs, method='sls_h', num_iter=num_iter, energy_criterium_db=-60)
    print(f"SLS-H (-60): {average_time_ctfr:0.3f} s -- {100*average_time_ctfr/duration:0.2f}% real-time -- {100*criterium_share(max_local_energy, -60):.2f}% SLS")
    cspec_ctfr, average_time_ctfr = benchmark_method(specs, method='sls_h', num_iter=num_iter, energy_criterium_db=-40)
    print(f"SLS-H (-40): {average_time_ctfr:0.3f} s -- {100*average_time_ctfr/duration:0.2f}% real-time -- {100*criterium_share(max_local_energy, -40):.2f}% SLS")
    cspec_ctfr, average_time_ctfr = benchmark_method(specs, method='sls_h', num_iter=num_iter, energy_criterium_db=-20)
    print(f"SLS-H (-20): {average_time_ctfr:0.3f} s -- {100*average_time_ctfr/duration:0.2f}% real-time -- {100*criterium_share(max_local_energy, -20):.2f}% SLS")

    interp_steps_default = np.array([[4, 1], [2, 2], [1, 4]])
    interp_steps_double = np.array([[8, 2], [4, 4], [2, 8]])
    cspec_ctfr, average_time_ctfr = benchmark_method(specs, method='sls_i', num_iter=num_iter, interp_steps=interp_steps_default)
    print(f"SLS-I (default): {average_time_ctfr:0.3f} s -- {100*average_time_ctfr/duration:0.2f}% real-time -- {100*non_interp_share(specs.shape, interp_steps_default):.2f}% SLS")
    cspec_ctfr, average_time_ctfr = benchmark_method(specs, method='sls_i', num_iter=num_iter, interp_steps=interp_steps_double)
    print(f"SLS-I (doubled): {average_time_ctfr:0.3f} s -- {100*average_time_ctfr/duration:0.2f}% real-time -- {100*non_interp_share(specs.shape, interp_steps_double):.2f}% SLS")


if __name__ == "__main__":
    if len(sys.argv) == 2:
        num_iter = int(sys.argv[1])
    else:
        num_iter = 5
    time_all_pipeline(num_iter)
