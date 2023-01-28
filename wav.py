"""
File: wav.py
Author: Jeff Martin
Date: 1/25/23

This is a no-nonsense WAV file reader. Reference: https://ccrma.stanford.edu/courses/422-winter-2014/projects/WaveFormat/
"""

import numpy as np

HEADER_SIZE = 44
LARGE_FIELD = 4
SMALL_FIELD = 2

class AudioFile:
    def __init__(self):
        self.bits_per_sample = 0
        self.byte_rate = 0
        self.bytes_per_sample = 0
        self.header = b""
        self.num_channels = 0
        self.num_frames = 0
        self.sample_rate = 0
        self.samples = None
        self.scaling_factor = 0


def read_wav(file_name) -> AudioFile:
    """
    Reads a WAV file and returns an AudioFile object with the data.
    :param file_name: The name of the file
    :return: An AudioFile object with the contents of the WAV file
    """
    audio_file = AudioFile()
    audio_data = []
    with open(file_name, "rb") as audio:
        # Read the header. We will store the entire header in the AudioFile object which will make it easier to write
        # back to the file.
        audio_file.header = audio.read(HEADER_SIZE)
        audio_file.num_channels = int.from_bytes(audio_file.header[22:24], byteorder="little", signed=False)
        audio_file.sample_rate = int.from_bytes(audio_file.header[24:28], byteorder="little", signed=False)
        audio_file.byte_rate = int.from_bytes(audio_file.header[28:32], byteorder="little", signed=False)
        audio_file.bits_per_sample = int.from_bytes(audio_file.header[34:36], byteorder="little", signed=False)
        audio_file.bytes_per_sample = audio_file.bits_per_sample // 8
        audio_file.num_frames = (int.from_bytes(audio_file.header[4:8], byteorder="little", signed=False) - 36) // (audio_file.num_channels * audio_file.bytes_per_sample)
        
        # Read the samples. The channels are interleaved, so for now we will read the samples for all channels together.
        for i in range(audio_file.num_frames):
            audio_data.append(audio.read(audio_file.bytes_per_sample * audio_file.num_channels))

        samples = np.zeros((audio_file.num_channels, audio_file.num_frames), dtype=np.int32)
        audio_file.samples = np.zeros((audio_file.num_channels, audio_file.num_frames), dtype=np.float32)

        # Separate the samples from different channels. The 2D array is of dimension num channels x num frames.
        for i in range(audio_file.num_frames):
            for j in range(audio_file.num_channels):
                samples[j, i] = int.from_bytes(audio_data[i][j * audio_file.bytes_per_sample : (j + 1) * audio_file.bytes_per_sample], byteorder="little", signed=True)
        
        audio_file.samples = samples
        # Scale the samples to float values from -1 to 1.
        # audio_file.scaling_factor = np.max(np.abs(samples))
        # for i in range(audio_file.num_frames):
        #     for j in range(audio_file.num_channels):
        #         audio_file.samples[j, i] = samples[j, i] / audio_file.scaling_factor
        

    return audio_file


def write_wav(file: AudioFile, path: str):
    """
    Writes an audio file
    :param file: An AudioFile representation of the file
    :param path: A file path
    :return: None
    Note that in the AudioFile, the following parameters should be properly set:
    - num_channels (e.g. 1)
    - sample_rate (e.g. 44000)
    - byte_rate
    - bits_per_sample (e.g. 16, 24, 32)
    - bytes_per_sample (e.g. 2, 3, 4)
    - num_samples
    - num_frames
    - scaling_factor
    """
    with open(path, "wb") as audio:
        header = b"".join([
            b"RIFF",
            (36 + file.num_frames * file.num_channels * file.bytes_per_sample).to_bytes(LARGE_FIELD, byteorder="little", signed=False),
            b"WAVE",
            b"fmt ",
            int(16).to_bytes(LARGE_FIELD, byteorder="little", signed=False),
            int(1).to_bytes(SMALL_FIELD, byteorder="little", signed=False),
            file.num_channels.to_bytes(SMALL_FIELD, byteorder="little", signed=False),
            file.sample_rate.to_bytes(LARGE_FIELD, byteorder="little", signed=False),
            file.byte_rate.to_bytes(LARGE_FIELD, byteorder="little", signed=False),
            (file.num_channels * file.bytes_per_sample).to_bytes(SMALL_FIELD, byteorder="little", signed=False),
            file.bits_per_sample.to_bytes(SMALL_FIELD, byteorder="little", signed=False),
            b"data",
            (file.num_frames * file.num_channels * file.bytes_per_sample).to_bytes(LARGE_FIELD, byteorder="little", signed=False)
        ])
        audio.write(header)
        for i in range(file.num_frames):
            for j in range(file.num_channels):
                audio.write(int(file.samples[j, i] * file.scaling_factor).to_bytes(file.bytes_per_sample, byteorder="little", signed=True))

def scale_wav(wav_data):
    """
    Scales a provided NumPy array with wavfile data
    :param wav_data: A NumPy array
    :return: The scaling denominator and a scaled array
    """
    scaler = np.max(wav_data)
    return scaler, wav_data / scaler
