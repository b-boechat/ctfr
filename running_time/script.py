import ctfr
import sys

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
    for i in range(num_iter):
        swgm_spec, elapsed_time = ctfr.ctfr_from_specs(specs, method=method, **kwargs)
        total_time += elapsed_time
    average_time = total_time / num_iter
    return average_time


def time_all_pipeline(num_iter):

    specs = load_test_signal()

    print("Execution time for each method and implementation:")
    
    print("\n==== SWGM ====\n")
    print(f"Baseline: {time_method(specs, method='baseline_swgm', num_iter=5):0.3f} s")
    print(f"ctfr: {time_method(specs, method='swgm'):0.3f} s")

    print("\n==== LT ====\n")
    print(f"Baseline: {time_method(specs, method='baseline_lt', num_iter=5):0.3f} s")
    print(f"ctfr: {time_method(specs, method='lt', num_iter=5):0.3f} s")

if __name__ == "__main__":
    if len(sys.argv) == 2:
        num_iter = int(sys.argv[1])
    else:
        num_iter = 5
    time_all_pipeline(num_iter)