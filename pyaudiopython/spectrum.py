"""
File: spectrum.py
Author: Jeff Martin
Date: 2/11/23

This file contains functionality for spectral analysis.
"""

import scipy.fft
import numpy as np
import matplotlib.pyplot as plt
from . import audiofile


def fft_data_decompose(fft_data):
    """
    Decomposes FFT data from a Numpy array into arrays of amplitudes and phases.
    This function can handle Numpy arrays of any dimension.
    :param fft_data: The data from a FFT function
    :return: Two arrays: one for amplitudes and one for phases
    """
    amps = np.abs(fft_data)
    phases = np.angle(fft_data)
    return amps, phases


def fft_data_recompose(amps, phases):
    """
    Recomposes FFT data from arrays of amplitudes and phases
    This function can handle Numpy arrays of any dimension.
    :param amps: An array of amplitudes
    :param phases: An array of phases
    :return: An array of FFT data
    """
    real = np.cos(phases) * amps
    imag = np.sin(phases) * amps
    return real + (imag * 1j)


def plot_spectrogram(file: audiofile.AudioFile, channel: int = 0, frames=None, window_size: int = 1024):
    """
    Plots FFT data
    :param file: An AudioFile
    :param channel: The channel to analyze
    :param frames: A list or tuple specifying the outer frames of an area to analyze. If None, the entire file will be analyzed.
    :param window_size: The window size that will be analyzed
    """
    if frames is None:
        x = file.samples[channel, :]
    else:
        x = file.samples[channel, frames[0]:frames[1]]
    
    fig, ax = plt.subplots(figsize = (10, 5))
    ax.specgram(x, NFFT=window_size, Fs=file.sample_rate, noverlap=128)
    ax.set_title(f"Spectrum of \"{file.file_name}\"")
    ax.set_xlabel("Time (seconds)")
    ax.set_ylabel("Frequency (Hz)")
    plt.show()


def plot_spectrum(spectrum, sample_rate, frequency_range=None):
    """
    Plots FFT data. The FFT data should be in original imaginary form.
    It will be converted to a normalized power spectrum in decibels.
    :param spectrum: An imaginary spectrum to plot
    :param sample_rate: The sample rate (for determining frequencies)
    :param frequency_range: If not None, only the frequencies within this range will be plotted.
    """
    fig, ax = plt.subplots(figsize = (10, 5))
    mags, phases = fft_data_decompose(spectrum)
    power = np.square(mags)
    power = 20 * np.log10(np.abs(power)/np.max(np.abs(power)))

    freqs = scipy.fft.rfftfreq((spectrum.shape[-1] - 1) * 2, 1/sample_rate)
    if frequency_range is not None:
        new_freqs = []
        new_power_spectrum = []
        for i in range(freqs.shape[-1]):
            if frequency_range[0] <= freqs[i] <= frequency_range[1]:
                new_freqs.append(freqs[i])
                new_power_spectrum.append(power[i])
        ax.plot(new_freqs, new_power_spectrum)
    else:
        ax.plot(freqs, power)
    ax.set_title(f"Spectrum")
    ax.set_xlabel("Frequency (Hz)")
    ax.set_ylabel("Amplitude (dB)")
    plt.show()
