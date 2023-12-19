"""
File: analysis.py
Author: Jeff Martin
Date: 12/17/23

Audio analysis tools developed from Eyben, "Real-Time Speech and Music Classification"
"""

import numpy as np
import scipy.fft
import scipy.signal
import sklearn.linear_model
import spectrum


def analyzer(audio):
    """
    Runs a suite of analysis tools on a provided NumPy array of audio samples
    :param audio: A 1D NumPy array of audio samples
    :return: A dictionary with the analysis results
    """
    results = {}
    audio_spectrum = scipy.fft.rfft(audio)
    magnitude_spectrum, phase_spectrum = spectrum.fft_data_decompose(audio_spectrum)
    rfftfreqs = scipy.fft.rfftfreq(audio.shape[-1], 1/44100)
    results['energy'] = energy(audio)
    results['spectral_slope'] = spectral_slope(magnitude_spectrum, rfftfreqs)
    results['zero_crossing_rate'] = zero_crossing_rate(audio)
    return results


def energy(audio):
    """
    Extracts the RMS energy of the signal
    :param audio: A NumPy array of audio samples
    :return: The RMS energy of the signal
    Reference: Eyben, pp. 21-22
    """
    return np.sqrt((1 / audio.shape[-1]) * np.sum(np.square(audio)))


def spectral_slope(magnitude_spectrum, magnitude_freqs):
    """
    Calculates the spectral slope from provided magnitude spectrum
    :param magnitude_spectrum: The magnitude spectrum
    :param magnitude_freqs: The magnitude frequencies
    :return: The slope and y-intercept
    """
    slope = sklearn.linear_model.LinearRegression().fit(np.reshape(magnitude_spectrum, (magnitude_spectrum.shape[-1], 1)), magnitude_freqs)
    return slope.coef_[-1], slope.intercept_


def zero_crossing_rate(audio, sample_rate):
    """
    Extracts the zero-crossing rate
    :param audio: A NumPy array of audio samples
    :param sample_rate: The sample rate of the audio
    :return: The zero-crossing rate
    Reference: Eyben, p. 20
    """
    num_zc = 0
    N = audio.shape[-1]
    for n in range(1, N):
        if audio[n-1] * audio[n] < 0:
            num_zc += 1
        elif n < N-1 and audio[n-1] * audio[n+1] < 0 and audio[n] == 0:
            num_zc += 1
    return num_zc * sample_rate / N


