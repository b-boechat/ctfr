import ctfr
import sys
import numpy as np

def load_test_signal():

    signal, sr = ctfr.load("running_time/audio/guitarset_sample.wav", sr=22050, offset=5.0, duration=4.0)

    n_fft = 2048
    hop_length = 256

    spec_1 = ctfr.stft_spec(signal, win_length=512, n_fft=n_fft, hop_length=hop_length)
    spec_2 = ctfr.stft_spec(signal, win_length=1024, n_fft=n_fft, hop_length=hop_length)
    spec_3 = ctfr.stft_spec(signal, win_length=2048, n_fft=n_fft, hop_length=hop_length)

    return spec_1, spec_2, spec_3

def time_method(specs, method, num_iter=5, **kwargs):
    total_time = 0.0
    for _ in range(num_iter):
        swgm_spec, elapsed_time = ctfr.ctfr_from_specs(specs, method=method, **kwargs)
        total_time += elapsed_time
    average_time = total_time / num_iter
    return swgm_spec, average_time


def time_all_pipeline(num_iter):

    specs = load_test_signal()

    print("Execution time for each method and implementation:")

    print("\n==== Binwise minimum ====\n")
    _, average_time_ctfr = time_method(specs, method='min', num_iter=num_iter)
    print(f"ctfr: {average_time_ctfr:0.3f} s")
    
    print("\n==== SWGM ====\n")
    cspec_base, average_time_base = time_method(specs, method='baseline_swgm', num_iter=num_iter)
    print(f"Baseline: {average_time_base:0.3f} s")
    cspec_ctfr, average_time_ctfr = time_method(specs, method='swgm', num_iter=num_iter)
    print(f"ctfr: {average_time_ctfr:0.3f} s")
    assert np.allclose(cspec_base, cspec_ctfr)

    print("\n==== FLS ====\n")
    cspec_base, average_time_base = time_method(specs, method='baseline_fls', num_iter=num_iter)
    print(f"Baseline: {average_time_base:0.3f} s")
    cspec_ctfr, average_time_ctfr = time_method(specs, method='fls', num_iter=num_iter)
    print(f"ctfr: {average_time_ctfr:0.3f} s")
    assert np.allclose(cspec_base, cspec_ctfr)

    print("\n==== LT ====\n")
    cspec_base, average_time_base = time_method(specs, method='baseline_lt', num_iter=num_iter)
    print(f"Baseline: {average_time_base:0.3f} s")
    cspec_ctfr, average_time_ctfr = time_method(specs, method='lt', num_iter=num_iter)
    print(f"ctfr: {average_time_ctfr:0.3f} s")
    assert np.allclose(cspec_base, cspec_ctfr)

if __name__ == "__main__":
    if len(sys.argv) == 2:
        num_iter = int(sys.argv[1])
    else:
        num_iter = 5
    time_all_pipeline(num_iter)
