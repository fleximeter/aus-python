"""
File: granulator.py
Author: Jeff Martin
Date: 7/16/23

This file is for experimenting with granular synthesis.
"""

import numpy as np
import random
import datetime

_rng = random.Random(datetime.datetime.now().timestamp())

def extract_grain(audio: np.array, start_point=None, grain_size=None, window="hanning", max_window_size=None) -> np.array:
    """
    Extracts a single grain from an array of samples.
    :param audio: A numpy array of audio samples
    :param start_point: The starting frame of the grain. If None, this will be randomly chosen.
    :param grain_size: The size of the grain in frames. If None, this will be randomly chosen.
    :param window: The window that will be applied to the grain.
    :param max_window_size: If specified, the window will not be larger than this size. If the grain is longer,
    the window will be split and only applied to the start and end of the grain.
    :return: A Numpy array with the grain
    """
    if audio is None:
        raise TypeError("You need to provide audio to granulate.")
    else:
        if start_point is None:
            start_point = _rng.randint(0, audio.shape[0] - 1)
        if grain_size is None:
            grain_size = _rng.randint(0, audio.shape[0] - 1 - start_point)
        if max_window_size is None:
            max_window_size = grain_size
        elif max_window_size > grain_size:
            max_window_size = grain_size
        grain = audio[start_point:start_point + grain_size]

        if window == "bartlett":
            window = np.bartlett(max_window_size)
        elif window == "blackman":
            window = np.blackman(max_window_size)
        elif window == "hanning":
            window = np.hanning(max_window_size)
        elif window == "hamming":
            window = np.hamming(max_window_size)
        else:
            window = np.ones((max_window_size))
        
        if max_window_size < grain_size:
            window = np.hstack((window[:max_window_size // 2], np.ones((grain_size - max_window_size)), window[max_window_size // 2:]))
        
        return grain * window


def merge_grains(grains: list, overlap_size=10) -> np.array:
    """
    Merges a list of grains, with some overlap between grains
    :param grains: A list of grains
    :param overlap_size: The number of samples to overlap from grain to grain
    :return: An array with the combined grains
    """
    current_grain = 1
    output = grains[0]
    while current_grain < len(grains):
        output = np.hstack((output[:-overlap_size], output[-overlap_size:] + grains[current_grain][:overlap_size], grains[current_grain][overlap_size:]))
        current_grain += 1
    return output
