import ctfr
import sys
import numpy as np
from scipy.signal import correlate

def load_test_signal():

    signal, _ = ctfr.load("running_time/audio/guitarset_sample.wav", sr=22050, offset=5.0, duration=4.0)

    n_fft = 2048
    hop_length = 256

    spec_1 = ctfr.stft_spec(signal, win_length=512, n_fft=n_fft, hop_length=hop_length)
    spec_2 = ctfr.stft_spec(signal, win_length=1024, n_fft=n_fft, hop_length=hop_length)
    spec_3 = ctfr.stft_spec(signal, win_length=2048, n_fft=n_fft, hop_length=hop_length)

    print(f"Specs shape: {spec_1.shape}, {spec_2.shape}, {spec_3.shape}")

    return {"specs": (spec_1, spec_2, spec_3), "duration": 4.0}

def time_method(specs, method, num_iter=5, **kwargs):
    total_time = 0.0
    for _ in range(num_iter):
        swgm_spec, elapsed_time = ctfr.ctfr_from_specs(specs, method=method, **kwargs)
        total_time += elapsed_time
    average_time = total_time / num_iter
    return swgm_spec, average_time

def compute_max_local_energy(specs, freq_width=11, time_width=11):
    epsilon=1e-10

    hamming_freq = np.hamming(freq_width)
    hamming_asym_time = np.hamming(time_width)
    hamming_asym_time[(time_width-1)//2:] = 0
    energy_window = np.outer(hamming_freq, hamming_asym_time)
    energy_window = energy_window/np.sum(energy_window, axis=None)

    local_energy = np.array([
        np.clip(correlate(spec, energy_window, mode='same')/np.sum(energy_window, axis=None), a_min=epsilon, a_max=None) for spec in specs
    ], dtype=np.double)

    print("shape", local_energy.shape)

    return np.max(local_energy, axis=0)


def criterium_share(max_local_energy, energy_criterium_db):
    energy_criterium = 10.0 ** (energy_criterium_db/10.0)
    
    return np.sum(max_local_energy >= energy_criterium)/max_local_energy.size


def time_all_pipeline(num_iter):

    test_sig_dict = load_test_signal()
    specs = test_sig_dict["specs"]
    duration = test_sig_dict["duration"]

    print("Execution time for each method and implementation:")

    print("\n==== Binwise minimum ====\n")
    _, average_time_ctfr = time_method(specs, method='min', num_iter=num_iter)
    print(f"ctfr: {average_time_ctfr:0.3f} s -- {100*average_time_ctfr/duration:0.2f}% real-time")
    
    print("\n==== SWGM ====\n")
    cspec_base, average_time_base = time_method(specs, method='baseline_swgm', num_iter=num_iter)
    print(f"Baseline: {average_time_base:0.3f} s -- {100*average_time_base/duration:0.2f}% real-time")
    cspec_ctfr, average_time_ctfr = time_method(specs, method='swgm', num_iter=num_iter)
    print(f"ctfr: {average_time_ctfr:0.3f} s -- {100*average_time_ctfr/duration:0.2f}% real-time")
    assert np.allclose(cspec_base, cspec_ctfr)

    print("\n==== FLS ====\n")
    cspec_base, average_time_base = time_method(specs, method='baseline_fls', num_iter=num_iter)
    print(f"Baseline: {average_time_base:0.3f} s -- {100*average_time_base/duration:0.2f}% real-time")
    cspec_ctfr, average_time_ctfr = time_method(specs, method='fls', num_iter=num_iter)
    print(f"ctfr: {average_time_ctfr:0.3f} s -- {100*average_time_ctfr/duration:0.2f}% real-time")
    assert np.allclose(cspec_base, cspec_ctfr)

    print("\n==== SLS ====\n")
    cspec_base, average_time_base = time_method(specs, method='baseline_sls', num_iter=num_iter)
    print(f"Baseline: {average_time_base:0.3f} s -- {100*average_time_base/duration:0.2f}% real-time")
    cspec_ctfr, average_time_ctfr = time_method(specs, method='sls_h', num_iter=num_iter, energy_criterium_db=-200)

    max_local_energy = compute_max_local_energy(specs)

    cspec_ctfr, average_time_ctfr = time_method(specs, method='sls_h', num_iter=num_iter, energy_criterium_db=-60)
    print(f"Hybrid (-60): {average_time_ctfr:0.3f} s -- {100*average_time_ctfr/duration:0.2f}% real-time -- {100*criterium_share(max_local_energy, -60):.2f}% SLS")
    cspec_ctfr, average_time_ctfr = time_method(specs, method='sls_h', num_iter=num_iter, energy_criterium_db=-40)
    print(f"Hybrid (-40): {average_time_ctfr:0.3f} s -- {100*average_time_ctfr/duration:0.2f}% real-time -- {100*criterium_share(max_local_energy, -40):.2f}% SLS")
    cspec_ctfr, average_time_ctfr = time_method(specs, method='sls_h', num_iter=num_iter, energy_criterium_db=-20)
    print(f"Hybrid (-20): {average_time_ctfr:0.3f} s -- {100*average_time_ctfr/duration:0.2f}% real-time -- {100*criterium_share(max_local_energy, -20):.2f}% SLS")


if __name__ == "__main__":
    if len(sys.argv) == 2:
        num_iter = int(sys.argv[1])
    else:
        num_iter = 5
    time_all_pipeline(num_iter)
