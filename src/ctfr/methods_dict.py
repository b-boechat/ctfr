from ctfr.implementations.swgm_cy import _swgm_wrapper
from ctfr.implementations.fls_cy import _fls_wrapper
from ctfr.implementations.lt_cy import _lt_wrapper
from ctfr.implementations.sls_cy import _sls_wrapper
from ctfr.implementations.binwise_np import _mean_wrapper, _hmean_wrapper, _gmean_wrapper, _min_wrapper

_methods_dict = {
    "mean": {
        "name": "Binwise mean",
        "function": _mean_wrapper,
        "citations": ['C. Detka, P. Loughlin, and A. El-Jaroudi, “On combining evolutionary spectral estimates,” in IEEE Seventh SP Workshop on Statistical Signal and Array Processing, Jun. 1994, pp. 243–246.'],
        "parameters": {}
    },
    "hmean": {
        "name": "Binwise harmonic mean",
        "function": _hmean_wrapper,
        "citations": ['C. Detka, P. Loughlin, and A. El-Jaroudi, “On combining evolutionary spectral estimates,” in IEEE Seventh SP Workshop on Statistical Signal and Array Processing, Jun. 1994, pp. 243–246.'],
        "parameters": {}
    },
    "gmean": {
        "name": "Binwise geometric mean",
        "function": _gmean_wrapper,
        "citations": ['P. Loughlin, J. Pitton, and B. Hannaford, “Approximating time-frequency density functions via optimal combinations of spectrograms,” IEEE Signal Processing Letters, vol. 1, no. 12, pp. 199–202, Dec. 1994.'],
        "parameters": {}
    },
    "min": {
        "name": "Binwise minimum",
        "function": _min_wrapper,
        "citations": ['P. Loughlin, J. Pitton, and B. Hannaford, “Approximating time-frequency density functions via optimal combinations of spectrograms,” IEEE Signal Processing Letters, vol. 1, no. 12, pp. 199–202, Dec. 1994.'],
        "parameters": {}
    },
    "swgm": {
        "name": "Sample-weighted geometric mean (SWGM)",
        "function": _swgm_wrapper,
        "citations": ['M. d. V. M. da Costa and L. W. P. Biscainho, “Combining time-frequency representations for music information retrieval,” in 15th AES-Brasil Engineering Congress. Florianópolis, Brazil: Audio Engineering Society, Oct. 2017, pp. 12–18.'],
        "parameters": {
            "beta": {
                "type_and_info": r"float, range: [0, 1]",
                "description": r"Factor used in the computation of weights for the geometric mean. When ``beta = 0``, the SWGM is equivalent to an unweighted geometric mean. When ``beta = 1``, the SWGM is equivalent to the minimum combination. Defaults to 0.3."
            },
            "max_gamma": {
                "type_and_info": r"float >= 1",
                "description": r"Maximum weight for the geometric mean. This parameter is used to avoid numerical instability when the weights are too large. Defaults to 20."
            }
        }
    },
    "fls": {
        "name": "Fast local sparsity (FLS)",
        "function": _fls_wrapper,
        "citations": ['M. d. V. M. da Costa and L. W. P. Biscainho, “The fast local sparsity method: A low-cost combination of time-frequency representations based on the hoyer sparsity,” Journal of the Audio Engineering Society, vol. 70, no. 9, pp. 698–707, Sep. 2022.'],
        "parameters": {
            "freq_width": {
                "type_and_info": r"int > 0, odd",
                "description": r"Width in frequency bins of the analysis window used in the local sparsity computation. Defaults to 21."
            },
            "time_width": {
                "type_and_info": r"int > 0, odd",
                "description": r"Width in time frames of the analysis window used in the local sparsity computation. Defaults to 11."
            },
            "gamma": {
                "type_and_info": r"float >= 0",
                "description": r"Factor used in the computation of combination weights. Defaults to 20."
            }
        }
    },
    "lt": {
        "name": "Lukin-Todd (LT)",
        "function": _lt_wrapper,
        "citations": ['A. Lukin and J. G. Todd, “Adaptive time-frequency resolution for analysis and processing of audio,” in 120th Audio Engineering Society Convention. Paris, France: Audio Engineering Society, May 2006.'],
        "parameters": {
            "freq_width": {
                "type_and_info": r"int > 0, odd",
                "description": r"Width in frequency bins of the analysis window used in the local energy smearing computation. Defaults to 21."
            },
            "time_width": {
                "type_and_info": r"int > 0, odd",
                "description": r"Width in time frames of the analysis window used in the local energy smearing computation. Defaults to 11."
            },
            "eta": {
                "type_and_info": r"float >= 0",
                "description": r"Factor used in the computation of combination weights. Defaults to 8."
            }
        }
    },
    "sls": {
        "name": "Smoothed local sparsity (LS)",
        "function": _sls_wrapper,
        "citations": [
            'M. d. V. M. da Costa and L. W. P. Biscainho, “Combining time-frequency representations via local sparsity criterion,” in 2nd AES Latin American Congress of Audio Engineering, Montevideo, Uruguay, Sep. 2018, pp. 78–85.',
            'M. d. V. M. da Costa, I. Apolinário, and L. W. P. Biscainho, “Sparse time-frequency representations for polyphonic audio based on combined efficient fan-chirp transforms,” Journal of the Audio Engineering Society, vol. 67, no. 11, pp. 894–905, Nov. 2019.'
        ],
        "parameters": {}
    }
}