"""
File: analysis.py
Author: Jeff Martin
Date: 12/17/23

Audio analysis tools developed from Eyben, "Real-Time Speech and Music Classification"
"""

import operations
from . import spectrum
import librosa
import numpy as np
import scipy.fft
import scipy.signal
import sklearn.linear_model


def analyzer(audio, sample_rate, frequency_quantile=0.5):
    """
    Runs a suite of analysis tools on a provided NumPy array of audio samples
    :param audio: A 1D NumPy array of audio samples
    :param sample_rate: The sample rate of the audio
    :param frequency_quantile: The quantile to select the frequency from, since the frequencies 
    are calculated as an array of frequencies. Normally the median (0.5) is a good choice.
    :return: A dictionary with the analysis results
    """
    results = {}
    audio_spectrum = scipy.fft.rfft(audio)
    magnitude_spectrum, phase_spectrum = spectrum.fft_data_decompose(audio_spectrum)
    power_spectrum = np.square(magnitude_spectrum)
    rfftfreqs = scipy.fft.rfftfreq(audio.shape[-1], 1/sample_rate)
    results["dbfs"] = operations.dbfs_audio(audio)
    results['energy'] = energy(audio)
    results['pitch'] = librosa_pitch_estimation(audio, sample_rate, 27.5, 3520, frequency_quantile)
    results['midi'] = midi_estimation_from_pitch(results['pitch'])
    results['spectral_centroid'] = spectral_centroid(magnitude_spectrum, rfftfreqs)
    results['spectral_entropy'] = spectral_entropy(power_spectrum)
    results['spectral_flatness'] = spectral_flatness(magnitude_spectrum)
    results['spectral_slope'] = spectral_slope(magnitude_spectrum, rfftfreqs)
    results['spectral_roll_off_0.5'] = spectral_roll_off_point(power_spectrum, rfftfreqs, 0.5)
    results['spectral_roll_off_0.75'] = spectral_roll_off_point(power_spectrum, rfftfreqs, 0.75)
    results['spectral_roll_off_0.9'] = spectral_roll_off_point(power_spectrum, rfftfreqs, 0.9)
    results['spectral_roll_off_0.95'] = spectral_roll_off_point(power_spectrum, rfftfreqs, 0.95)
    results['zero_crossing_rate'] = zero_crossing_rate(audio, sample_rate)
    results.update(spectral_moments(power_spectrum, rfftfreqs, results["spectral_centroid"]))
    return results


def energy(audio):
    """
    Extracts the RMS energy of the signal
    :param audio: A NumPy array of audio samples
    :return: The RMS energy of the signal
    Reference: Eyben, pp. 21-22
    """
    energy = np.sqrt((1 / audio.shape[-1]) * np.sum(np.square(audio)))
    if np.isnan(energy) or np.isneginf(energy) or np.isinf(energy):
        energy = 0.0
    return energy
    

def midi_estimation_from_pitch(frequency):
    """
    Estimates MIDI note number from provided frequency
    :param frequency: The frequency
    :return: The midi note number (or NaN)
    """
    midi_est = 12 * np.log2(frequency / 440) + 69
    if np.isnan(midi_est) or np.isneginf(midi_est) or np.isinf(midi_est):
        midi_est = 0.0
    return midi_est
    

def librosa_pitch_estimation(audio, sample_rate=44100, min_freq=55, max_freq=880, quantile=0.5):
    """
    Estimates the pitch of the signal, based on the LibRosa pyin function
    :param audio: A NumPy array of audio samples
    :param sample_rate: The sample rate of the audio
    :param min_freq: The minimum frequency allowed for the pyin function
    :param max_freq: The maximum frequency allowed for the pyin function
    :param quantile: The quantile to select the frequency from, since the frequencies 
    are calculated as an array of frequencies. Normally the median (0.5) is a good choice.
    :return: The pitch
    """
    estimates = librosa.pyin(audio, fmin=min_freq, fmax=max_freq, sr=sample_rate)
    nans = set()
    for i in range(estimates[0].shape[-1]):
        if np.isnan(estimates[0][i]) or np.isinf(estimates[0][i]) or np.isneginf(estimates[0][i]):
            nans.add(i)
    # We arbitrarily decide that if half of the detected pitches are NaN, we will
    # be returning NaN
    if estimates[0].shape[-1] // 2 > len(nans):
        for i in nans:
            estimates[0][i] = 0
    return np.quantile(estimates[0], quantile)


def spectral_centroid(magnitude_spectrum, magnitude_freqs):
    """
    Calculates the spectral centroid from provided magnitude spectrum
    :param magnitude_spectrum: The magnitude spectrum
    :param magnitude_freqs: The magnitude frequencies
    :return: The spectral centroid
    Reference: Eyben, pp. 39-40
    """
    centroid = np.sum(np.multiply(magnitude_spectrum, magnitude_freqs)) / np.sum(magnitude_spectrum)
    if np.isnan(centroid) or np.isneginf(centroid) or np.isinf(centroid):
        centroid = 0.0
    return centroid


