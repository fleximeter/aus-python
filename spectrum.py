"""
File: spectrum.py
Author: Jeff Martin
Date: 2/11/23

This file contains functionality for spectral analysis.
"""

import scipy.fft
from wav import AudioFile

def fft(file: AudioFile, channel: int = 0, frames=None):
    """
    Performs the FFT on an AudioFile.
    :param file: An AudioFile
    :param channel: The channel to analyze
    :param frames: A list or tuple specifying the outer frames of an area to analyze. If None, the entire file will be analyzed.
    :return: The spectrum of the file
    """
    if frames is None:
        return scipy.fft.rfft(file.samples[channel, :])
    else:
        return scipy.fft.rfft(file.samples[channel, frames[0]:frames[1]])
