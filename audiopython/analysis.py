"""
File: analysis.py
Author: Jeff Martin
Date: 12/17/23

Audio analysis tools developed from Eyben, "Real-Time Speech and Music Classification"
"""

import numpy as np


def energy(audio):
    """
    Extracts the RMS energy of the signal
    :param audio: A NumPy array of audio samples
    :return: The RMS energy of the signal
    Reference: Eyben, pp. 21-22
    """
    return np.sqrt((1 / audio.shape[-1]) * np.sum(np.square(audio)))


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


