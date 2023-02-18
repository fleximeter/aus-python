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


def detect_major_peaks(audio: AudioFile, min_percentage_of_max: float = 0.9, chunk_width: int = 5000, channel_index: int = 0) -> list:
    """
    Detects major peaks in an audio file. A major peak is a peak that is one of the highest in its local region.
    
    The local region is specified by the chunk width. We segment the audio file into segments of width chunk_width,
    and search for the highest peak in that chunk. Then we identify all other peaks that are close in height
    to the highest peak. A peak is close in height to said peak if it is greater than or equal to min_percentage_of_max
    of that peak. (For example, suppose the highest peak is 1, and the min_percentage_of_max is 0.9. Then any peak with
    amplitude from 0.9 to 1 will be considered a major peak.)
    
    :param audio: An AudioFile object with the contents of a WAV file
    :param min_percentage_of_max: A peak must be at least this percentage of the maximum peak to be included as a major
    peak.
    :param chunk_width: The width of the chunk to search for the highest peak
    :param channel_index: The index of the channel to scan for peaks
    :return: Returns a list of tuples; the tuple has an index and an amplitude value.
    """
    peaks = []
    for i in range(1, audio.num_frames - 1, chunk_width):
        # Get the index and absolute value of the highest peak in the current chunk
        peak_idx = i + np.argmax(np.abs(audio.samples[channel_index, i:i+chunk_width]))
        peak_val = np.abs(audio.samples[channel_index, peak_idx])
        
        # print(peak_idx, peak_val)

        # Iterate through the current chunk and find all major peaks
        j = i
        while j < i + chunk_width and j < audio.num_frames - 1:
            if (
                # If the current sample is a positive peak (both neighboring samples are lower)
                ((audio.samples[channel_index, j-1] < audio.samples[channel_index, j] > audio.samples[channel_index, j+1] \
                    and audio.samples[channel_index, j] > 0) \
                
                # Or the sample is a negative peak (both neighboring samples are higher)
                or (audio.samples[channel_index, j-1] > audio.samples[channel_index, j] < audio.samples[channel_index, j+1] \
                    and audio.samples[channel_index, j] < 0)) \
                
                # And the peak is a major peak
                and np.abs(audio.samples[channel_index, j]) >= peak_val * min_percentage_of_max
            ):
                peaks.append((j, audio.samples[channel_index, j]))
            j += 1

    return peaks


def detect_loop_points(audio: AudioFile, channel_index: int = 0, num_periods: int = 5) -> list:
    """
    Detects loop points in an audio sample. Loop points are frame indices that could be used for
    a seamless repeating loop in a sampler. Ideally, if you choose loop points correctly, no crossfading
    would be needed within the loop.
    We have several requirements for a good loop:
    1. The standard deviation of peak amplitudes should be minimized (i.e. the loop is not increasing or decreasing in amplitude)
    2. The distance between successive wave major peaks should be consistent
    3. The frames at which looping begins and ends should have values as close to 0 as possible
    :param audio: An AudioFile object
    :param channel_index: The index of the channel to scan for loops (you really should use mono audio 
    with a sampler)
    :param num_periods: The number of periods to include from the waveform
    :return: A list of tuples that are start and ending frames for looping
    """

    # This is the maximum percentage of amplitude variance that will be allowed.
    # We want the loop to be dynamically stable.
    MAX_AMPLITUDE_VARIANCE = 0.5

    # We need an effective zero point. We will arbitrarily assume that a level less than 0.001 can serve
    # as a zero point here. If we are storing as int, we need to scale this number.
    EFFECTIVE_ZERO = 0.01
    if type(audio.samples[0, 0]) == np.int16 \
        or type(audio.samples[0, 0]) == np.int32 \
        or type(audio.samples[0, 0]) == np.int64: 
        EFFECTIVE_ZERO *= 0.001 * 2 ** (audio.bits_per_sample - 1)

    # The major peaks in the sound file.
    major_peaks = detect_major_peaks(audio, 0.9, 5000, channel_index)
    
    # This stores frame tuples that identify potential loop points.
    frame_tuples = []

    # We will try to build a loop starting at each peak, then shifting backward to a zero point.
    for i in range(len(major_peaks)):
        potential_loop_peaks = []
        
        # We will use these two valuse to determine if there is too much dynamic variation
        # within the proposed loop.
        max_peak = -np.inf  # the absolute value of the major peak with greatest magnitude
        min_peak = np.inf  # the absolute value of the major peak with least magnitude
    
        # We start by grabbing peaks for the minimum number of periods necessary. We have to 
        # grab an extra peak to complete the final period.
        for j in range(i, min(i + num_periods * 2 + 1, len(major_peaks))):
            potential_loop_peaks.append(major_peaks[j])
            peak_abs = np.abs(major_peaks[j][1])
            if peak_abs > max_peak:
                max_peak = peak_abs
            elif peak_abs < min_peak:
                min_peak = peak_abs
        
        # If we weren't able to pull enough periods, we can't continue with making the loop.
        if len(potential_loop_peaks) // 2 < num_periods:
            break

        # If there's too much dynamic variation in this audio chunk, we can't continue with
        # making the loop.
        if 1 - (max_peak - min_peak) / max_peak > MAX_AMPLITUDE_VARIANCE:
            break

        # We need to record loop points now. Recall that the final peak is actually the beginning
        # of the next period, so we need to move back one sample.
        loop_points = [potential_loop_peaks[0][0], potential_loop_peaks[-1][0] - 1]
        period_width = len(potential_loop_peaks) // num_periods

        # Now we shift back to make the loop start and end on 0. There might be multiple possible
        # places where the loop could start and end on 0.
        while loop_points[0] + period_width > potential_loop_peaks[0][0] and loop_points[0] >= 0:
            while audio.samples[channel_index, loop_points[0]] > EFFECTIVE_ZERO and loop_points[0] >= 0:
                loop_points[0] -= 1
                loop_points[1] -= 1

            # If we've found good loop points, we will record them.
            if audio.samples[channel_index, loop_points[0]] < EFFECTIVE_ZERO \
                and audio.samples[channel_index, loop_points[1]] < EFFECTIVE_ZERO:
                frame_tuples.append((loop_points[0], loop_points[1]))

    return frame_tuples
