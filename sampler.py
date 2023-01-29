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

    for i in range(audio.num_frames):
        if np.abs(audio.samples[channel_index, i]) >= level_delimiter:
            last_above_threshold = i
            num_below_threshold = 0
            if current_region is None:
                current_region = i
        elif np.abs(audio.samples[channel_index, i]) < level_delimiter:
            num_below_threshold += 1
            if current_region is not None and num_below_threshold >= num_consecutive:
                regions.append((current_region, last_above_threshold))
                current_region = None

    if current_region is not None:
        regions.append((current_region, audio.num_frames - 1))
    return regions


def detect_peaks(audio: AudioFile, channel_index: int = 0) -> list:
    """
    Detects peaks in an audio file.
    :param audio: An AudioFile object with the contents of a WAV file
    :param channel_index: The index of the channel to scan for peaks
    :return: Returns a list of indices; each index corresponds to a frame with a peak in the selected channel.
    """
    peaks = []
    for i in range(1, audio.num_frames - 1):
        if audio.samples[channel_index, i-1] < audio.samples[channel_index, i] > audio.samples[channel_index, i+1] \
            and audio.samples[channel_index, i] > 0:
            peaks.append(i)
        elif audio.samples[channel_index, i-1] > audio.samples[channel_index, i] < audio.samples[channel_index, i+1] \
            and audio.samples[channel_index, i] < 0:
            peaks.append(i)
    return peaks


def fit_amplitude_envelope(audio: AudioFile, chunk_width: int = 5000, channel_index: int = 0) -> list:
    """
    Fits an amplitude envelope to a provided audio file.
    Detects peaks in an audio file. Peaks are identified by being surrounded by lower absolute values to either side.
    :param audio: An AudioFile object with the contents of a WAV file
    :param chunk_width: The AudioFile is segmented into adjacent chunks, and we look for the highest peak amplitude 
    in each chunk.
    :param channel_index: The index of the channel to scan for peaks
    :return: Returns a list of tuples; the tuple has an index and an amplitude value.
    """
    envelope = []
    for i in range(0, audio.num_frames, chunk_width):
        peak_idx = np.argmax(np.abs(audio.samples[channel_index, i:i+chunk_width]))
        envelope.append((i + peak_idx, np.abs(audio.samples[channel_index, i + peak_idx])))
    return envelope


def detect_major_peaks(audio: AudioFile, max_difference_ratio: float = 0.1, chunk_width: int = 5000, channel_index: int = 0) -> list:
    """
    Detects major peaks in an audio file. A major peak is a peak that is one of the highest in its local region.
    The local region is specified by the chunk width. We segment the audio file into segments of width chunk_width,
    and search for the highest peak in that chunk. Then we identify all other peaks that are close in height
    to the max peak. A peak is close in height to the max peak if it is within max_difference_ratio of that peak.
    :param audio: An AudioFile object with the contents of a WAV file
    :param max_difference_ratio: We detect the max peak in a range, and eliminate all peaks that are not within this fraction of that peak.
    :param chunk_width: The width of the chunk to search for the highest peak
    :param channel_index: The index of the channel to scan for peaks
    :return: Returns a list of tuples; the tuple has an index and an amplitude value.
    """
    peaks = []
    for i in range(1, audio.num_frames - 1, chunk_width):
        peak_idx = i + np.argmax(np.abs(audio.samples[channel_index, i:i+chunk_width]))
        peak_val = np.abs(audio.samples[channel_index, peak_idx])
        print(peak_idx, peak_val)

        j = i
        while j < i + chunk_width and j < audio.num_frames - 1:
            if ((audio.samples[channel_index, j-1] < audio.samples[channel_index, j] > audio.samples[channel_index, j+1] and audio.samples[channel_index, j] > 0) \
                or (audio.samples[channel_index, j-1] > audio.samples[channel_index, j] < audio.samples[channel_index, j+1] and audio.samples[channel_index, j] < 0)) \
                and np.abs((peak_val - np.abs(audio.samples[channel_index, j])) / peak_val) <= max_difference_ratio:
                peaks.append((j, audio.samples[channel_index, j]))
            j += 1

    return peaks
