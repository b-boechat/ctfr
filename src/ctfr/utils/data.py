from ctfr import __version__
import pooch

_SAMPLES = {
    "synthetic": {
        "filename": "synthetic.wav",
        "description": "Synthetic audio of 1 s sampled at 22050 Hz, composed of two sinusoidal components with frequencies 440 Hz and 506 Hz, as well as a pulse component with a short duration around the 0.5 s mark."
    },
    "guitarset_sample": {
        "filename": "guitarset_sample.wav",
        "description": "Excerpt from the GuitarSet dataset, containing 4 s of guitar performance sampled at 44100 Hz."
    }
}

_GOODBOY = pooch.create(
    path=pooch.os_cache("ctfr"),
    #base_url=r"https://github.com/b-boechat/ctfr/raw/{version}/data/",
    base_url=r"https://github.com/b-boechat/ctfr/raw/refs/heads/pooch/data/", # Placeholder for testing.
    version=__version__,
    version_dev="main",
    registry = {_SAMPLES[key]["filename"]: None for key in _SAMPLES}
)

def list_samples():
    """List the available sample files included in this package, along with their brief descriptions.

    See Also
    --------
    fetch_sample
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

    See Also
    --------
    list_samples
    """
    return _GOODBOY.fetch(_SAMPLES[sample_key]["filename"])