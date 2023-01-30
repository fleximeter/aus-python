"""
File: wav.py
Author: Jeff Martin
Date: 1/25/23

This is a no-nonsense WAV file reader. Reference: https://ccrma.stanford.edu/courses/422-winter-2014/projects/WaveFormat/
For future reference, to support 32-bit float files, reference https://www.sounddevices.com/32-bit-float-files-explained/.
"""

import numpy as np

LARGE_FIELD = 4
SMALL_FIELD = 2


class AudioFile:
    def __init__(self):
        self.bits_per_sample = 0
        self.block_align = 0
        self.byte_rate = 0
        self.bytes_per_sample = 0
        self.duration = 0
        self.num_channels = 0
        self.num_frames = 0
        self.sample_rate = 0
        self.samples = None
        self.scaling_factor = 1


def read_wav(file_name) -> AudioFile:
    """
    Reads a WAV file and returns an AudioFile object with the data. Currently this implementation
    supports reading 16-bit and 24-bit WAV files, and should support any sample rate. 32-bit float
    files are not yet supported.
    The advantage of this implementation over the SciPy wavfile functionality is that it preserves
    more information so that you can reconstruct the original WAV file more accurately. For example,
    SciPy (at the time of writing) stores 24-bit samples in np.int32 format *but* left-shifts the
    absolute value of every sample by 8 bytes, inflating the amplitude. This implementation does
    not do that. Furthermore, it records the bit depth of the file so that you can actually write
    in 24-bit format. 
    :param file_name: The name of the file
    :return: An AudioFile object with the contents of the WAV file
    """
    audio_file = AudioFile()
    with open(file_name, "rb") as audio:
        # Read the header. We will store the entire header in the AudioFile object which will make it easier to write
        # back to the file.
        CHUNK_HEADER_SIZE = 8
        RIFF_CHUNK_SIZE = 12
        RIFF_CHUNK_1 = b'RIFF'
        RIFF_CHUNK_3 = b'WAVE'
        FMT_CHUNK_1 = b'fmt '
        DATA_CHUNK_1 = b'data'
        remaining_size = 0
        chunk_riff = audio.read(RIFF_CHUNK_SIZE)
        
        # We use this to validate the file as we go. If we encounter corrupt data, we will flip this to False.
        valid_file = True

        # Validate the RIFF chunk before proceeding
        if chunk_riff[:4] != RIFF_CHUNK_1 or chunk_riff[8:] != RIFF_CHUNK_3:
            valid_file = False
        else:
            remaining_size = int.from_bytes(chunk_riff[4:8], byteorder="little", signed=False)
        
        # Read the format subchunk
        if valid_file:
            data = audio.read(CHUNK_HEADER_SIZE)
            remaining_size -= CHUNK_HEADER_SIZE
            if data[:4] != FMT_CHUNK_1:
                valid_file = False
            else:
                fmt_chunk_size = int.from_bytes(data[4:], byteorder="little", signed=False)
                fmt_chunk = audio.read(fmt_chunk_size)
                remaining_size -= fmt_chunk_size

                # Verify that the format is PCM
                if int.from_bytes(fmt_chunk[:2], byteorder="little", signed=False) != 1:
                    valid_file = False
                
                # If the format is PCM, we continue and read the rest of the format subchunk
                else:
                    audio_file.num_channels = int.from_bytes(fmt_chunk[2:4], byteorder="little", signed=False)                    
                    audio_file.sample_rate = int.from_bytes(fmt_chunk[4:8], byteorder="little", signed=False)
                    audio_file.byte_rate = int.from_bytes(fmt_chunk[8:12], byteorder="little", signed=False)
                    audio_file.block_align = int.from_bytes(fmt_chunk[12:14], byteorder="little", signed=False)
                    audio_file.bits_per_sample = int.from_bytes(fmt_chunk[14:16], byteorder="little", signed=False)
                    audio_file.bytes_per_sample = audio_file.bits_per_sample // 8

        # Now that the file has been read, we continue to read the remaining subchunks.
        # The only remaining subchunk we are interested in is the data subchunk.
        if valid_file:
            while remaining_size > 0:
                subchunk_header = audio.read(CHUNK_HEADER_SIZE)
                remaining_size -= CHUNK_HEADER_SIZE
                subchunk_size = int.from_bytes(subchunk_header[4:8], byteorder="little", signed=False)
                subchunk_data = audio.read(subchunk_size)
                remaining_size -= subchunk_size

                # Detect if we've read a data subchunk. If this is something else
                # (e.g. a JUNK subchunk), we ignore it.
                if subchunk_header[:4] == DATA_CHUNK_1:
                    audio_file.num_frames = subchunk_size // (audio_file.num_channels * audio_file.bytes_per_sample)
                    audio_file.samples = np.zeros((audio_file.num_channels, audio_file.num_frames), dtype=np.int32)
                    for i in range(0, subchunk_size, audio_file.block_align):
                        j = i // audio_file.block_align
                        for k in range(0, audio_file.num_channels):
                            audio_file.samples[k, j] = int.from_bytes(
                                subchunk_data[i + k * audio_file.num_channels : i + k * audio_file.num_channels + audio_file.bytes_per_sample],
                                byteorder="little",
                                signed=True
                            )
                    audio_file.duration = audio_file.num_frames / audio_file.sample_rate

    # If the WAV file was formatted unusually (for example, not in PCM), we return nothing
    # and raise a warning.
    if valid_file:
        return audio_file
    else:
        raise RuntimeWarning("The WAV file was unusually formatted and could not be read." +
            "This might be because you tried to read a WAV file that was not in PCM format.")


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


def scale_wav(file: AudioFile):
    """
    Scales a provided AudioFile
    :param file: An AudioFile
    """
    file.scaling_factor = np.max(np.abs(file.samples))
    file.samples = file.samples / file.scaling_factor
