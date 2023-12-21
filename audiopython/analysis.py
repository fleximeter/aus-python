"""
File: analysis.py
Author: Jeff Martin
Date: 12/17/23

Audio analysis tools developed from Eyben, "Real-Time Speech and Music Classification"
"""

import audiopython.spectrum
import crepe
import numpy as np
import scipy.fft
import scipy.signal
import sklearn.linear_model


def analyzer(audio, sample_rate):
    """
    Runs a suite of analysis tools on a provided NumPy array of audio samples
    :param audio: A 1D NumPy array of audio samples
    :param sample_rate: The sample rate of the audio
    :return: A dictionary with the analysis results
    """
    results = {}
    audio_spectrum = scipy.fft.rfft(audio)
    magnitude_spectrum, phase_spectrum = audiopython.spectrum.fft_data_decompose(audio_spectrum)
    rfftfreqs = scipy.fft.rfftfreq(audio.shape[-1], 1/44100)
    results['energy'] = energy(audio)
    results['spectral_centroid'] = spectral_centroid(magnitude_spectrum, rfftfreqs)
    results['spectral_flatness'] = spectral_flatness(magnitude_spectrum)
    results['spectral_slope'] = spectral_slope(magnitude_spectrum, rfftfreqs)
    results['spectral_roll_off_0.5'] = spectral_roll_off_point(magnitude_spectrum, rfftfreqs, 0.5)
    results['spectral_roll_off_0.75'] = spectral_roll_off_point(magnitude_spectrum, rfftfreqs, 0.75)
    results['spectral_roll_off_0.9'] = spectral_roll_off_point(magnitude_spectrum, rfftfreqs, 0.9)
    results['spectral_roll_off_0.95'] = spectral_roll_off_point(magnitude_spectrum, rfftfreqs, 0.95)
    results['zero_crossing_rate'] = zero_crossing_rate(audio, sample_rate)
    results.update(spectral_moments(magnitude_spectrum, rfftfreqs, results["spectral_centroid"]))
    return results


def energy(audio):
    """
    Extracts the RMS energy of the signal
    :param audio: A NumPy array of audio samples
    :return: The RMS energy of the signal
    Reference: Eyben, pp. 21-22
    """
    return np.sqrt((1 / audio.shape[-1]) * np.sum(np.square(audio)))


def spectral_centroid(magnitude_spectrum, magnitude_freqs):
    """
    Calculates the spectral centroid from provided magnitude spectrum
    :param magnitude_spectrum: The magnitude spectrum
    :param magnitude_freqs: The magnitude frequencies
    :return: The spectral centroid
    Reference: Eyben, pp. 39-40
    """
    return np.sum(np.multiply(magnitude_spectrum, magnitude_freqs)) / np.sum(magnitude_spectrum)


def spectral_entropy(magnitude_spectrum):
    """
    Calculates the spectral entropy from provided magnitude spectrum
    :param magnitude_spectrum: The magnitude spectrum
    :return: The spectral entropy
    Reference: Eyben, pp. 23, 40, 41
    """
    power_spectrum = np.square(magnitude_spectrum)
    spectrum_pmf = power_spectrum / np.sum(power_spectrum)
    entropy = 0
    for i in range(spectrum_pmf.size):
        entropy += spectrum_pmf[i] * np.log2(spectrum_pmf[i])
    return -entropy


def spectral_flatness(magnitude_spectrum):
    """
    Calculates the spectral flatness from provided magnitude spectrum
    :param magnitude_spectrum: The magnitude spectrum
    :return: The spectral flatness, in dBFS
    Reference: Eyben, p. 39, https://en.wikipedia.org/wiki/Spectral_flatness
    """
    flatness = np.exp(np.sum(np.log(magnitude_spectrum)) / magnitude_spectrum.size) / (np.sum(magnitude_spectrum) / magnitude_spectrum.size)
    return 20 * np.log10(flatness)


def spectral_moments(magnitude_spectrum, magnitude_freqs, centroid):
    """
    Calculates the spectral moments from provided magnitude spectrum
    :param magnitude_spectrum: The magnitude spectrum
    :param magnitude_freqs: The magnitude frequencies
    :param centroid: The spectral centroid
    :return: The spectral moments
    Reference: Eyben, pp. 23, 39-40
    """
    power_spectrum = np.square(magnitude_spectrum)
    spectrum_pmf = power_spectrum / np.sum(power_spectrum)
    spectral_variance = 0
    spectral_skewness = 0
    spectral_kurtosis = 0
    for i in range(magnitude_freqs.shape[-1]):
        spectral_variance += ((magnitude_freqs[i] - centroid) ** 2) * spectrum_pmf[i]
    for i in range(magnitude_freqs.shape[-1]):
        spectral_skewness += ((magnitude_freqs[i] - centroid) ** 3) * spectrum_pmf[i]
    for i in range(magnitude_freqs.shape[-1]):
        spectral_kurtosis += ((magnitude_freqs[i] - centroid) ** 4) * spectrum_pmf[i]
    spectral_skewness /= np.power(spectral_variance, 3/2)
    spectral_kurtosis /= np.power(spectral_variance, 2)
    return {"spectral_variance": spectral_variance, "spectral_skewness": spectral_skewness, "spectral_kurtosis": spectral_kurtosis}


def spectral_roll_off_point(magnitude_spectrum, magnitude_freqs, n):
    """
    Calculates the spectral slope from provided magnitude spectrum
    :param magnitude_spectrum: The magnitude spectrum
    :param magnitude_freqs: The magnitude frequencies
    :param n: The roll-off, as a fraction (0 <= n <= 1.00)
    :return: The roll-off frequency
    Reference: Eyben, p. 41
    """
    power_spectrum = np.square(magnitude_spectrum)
    energy = np.sum(power_spectrum)
    i = -1
    cumulative_energy = 0
    while cumulative_energy < n and i < magnitude_freqs.size - 1:
        i += 1
        cumulative_energy += power_spectrum[i] / energy
    return magnitude_freqs[i]


def spectral_slope(magnitude_spectrum, magnitude_freqs):
    """
    Calculates the spectral slope from provided magnitude spectrum
    :param magnitude_spectrum: The magnitude spectrum
    :param magnitude_freqs: The magnitude frequencies
    :return: The slope and y-intercept
    Reference: Eyben, pp. 35-38
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
