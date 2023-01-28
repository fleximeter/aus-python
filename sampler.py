"""
File: sampler.py
Author: Jeff Martin
Date: 1/26/23

This file contains functionality for processing audio files for use with samplers.
"""

import numpy as np
from wav import AudioFile

def identify_amplitude_regions(audio: AudioFile, level_delimiter: int = 0.01, num_consecutive: int = 10, channel_index: int = 0) -> list:
    """
    Identifies amplitude regions in a sound. You provide a threshold, and any time the threshold is
    breached, we start a new amplitude region which ends when we return below the threshold.
    :param audio: An AudioFile object with the contents of a WAV file
    :param level_delimiter: The lowest level allowed in a region. You should probably scale levels to between
    -1 and 1 before using this function.
    :param num_consecutive: The number of consecutive samples below the threshold required to end a region
    :param channel_index: The index of the channel in the AudioFile to study
    :return: A list of tuples. Each tuple contains the starting and ending frame index of an amplitude region.
    """
    regions = []
    current_region = None
    num_below_threshold = 0
    last_above_threshold = 0

    if len(audio.shape) > 1:
        audio = audio[channel_index, :]
    num_frames = audio.shape[0]

    for i in range(num_frames):
        if np.abs(audio[i]) >= level_delimiter:
            last_above_threshold = i
            num_below_threshold = 0
            if current_region is None:
                current_region = i
        elif np.abs(audio[i]) < level_delimiter:
            num_below_threshold += 1
            if current_region is not None and num_below_threshold >= num_consecutive:
                regions.append((current_region, last_above_threshold))
                current_region = None

    if current_region is not None:
        regions.append((current_region, num_frames - 1))
    return regions


def detect_peaks():
    pass
