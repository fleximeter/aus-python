"""
File: granulator.py
Author: Jeff Martin
Date: 7/16/23

This file is for experimenting with filter design.
"""

import numpy as np
import random
import datetime

_rng = random.Random(datetime.datetime.now().timestamp())

def extract_grain(audio: np.array, start_point=None, grain_size=None, window="hanning") -> np.array:
    """
    Extracts a single grain from an array of samples.
    :param audio: A 1-dimensional Numpy array of audio samples
    :param start_point: The starting frame of the grain. If None, this will be randomly chosen.
    :param grain_size: The size of the grain in frames. If None, this will be randomly chosen.
    :param window: The window that will be applied to the grain.
    :return: A Numpy array with the grain
    """
    if audio is None:
        raise TypeError("You need to provide audio to granulate.")
    else:
        if start_point is None:
            start_point = _rng.randint(0, audio.shape[0] - 1)
        if grain_size is None:
            grain_size = _rng.randint(0, audio.shape[0] - 1 - start_point)
        grain = audio[start_point:start_point + grain_size]

        if window == "bartlett":
            window = np.bartlett(grain_size)
        elif window == "blackman":
            window = np.blackman(grain_size)
        elif window == "hanning":
            window = np.hanning(grain_size)
        elif window == "hamming":
            window = np.hamming(grain_size)
        else:
            window = np.ones((grain_size))
        
        return grain * window
