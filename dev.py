import numpy as np
from scipy.io.wavfile import read
import scipy.fft
import sampler
import wav
import matplotlib.pyplot as plt
import struct
import math

file_name = "D:\\Recording\\ReaperProjects\\trombone_samples\\samples\\trombone_sample_mute_9-19-22_a69_p.wav"
file_name1 = "D:\\Recording\\Samples\\pianobook\\YamahaC7\\YamahaC7\\Samples\\A#5_T1B.wav"
file_name2 = "D:\\Desktop\\sample24.wav"
file_name3 = "D:\\Desktop\\sample32.wav"
file_name4 = "C:\\Users\jeff_martin\Desktop\sample24.wav"
file_name5 = "C:\\Users\jeff_martin\Desktop\sample32.wav"
file_name6 = "D:\\Desktop\\sample16.aif"
file_name7 = "D:\\Desktop\\sample24.aif"
file_name8 = "D:\\Desktop\\sample32.aif"
file_name9 = "C:\\Users\jeff_martin\Desktop\sample24.aif"
file_name10 = "C:\\Users\jeff_martin\Desktop\sample32.aif"

a = wav.read_wav(file_name2)
print(a.samples.shape)

# x = a.samples[0, 16384:16384+4096]
# print(x.shape)

# s = scipy.fft.rfft(x)
# f = scipy.fft.rfftfreq(4096, 1/a.sample_rate)

# print(s.shape)
# print(f.shape)

# fig, ax = plt.subplots()
# ax.plot(f, np.abs(s))
# plt.show()

def unpack_float80(bytes):
    """
    A hack to get the sample rate from a float 80 number. Since Python doesn't really have
    native support for the float80 format, we have to be creative. We take advantage of the
    fact that the sample rate will always be a whole number, and discard the decimal part.
    :param bytes: Some bytes representing a float 80 number
    :return: An integer with the whole number part
    """
    chunk1 = int.from_bytes(bytes[:2], byteorder="big", signed=False)
    # sign = chunk1 >> 15  # extract the sign bit (this is unnecessary because sample rates are never negative)
    exponent = (chunk1 << 1) >> 1  # get rid of the sign bit
    exponent -= 16383  # 2 ** 14 - 1 (the sign part is two's complement)
    num_bytes = math.ceil(exponent/8)
    int_part = int.from_bytes(bytes[2:2+num_bytes], byteorder="big", signed=False)
    int_part >>= num_bytes * 8 - exponent - 1
    return int_part
    

def pack_float80(num):
    """
    Packs a sample rate to float 80 format.
    :param num: An integer to convert
    :return: The packed format
    """
    int_part = num.to_bytes(length=8, byteorder="big", signed=False)
    exp = math.ceil(math.log2(num)) - 1 + 16383
    exp_part = exp.to_bytes(2, byteorder="big", signed=False)
    print(int_part[-2:], exp)


# http://paulbourke.net/dataformats/audio/
# http://midi.teragonaudio.com/tech/aiff.htm
with open(file_name6, "rb") as audio:
    HEADER1 = b'FORM'
    HEADER2 = b'AIFF'
    HEADER3 = b'COMM'
    HEADER4 = b'SSND'
    
    eof = False

    while not eof:
        chunk_title = audio.read(4)
        if len(chunk_title) < 4:
            eof = True
        
        # read the form chunk
        elif chunk_title == HEADER1:
            file_size = audio.read(4)
            file_size = int.from_bytes(file_size, byteorder="big", signed=False)
            label = audio.read(4)
            if label != HEADER2:
                raise Exception(message="File is corrupted and cannot be read.")
        
        # read the common chunk
        elif chunk_title == HEADER3:
            chunk_size = audio.read(4)
            chunk_size = int.from_bytes(chunk_size, byteorder="big", signed=False)
            common_chunk = audio.read(chunk_size)
            num_channels = int.from_bytes(common_chunk[:2], byteorder="big", signed=False) # number of channels
            num_frames = int.from_bytes(common_chunk[2:6], byteorder="big", signed=False) # number of frames
            sample_size_bits = int.from_bytes(common_chunk[6:8], byteorder="big", signed=False) # sample size (bits)
            sample_size_bytes = sample_size_bits // 8
            sample_rate = unpack_float80(common_chunk[8:])
            print(sample_rate)
            # discard = int.from_bytes(common_chunk[8:10], byteorder="big", signed=False) # ?? I don't know what this is
            # sample_rate = int.from_bytes(common_chunk[10:12], byteorder="big", signed=False) # sample rate
        
        # read the samples
        elif chunk_title == HEADER4:
            sound_chunk_size = audio.read(4)
            sound_chunk_size = int.from_bytes(sound_chunk_size, byteorder="big", signed=False)
            
            # Read the offset and block size, which will probably be 0
            offset = audio.read(4)
            offset = int.from_bytes(offset, byteorder="big", signed=False)
            block_size = audio.read(4)
            block_size = int.from_bytes(block_size, byteorder="big", signed=False)
            
            # Read the rest of the file
            data = audio.read()
            samples = np.zeros((num_channels, num_frames))
            frame_size = sample_size_bytes * num_channels
            k = 0
            for i in range(0, len(data), frame_size):
                for j in range(0, num_channels):
                    start_point = i + j * sample_size_bytes
                    samples[j, k] = int.from_bytes(data[start_point:start_point+sample_size_bytes], byteorder="big", signed=True)
                k += 1

pack_float80(44100)