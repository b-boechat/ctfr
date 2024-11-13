"""
Basic usage
===========

This example demonstrates the basic usage of combined TFRs and how to
compute and plot them using the ctfr package.

"""

import ctfr
import numpy as np
import matplotlib.pyplot as plt


######################################################################
# --------------
# 


######################################################################
# Loading the audio data
# ~~~~~~~~~~~~~~~~~~~~~~
# 


######################################################################
# Our synthetic example consists of :math:`1` s of audio data sampled at
# :math:`22050 Hz`. The signal is comprised of two superposed sinusoidal
# components with frequencies :math:`f_1 = 440` Hz and :math:`f_2 = 506`
# Hz, as well as a pulse component with a short duration around
# :math:`t = 0.5` s. We will see how the ctfr package can help us compute
# a combined TFR of STFTs with good resolution in both time and frequency
# domains, which is not possible with a traditional STFT. Let’s load the
# audio data and plot it.
# 

# Load and print the audio signal.
signal, sr = ctfr.load("audio/synthetic.wav")
print(f"Sample rate: {sr} Hz")
plt.plot(signal);


######################################################################
# --------------
# 


######################################################################
# Computing STFT spectrograms with different resolutions.
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 


######################################################################
# Now, let’s compute plot an STFT spectrogram of the audio signal. We will
# use a window length of :math:`L = 512` samples (~ :math:`23` ms), a hop
# length of :math:`512` samples, and a FFT size of :math:`2048` samples.
# 

# Compute the spectrogram with L = 512.
spec_512 = ctfr.stft_spec(signal, win_length=512, n_fft=2048, hop_length=256)

# Plot the spectrogram.
img = ctfr.specshow(ctfr.power_to_db(spec_512, ref=np.max), sr=sr, hop_length=256, x_axis='time', y_axis='linear', cmap='inferno')
plt.ylim(0, 1000)
plt.colorbar(img, format="%+2.0f dB");


######################################################################
# We can see that the the pulse component’s onset and offset are well
# delineated, but the sinusoidal components are not well resolved in the
# frequency domain. This is due to the short window length, which provides
# good time resolution but poor frequency resolution.
# 
# Now, let’s increase the window length to :math:`L = 1024` samples (~
# :math:`46` ms) and plot the STFT spectrogram again.
# 

# Compute the spectrogram with L = 1024.
spec_1024 = ctfr.stft_spec(signal, win_length=1024, n_fft=2048, hop_length=256)

# Plot the spectrogram.
img = ctfr.specshow(ctfr.power_to_db(spec_1024, ref=np.max), sr=sr, hop_length=256, x_axis='time', y_axis='linear', cmap='inferno')
plt.ylim(0, 1000)
plt.colorbar(img, format="%+2.0f dB");


######################################################################
# Wee see that our frequency resolution is improved at cost of poorer time
# resolution.
# 
# Let’s go even further and increase our window length to :math:`L = 2048`
# samples (~ :math:`93` ms), compute the corresponding STFT and plot the
# resulting spectrogram.
# 

# Compute the spectrogram with L = 1024.
spec_2048 = ctfr.stft_spec(signal, win_length=2048, n_fft=2048, hop_length=256)

# Plot the spectrogram.
img = ctfr.specshow(ctfr.power_to_db(spec_2048, ref=np.max), sr=sr, hop_length=256, x_axis='time', y_axis='linear', cmap='inferno')
plt.ylim(0, 1000)
plt.colorbar(img, format="%+2.0f dB");


######################################################################
# With this larger window length, our sinusoidal components are now well
# resolved in the frequency domain, but the pulse component’s onset and
# offset are not well delineated.
# 


######################################################################
# --------------
# 


######################################################################
# Computing a combined TFR
# ~~~~~~~~~~~~~~~~~~~~~~~~
# 


######################################################################
# In summary, what we have seen is the time-frequency trade-off. Achieving
# better frequency resolution (by increasing the window length) comes at
# the cost of poorer time resolution, and vice versa. However, we can
# circumvent this problem by computing a combined TFR, which is an average
# (in a generalized sense, depending on the combination method) of
# multiple STFTs computed with different window lengths. This allows us to
# achieve good resolution in both time and frequency domains.
# 
# Let’s see how we can do this using this package.
# 


######################################################################
# Using ctfr.ctfr_from_specs
# ^^^^^^^^^^^^^^^^^^^^^^^^^^
# 


######################################################################
# Since we have already computed STFTs with different window lengths, we
# can use the ``ctfr_from_specs`` function to compute a combined TFR from
# these STFT spectrograms. This function requires an iterable of STFT
# spectrograms with the same time-frequency alignment. Since we used the
# same hop length and FFT size for all STFTs, they are already aligned.
# 

print(spec_512.shape)
print(spec_1024.shape)
print(spec_2048.shape)


######################################################################
# We also have to provide a combination method. Let’s list all available
# methods:
# 

ctfr.show_methods()


######################################################################
# For this example, we’ll use the Sample-Weighted Geometric Mean (SWGM),
# which is a lightweight and effective binwise combination method. Let’s
# compute the combined TFR and plot it.
# 

# Compute the combined spectrogram using ctfr.ctfr_from_specs and the SWGM method,
swgm_spec = ctfr.ctfr_from_specs((spec_512, spec_1024, spec_2048), method='swgm')

# Plot the combined spectrogram.
img = ctfr.specshow(ctfr.power_to_db(swgm_spec, ref=np.max), sr=sr, hop_length=256, x_axis='time', y_axis='linear', cmap='inferno')
plt.ylim(0, 1000)
plt.colorbar(img, format="%+2.0f dB");


######################################################################
# .. note::
#    You can also use ``ctfr.methods.swgm_from_specs(X, ...)``,
#    which is an alias for
#    ``ctfr.ctfr_from_specs(X, method='swgm', ...)``.
# 


######################################################################
# As we can see, we have achieved good resolution in both time and
# frequency domains, with the sinusoidal components and the pulse
# component well resolved.
# 


######################################################################
# --------------
# 


######################################################################
# Using ctfr.ctfr
# ^^^^^^^^^^^^^^^
# 


######################################################################
# Using ``ctfr_from_specs`` is useful when we already have the STFT
# spectrograms to combine, or when we want more control over how to
# generate them. When we just want to compute a combined TFR directly from
# an audio signal, we can use the ``ctfr`` function, which computes the
# STFT spectrograms with different window lengths and then combines them.
# 
# Let’s do this for our signal, using the same parameters as before.
# 

# Compute the combined spectrogram using ctfr.ctfr and the SWGM method,
swgm_spec_2 = ctfr.ctfr(signal, sr = sr, method = "swgm", win_length_list=[512, 1024, 2048], hop_length=256, n_fft=2048)

# Plot the combined spectrogram.
img = ctfr.specshow(ctfr.power_to_db(swgm_spec_2, ref=np.max), sr=sr, hop_length=512, x_axis='time', y_axis='linear', cmap='inferno')
plt.ylim(0, 1000)
plt.colorbar(img, format="%+2.0f dB");


######################################################################
# .. note::
#    You can also use ``ctfr.methods.swgm(X, sr, ...)``, which
#    is an alias for ``ctfr.ctfr(X, sr, method='swgm', ...)``.
# 


######################################################################
# We can see that the combined spectrogram looks the same as the one we
# computed in the previous section. Let’s confirm that they’re indeed the
# same:
# 

np.array_equal(swgm_spec, swgm_spec_2)