def spectral_entropy(power_spectrum):
    """
    Calculates the spectral entropy from provided power spectrum
    :param power_spectrum: The power spectrum
    :return: The spectral entropy
    Reference: Eyben, pp. 23, 40, 41
    """
    spectrum_pmf = power_spectrum / np.sum(power_spectrum)
    entropy = 0
    spec_mul = spectrum_pmf * np.log2(spectrum_pmf)
    entropy = -np.sum(spec_mul)
    if np.isnan(entropy) or np.isneginf(entropy) or np.isinf(entropy):
        entropy = 0.0
    return entropy


def spectral_flatness(magnitude_spectrum):
    """
    Calculates the spectral flatness from provided magnitude spectrum
    :param magnitude_spectrum: The magnitude spectrum
    :return: The spectral flatness, in dBFS
    Reference: Eyben, p. 39, https://en.wikipedia.org/wiki/Spectral_flatness
    """
    flatness = np.exp(np.sum(np.log(magnitude_spectrum)) / magnitude_spectrum.size) / (np.sum(magnitude_spectrum) / magnitude_spectrum.size)
    flatness = 20 * np.log10(flatness)
    if np.isnan(flatness) or np.isneginf(flatness) or np.isinf(flatness):
        flatness = 0.0
    return flatness


def spectral_moments(power_spectrum, magnitude_freqs, centroid):
    """
    Calculates the spectral moments from provided power spectrum
    :param power_spectrum: The power spectrum
    :param magnitude_freqs: The magnitude frequencies
    :param centroid: The spectral centroid
    :return: The spectral moments
    Reference: Eyben, pp. 23, 39-40
    """
    spectrum_pmf = power_spectrum / np.sum(power_spectrum)
    spectral_variance_arr = np.square(magnitude_freqs - centroid) * spectrum_pmf
    spectral_skewness_arr = np.power(magnitude_freqs - centroid, 3) * spectrum_pmf
    spectral_kurtosis_arr = np.power(magnitude_freqs - centroid, 4) * spectrum_pmf
    spectral_variance = np.sum(spectral_variance_arr)
    spectral_skewness = np.sum(spectral_skewness_arr)
    spectral_kurtosis = np.sum(spectral_kurtosis_arr)
    spectral_skewness /= np.float_power(spectral_variance, 3/2)
    spectral_kurtosis /= np.power(spectral_variance, 2)
    if np.isnan(spectral_variance) or np.isneginf(spectral_variance) or np.isinf(spectral_variance):
        spectral_variance = 0.0
    if np.isnan(spectral_skewness) or np.isneginf(spectral_skewness) or np.isinf(spectral_skewness):
        spectral_skewness = 0.0
    if np.isnan(spectral_kurtosis) or np.isneginf(spectral_kurtosis) or np.isinf(spectral_kurtosis):
        spectral_kurtosis = 0.0
    return {"spectral_variance": spectral_variance, "spectral_skewness": spectral_skewness, "spectral_kurtosis": spectral_kurtosis}


def spectral_roll_off_point(power_spectrum, magnitude_freqs, n):
    """
    Calculates the spectral slope from provided power spectrum
    :param power_spectrum: The power spectrum
    :param magnitude_freqs: The magnitude frequencies
    :param n: The roll-off, as a fraction (0 <= n <= 1.00)
    :return: The roll-off frequency
    Reference: Eyben, p. 41
    """
    energy = np.sum(power_spectrum)
    i = -1
    cumulative_energy = 0
    while cumulative_energy < n and i < magnitude_freqs.size - 1:
        i += 1
        cumulative_energy += power_spectrum[i] / energy
    roll_off = magnitude_freqs[i]
    if np.isnan(roll_off) or np.isneginf(roll_off) or np.isinf(roll_off):
        roll_off = 0.0
    return roll_off


def spectral_slope(magnitude_spectrum, magnitude_freqs):
    """
    Calculates the spectral slope from provided magnitude spectrum
    :param magnitude_spectrum: The magnitude spectrum
    :param magnitude_freqs: The magnitude frequencies
    :return: The slope and y-intercept
    Reference: Eyben, pp. 35-38
    """
    slope = sklearn.linear_model.LinearRegression().fit(np.reshape(magnitude_spectrum, (magnitude_spectrum.shape[-1], 1)), magnitude_freqs)
    m = slope.coef_[-1]
    b = slope.intercept_
    if np.isnan(m) or np.isneginf(m) or np.isinf(m):
        m = 0.0
    if np.isnan(b) or np.isneginf(b) or np.isinf(b):
        b = 0.0
    return m, b


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
    zcr = num_zc * sample_rate / N
    if np.isnan(zcr) or np.isneginf(zcr) or np.isinf(zcr):
        zcr = 0.0
    return zcr
