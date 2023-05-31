"""
File: spectrum.py
Author: Jeff Martin
Date: 2/11/23

This file contains functionality for spectral analysis.
"""

import scipy.fft
import numpy as np
import matplotlib.pyplot as plt
from audiofile import AudioFile


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
        fft_data = scipy.fft.rfft(x[i:i+num_samples_in_batch], n=num_samples_in_batch)
        fft_data = np.abs(fft_data)
        fft_data = np.reshape(fft_data, (fft_data.shape[0], 1))
        # print(fft_data.shape)
        output.append(fft_data)
    return np.hstack(output)


def fft_freqs(file: AudioFile, window_size: int = 1024) -> np.array:
    """
    Gets the FFT frequencies for plotting, etc.
    :param file: An AudioFile
    :param window_size: The window size used for FFT plotting
    :return: An array with the frequencies
    """
    return scipy.fft.rfftfreq(window_size, 1 / file.sample_rate)


def plot_fft_data(fft_data, file, window_size):
    """
    Plots FFT data
    :param fft_data: FFT data to plot
    """
    fig, ax = plt.subplots()
    ax.imshow(fft_data)
    plt.show()
