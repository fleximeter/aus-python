"""
File: filter_experiment.py
Author: Jeff Martin
Date: 7/16/23

This file is for experimenting with filter design.
"""

import numpy as np
import audio_files
import audiopython.audiofile as af

def basic_filter(audio_data):
    """
    A basic third-order FIR lowpass filter
    :param audio_data: A Numpy array with audio samples
    :return: A filtered version of the array
    """
    filtered_audio = np.zeros(audio_data.shape)
    for i in range(audio_data.shape[0]):
        for j in range(3, audio_data.shape[1]):
            filtered_audio[i, j] = audio_data[i, j-3] / 4 + audio_data[i, j-2] / 4 + audio_data[i, j-1] / 4 + audio_data[i, j] / 4
    return filtered_audio

if __name__ == "__main__":
    x = af.read(audio_files.violin_samples[0])
    af.write_wav(x, "D:\\filter_before.wav")
    x.samples = basic_filter(x.samples)
    af.write_wav(x, "D:\\filter_after.wav")
