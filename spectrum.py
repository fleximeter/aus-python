"""
File: spectrum.py
Author: Jeff Martin
Date: 2/11/23

This file contains functionality for spectral analysis.
"""

import scipy.fft
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from audiofile import AudioFile


def fft_data_decompose(fft_data):
    """
    Decomposes FFT data from a Numpy array into arrays of amplitudes and phases.
    This function can handle Numpy arrays of any dimension.
    :param fft_data: The data from a FFT function
    :return: Two arrays: one for amplitudes and one for phases
    """
    amps = np.abs(fft_data)
    phases = np.zeros(fft_data.shape)
    for i, x in np.ndenumerate(phases):
        phases[i] = np.angle(fft_data[i])
        if np.real(fft_data[i]) < 0:
            phases[i] += np.pi
        if phases[i] < 0:
            phases[i] += 2 * np.pi
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


def fft_range(file: AudioFile, channel: int = 0, frames=None, window_size: int = 1024):
    """
    Performs the FFT on a range of samples in an AudioFile.
    :param file: An AudioFile
    :param channel: The channel to analyze
    :param frames: A list or tuple specifying the outer frames of an area to analyze. If None, the entire file will be analyzed.
    :param window_size: The window size that will be analyzed
    :return: The spectrum of the file, as a 2D array
    """
    if frames is None:
        x = file.samples[channel, :]
    else:
        x = file.samples[channel, frames[0]:frames[1]]
    output = []
    for i in range(0, x.shape[0], window_size):
        num_samples_in_batch = min(x.shape[0] - i, window_size)
        batch = x[i:i+num_samples_in_batch]
        if num_samples_in_batch < window_size:
            batch = np.hstack((batch, np.zeros((window_size - num_samples_in_batch))))
        fft_data = scipy.fft.rfft(batch, n=window_size)
        fft_data = np.reshape(fft_data, (fft_data.shape[0], 1))
        output.append(fft_data)
    return np.hstack(output)
    

def fft_freqs(window_size: int = 1024, sample_rate: int = 44100) -> np.array:
    """
    Gets the FFT frequencies for plotting, etc.
    :param window_size: The window size used for FFT plotting
    :param sample_rate: The sample rate of the audio
    :return: An array with the frequencies
    """
    return scipy.fft.rfftfreq(window_size, 1 / sample_rate)


def plot_fft_data(fft_data, file, window_size):
    """
    Plots FFT data
    :param fft_data: FFT data to plot
    """
    fig, ax = plt.subplots(figsize = (10, 5))
    sns.heatmap(fft_data)
    plt.show()
