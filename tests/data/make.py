import tfrc
import json
import os
import numpy as np

def make_sample_stft_specs():

    output_path = "sample_stft_specs.json"
    if os.path.exists(output_path):
        raise FileExistsError(f"File already exists: {output_path}")

    signal, _ = tfrc.load(
        "sample_file_4.wav", 
        sr=22050, 
        mono=True, 
        duration=1.0,
        dtype=np.double,
        res_type='soxr_hq'
    )
    specs_tensor = np.array(
        [
            tfrc.stft_spec(
                signal, 
                n_fft = 2048,
                hop_length = 512,
                win_length = win_length,
                center = True,
                dtype=np.double,
                pad_mode='constant'
            )
            for win_length in [512, 1024, 2048]
        ]
    )

    with open(output_path, "w") as f:
        json.dump(specs_tensor.tolist(), f)
    print(f"Successfully created file: {output_path}.")

def make(arg):
    if arg == "sample_stft_specs":
        make_sample_stft_specs()
    
    else:
        raise ValueError(f"Invalid argument: {arg}")

if __name__ == "__main__":
    import sys
    make(sys.argv[1])