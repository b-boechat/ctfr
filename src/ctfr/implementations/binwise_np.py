import numpy as np

def _mean_wrapper(X):
    return np.mean(X, axis=0)

def _median_wrapper(X):
    return np.median(X, axis=0)

def _min_wrapper(X):
    return np.min(X, axis=0)