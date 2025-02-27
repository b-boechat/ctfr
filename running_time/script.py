import ctfr

def load_placeholder():

    signal, _ = ctfr.load("running_time/audio/placeholder.wav")

    n_fft = 2048
    hop_length = 256


    spec_1 = ctfr.stft_spec(signal, win_length=512, n_fft=n_fft, hop_length=hop_length)
    spec_2 = ctfr.stft_spec(signal, win_length=1024, n_fft=n_fft, hop_length=hop_length)
    spec_3 = ctfr.stft_spec(signal, win_length=2048, n_fft=n_fft, hop_length=hop_length)

    assert spec_1.shape == spec_2.shape
    assert spec_1.shape == spec_3.shape

    return spec_1, spec_2, spec_3


def time_method(load_function, method, num_iter=5, **kwargs):
    spec_1, spec_2, spec_3 = load_function()

    total_time = 0.0
    for i in range(num_iter):
        swgm_spec, elapsed_time = ctfr.ctfr_from_specs((spec_1, spec_2, spec_3), method=method, **kwargs)
        total_time += elapsed_time
    average_time = total_time / num_iter

    print(f"Method {method} - Averaged elapsed time: {average_time}")

if __name__ == "__main__":
    time_method(
        load_function=load_placeholder,
        method='swgm',
        num_iter=5
    )

    time_method(
        load_function=load_placeholder,
        method='baseline_swgm',
        num_iter=5
    )

    time_method(
        load_function=load_placeholder,
        method='lt',
        num_iter=5
    )

    time_method(
        load_function=load_placeholder,
        method='baseline_lt',
        num_iter=5
    )