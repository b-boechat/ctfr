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
        "citation": "M. V. M. da Costa and L. W. P. Biscainho, \"Combining time-frequency representations for music information retrieval\", in 15o Congresso de Engenharia de Áudio da AES-Brasil, 10 2017, pp. 12–18."
    },
    "fls": {
        "name": "Fast Local Sparsity (FLS)",
        "function": _fls_wrapper,
        "citation": "M. V. M. da Costa and L. W. P. Biscainho, \"The fast local sparsity method: a low-cost combination of time-frequency representations based on the Hoyer sparsity\", Journal of the Audio Engineering Society, vol. 70, no. 9, pp. 698–707, 09 2022.",
        "doi": "https://doi.org/10.17743/jaes.2022.0036"
    },
    "lt": {
        "name": "Lukin-Todd (LT)",
        "function": _lt_wrapper,
        "citation": "A. Lukin and J. Todd, \"Adaptive Time-Frequency Resolution for Analysis and Processing of Audio\", in Proceedings of the 27th AES International Conference, 05 2006.",
    },
    "ls": {
        "name": "Local Sparsity (LS)",
        "function": _ls_wrapper,
        "citation": "M. V. M. da Costa, I. F. Apolinário, and L. W. P. Biscainho, \"Sparse time-frequency representations for polyphonic audio based on combined efficient fan-chirp transforms\", Journal of the Audio Engineering Society, vol. 67, no. 11, pp. 894–905, 11 2019.",
        "doi": "http://doi.org/10.17743/jaes.2019.0039"
    }
}