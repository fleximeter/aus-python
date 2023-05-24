"""
File: spectrum.py
Author: Jeff Martin
Date: 2/11/23

This file contains functionality for spectral analysis.
"""

import scipy.fft
import numpy as np
from wav import AudioFile

def fft(file: AudioFile, channel: int = 0, frames=None, window_size: int = 1024):
    """
    Performs the FFT on an AudioFile.
    :param file: An AudioFile
    :param channel: The channel to analyze
    :param frames: A list or tuple specifying the outer frames of an area to analyze. If None, the entire file will be analyzed.
    :param window_size: The window size that will be analyzed
    :return: The spectrum of the file
    """
    if frames is None:
        x = file.samples[channel, :]
    else:
        x = file.samples[channel, frames[0]:frames[1]]
    output = None
    for i in range(0, file.num_frames, window_size):
        num_samples_in_batch = np.min(file.num_frames - i - 1, window_size)
        fft_data = scipy.fft.rfft(x[i:i+num_samples_in_batch], n=num_samples_in_batch)
        fft_data = np.transpose(fft_data)
        if output is None:
            output = fft_data
        else:
            output = np.hstack(output, fft_data)
    return output

def plot_fft_data(fft_data):
    """
    Plots FFT data
    :param fft_data: FFT data to plot
    """
    pass
