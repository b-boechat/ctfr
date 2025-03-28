from ctfr import __version__
from ctfr.exception import InvalidSampleError
from requests.exceptions import HTTPError
import pooch

_SAMPLES = {
    "synthetic": {
        "filename": "synthetic.wav",
        "description": "Synthetic audio of 1 s sampled at 22050 Hz, composed of two sinusoidal components with frequencies 440 Hz and 506 Hz, as well as a pulse component with a short duration around the 0.5 s mark."
    },
    "guitarset": {
        "filename": "guitarset.wav",
        "description": "Excerpt from the GuitarSet dataset, containing 4 s of guitar performance sampled at 44100 Hz."
    }
}

_GOODBOY_CURRENT_VERSION = pooch.create(
    path=pooch.os_cache("ctfr"),
    base_url=r"https://github.com/b-boechat/ctfr/raw/{version}/data/",
    version=__version__,
    version_dev="main",
    registry = {_SAMPLES[key]["filename"]: None for key in _SAMPLES}
)

_GOODBOY_LATEST = pooch.create(
    path=pooch.os_cache("ctfr"),
    base_url=r"https://github.com/b-boechat/ctfr/raw/refs/heads/main/data/",
    version_dev="main",
    registry = {_SAMPLES[key]["filename"]: None for key in _SAMPLES}
)

def list_samples():
    """List the available sample files included in this package, along with their brief descriptions.

    See Also
    --------
    ctfr.fetch_sample
    """
    print("Available samples:")
    print("-----------------------------------------------------------------------------")
    for key in _SAMPLES:
        print(f"{key:20}\t{_SAMPLES[key]['description']}")


def fetch_sample(sample_key):
    """Fetch the filename for a data sample included in this package.

    Parameters
    ----------
    sample_key : str
        The key of the sample dataset to fetch. The available keys can be listed using :func:`list_samples`.

    Returns
    -------
    str
        The path to the fetched sample dataset.

    Raises
    ------
    ctfr.exception.InvalidSampleError
        If the sample key does not match any sample file included in this package.

    See Also
    --------
    ctfr.list_samples
    """
    try:
        return _GOODBOY_CURRENT_VERSION.fetch(_SAMPLES[sample_key]["filename"])
    except KeyError:
        raise InvalidSampleError(f"Invalid sample key: {sample_key}. Use ctfr.list_samples() to list available keys.")
    except HTTPError:
        print("Sample not found in the current version. Fetching it from the latest main branch.")
        return _GOODBOY_LATEST.fetch(_SAMPLES[sample_key]["filename"])