from ctfr.implementations.swgm_cy import _swgm_wrapper
from ctfr.implementations.fls_cy import _fls_wrapper
from ctfr.implementations.lt_cy import _lt_wrapper
from ctfr.implementations.ls_cy import _ls_wrapper
from ctfr.implementations.binwise_np import _mean_wrapper, _median_wrapper, _min_wrapper

_methods_dict = {
    "mean": {
        "name": "Binwise Mean",
        "function": _mean_wrapper,
        "citation": None
    },
    "median": {
        "name": "Binwise Median",
        "function": _median_wrapper,
        "citation": None
    },
    "min": {
        "name": "Binwise Minimum",
        "function": _min_wrapper,
        "citation": None
    },
    "swgm": {
        "name": "Sample Weighted Geometric Mean (SWGM)",
        "function": _swgm_wrapper,
        "citation": "M. V. M. da Costa and L. W. P. Biscainho, \"Combining time-frequency representations for music information retrieval\", in 15o Congresso de Engenharia de Áudio da AES-Brasil, 10 2017, pp. 12–18.",
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
        "name": "Fast Local Sparsity (FLS)",
        "function": _fls_wrapper,
        "citation": "M. V. M. da Costa and L. W. P. Biscainho, \"The fast local sparsity method: a low-cost combination of time-frequency representations based on the Hoyer sparsity\", Journal of the Audio Engineering Society, vol. 70, no. 9, pp. 698–707, 09 2022.",
        "doi": "https://doi.org/10.17743/jaes.2022.0036",
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
        "citation": "A. Lukin and J. Todd, \"Adaptive Time-Frequency Resolution for Analysis and Processing of Audio\", in Proceedings of the 27th AES International Conference, 05 2006.",
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
    "ls": {
        "name": "Local Sparsity (LS)",
        "function": _ls_wrapper,
        "citation": "M. V. M. da Costa, I. F. Apolinário, and L. W. P. Biscainho, \"Sparse time-frequency representations for polyphonic audio based on combined efficient fan-chirp transforms\", Journal of the Audio Engineering Society, vol. 67, no. 11, pp. 894–905, 11 2019.",
        "doi": "http://doi.org/10.17743/jaes.2019.0039"
    }
}