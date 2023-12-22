"""
File: basic_operations.py
Author: Jeff Martin
Date: 12/2/23

This file allows you to perform some simple operations on an audio array.
"""

import librosa
import numpy as np
import pedalboard
np.seterr(divide="ignore")


def calculate_dc_bias(audio: np.array):
    """
    Calculates DC bias of an audio signal
    :param audio: The audio signal
    :return: The DC bias
    """
    return np.average(audio, axis=audio.ndim-1)


def dbfs_audio(audio: np.array) -> float:
    """
    Calculates dbfs (decibels full scale) for a chunk of audio. This function will use the RMS method, 
    and assumes that the audio is in float format where 1 is the highest possible peak.
    :param audio: The audio to calculate dbfs for
    :return: A float value representing the dbfs
    """
    try:
        rms = np.sqrt(np.average(np.square(audio), axis=audio.ndim-1))
        return 20 * np.log10(np.abs(rms))
    except RuntimeWarning:
        return -np.inf


def dbfs_max_local(audio: np.array, chunk_size=10, hop_size=5):
    """
    Checks the maximum local dbfs (decibels full scale) of an audio file
    :param audio: The audio
    :param chunk_size: The chunk size to check
    :param hop_size: The number of frames to hop from chunk center to chunk center
    :return: The max local dbfs
    """
    dbfs = -np.inf
    for i in range(0, len(audio), hop_size):
        end = min(i + chunk_size, len(audio) - 1)
        try:
            rms = np.sqrt(np.average(np.square(audio[i:end]), -1))
            dbfs = max(20 * np.log10(np.abs(rms)), dbfs)
        except RuntimeWarning:
            pass
    return dbfs


def dbfs_min_local(audio: np.array, chunk_size=10, hop_size=5):
    """
    Checks the minimum local dbfs (decibels full scale) of an audio file
    :param audio: The audio
    :param chunk_size: The chunk size to check
    :param hop_size: The number of frames to hop from chunk center to chunk center
    :return: The min local dbfs
    """
    dbfs = 0
    for i in range(0, len(audio), hop_size):
        end = min(i + chunk_size, len(audio) - 1)
        try:
            rms = np.sqrt(np.average(np.square(audio[i:end]), -1))
            dbfs = min(20 * np.log10(np.abs(rms)), dbfs)
        except RuntimeWarning:
            pass
    return dbfs


def dbfs_sample(sample) -> float:
    """
    Calculates dbfs (decibels full scale) for an audio sample. This function assumes that the 
    audio is in float format where 1 is the highest possible peak.
    :param sample: The sample to calculate dbfs for
    :return: A float value representing the dbfs
    """
    return 20 * np.log10(np.abs(sample))


def fade_in(audio: np.array, envelope="hanning", duration=100) -> np.array:
    """
    Implements a fade-in on an array of audio samples.
    :param audio: The array of audio samples (may have multiple channels; the fade-in will be applied to all channels)
    :param envelope: The shape of the fade-in envelope. Must be a NumPy envelope. The envelope will be divided in half, and only the first half will be used.
    :param duration: The duration (in frames) of the fade-in envelope half. If the duration is longer than the audio, it will be truncated.
    :return: The audio with a fade in applied.
    """
    duration = min(duration, audio.shape[-1])
        
    if envelope == "bartlett":
        envelope = np.bartlett(duration * 2)[:duration]
    elif envelope == "blackman":
        envelope = np.blackman(duration * 2)[:duration]
    elif envelope == "hanning":
        envelope = np.hanning(duration * 2)[:duration]
    elif envelope == "hamming":
        envelope = np.hamming(duration * 2)[:duration]
    else:
        envelope = np.ones((duration * 2))[:duration]
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
    duration = min(duration, audio.shape[-1])
        
    if envelope == "bartlett":
        envelope = np.bartlett(duration * 2)[duration:]
    elif envelope == "blackman":
        envelope = np.blackman(duration * 2)[duration:]
    elif envelope == "hanning":
        envelope = np.hanning(duration * 2)[duration:]
    elif envelope == "hamming":
        envelope = np.hamming(duration * 2)[duration:]
    else:
        envelope = np.ones((duration * 2))[duration:]
    envelope = np.hstack((np.ones((audio.shape[-1] - envelope.shape[-1])), envelope))
    
    return audio * envelope
    

def leak_dc_bias(audio: np.array) -> np.array:
    """
    Leaks DC bias of an audio signal
    :param audio: The audio signal
    :return: The bias-free signal
    """
    return audio - np.average(audio, axis=audio.ndim-1)


def midi_tuner(audio: np.array, midi_estimation, midi_division=1, sample_rate=44100, target_midi=None) -> np.array:
    """
    Retunes audio from a provided midi estimation to the nearest accurate MIDI note
    :param audio: The audio to tune
    :param midi_estimation: The MIDI estimation
    :param midi_division: The MIDI division to tune to (1 for nearest semitone, 0.5 for nearest quarter tone)
    :param sample_rate: The sample rate of the audio
    :param target_midi: If specified, overrides the rounding functionality and uses this as the target MIDI note
    :return: The tuned audio
    """
    if not target_midi:
        target_midi = round(float(midi_estimation / midi_division)) * midi_division
    ratio = 2 ** ((target_midi - midi_estimation) / 12)
    new_sr = sample_rate * ratio
    # print(midi_estimation, new_midi, ratio, new_sr)
    return librosa.resample(audio, orig_sr=new_sr, target_sr=sample_rate, res_type="soxr_vhq")


def mix_if_not_mono(audio: np.array) -> np.array:
    """
    Mixes a signal to a mono signal (if it isn't mono already). 
    If the amplitude is greater than 1, applies gain reduction to bring the amplitude down to 1.
    :param audio: The audio to mix if it isn't mono
    :return: The mixed audio
    """
    if audio.ndim > 1:
        mix = np.sum(audio, -2)
        mix = np.reshape(mix, (mix.shape[-1]))
        mixmax = np.max(mix)
        if mixmax > 1:
            mix /= mixmax
        return mix
    else:
        return audio
