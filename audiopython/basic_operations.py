"""
File: basic_operations.py
Author: Jeff Martin
Date: 12/2/23

This file allows you to perform some simple operations on an audio array.
"""

import numpy as np


def dbfs(audio: np.array) -> float:
    """
    Calculates dbfs (decibels full scale) for a chunk of audio. This function will use the RMS method, 
    and assumes that the audio is in float format where 1 is the highest possible peak.
    :param audio: The audio to calculate dbfs for
    :return: A float value representing the dbfs
    """
    rms = np.sqrt(np.average(np.square(audio), axis=audio.ndim-1))
    return 20 * np.log10(np.abs(rms))


def fade_in(audio: np.array, envelope="hanning", duration=100) -> np.array:
    """
    Implements a fade-in on an array of audio samples.
    :param audio: The array of audio samples (may have multiple channels; the fade-in will be applied to all channels)
    :param envelope: The shape of the fade-in envelope. Must be a NumPy envelope. The envelope will be divided in half, and only the first half will be used.
    :param duration: The duration (in frames) of the fade-in envelope half. If the duration is longer than the audio, it will be truncated.
    :return: The audio with a fade in applied.
    """
    duration = np.min(duration, audio.shape[-1])
        
    if envelope == "bartlett":
        envelope = np.bartlett(duration)[:duration // 2]
    elif envelope == "blackman":
        envelope = np.blackman(duration)[:duration // 2]
    elif envelope == "hanning":
        envelope = np.hanning(duration)[:duration // 2]
    elif envelope == "hamming":
        envelope = np.hamming(duration)[:duration // 2]
    else:
        envelope = np.ones((duration))[:duration // 2]
    envelope = np.hstack((envelope, np.ones((audio.shape[-1] - envelope.shape[-1]))))
    
    return audio * envelope
    

def fade_out(audio: np.array, envelope="hanning", duration=100) -> np.array:
    """
    Implements a fade-out on an array of audio samples.
    :param audio: The array of audio samples (may have multiple channels; the fade-out will be applied to all channels)
    :param envelope: The shape of the fade-out envelope. Must be a NumPy envelope. The envelope will be divided in half, and only the second half will be used.
    :param duration: The duration (in frames) of the fade-out envelope half. If the duration is longer than the audio, it will be truncated.
    :return: The audio with a fade-out applied.
    """
    duration = np.min(duration, audio.shape[-1])
        
    if envelope == "bartlett":
        envelope = np.bartlett(duration)[duration // 2:]
    elif envelope == "blackman":
        envelope = np.blackman(duration)[duration // 2:]
    elif envelope == "hanning":
        envelope = np.hanning(duration)[duration // 2:]
    elif envelope == "hamming":
        envelope = np.hamming(duration)[duration // 2:]
    else:
        envelope = np.ones((duration))[duration // 2:]
    envelope = np.hstack((np.ones((audio.shape[-1] - envelope.shape[-1])), envelope))
    
    return audio * envelope
    
