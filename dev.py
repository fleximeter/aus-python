import numpy as np
from scipy.io.wavfile import read
import scipy.fft
import sampler
import wav
import matplotlib.pyplot as plt

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

# a = wav.read_wav(file_name)

# x = a.samples[0, 16384:16384+4096]
# print(x.shape)

# s = scipy.fft.rfft(x)
# f = scipy.fft.rfftfreq(4096, 1/a.sample_rate)

# print(s.shape)
# print(f.shape)

# fig, ax = plt.subplots()
# ax.plot(f, np.abs(s))
# plt.show()

# http://paulbourke.net/dataformats/audio/
with open(file_name6, "rb") as audio:
    HEADER1 = b'FORM'
    HEADER2 = b'AIFF'
    HEADER3 = b'COMM'
    HEADER4 = b'SSND'
    
    title = audio.read(4)
    file_size = audio.read(4)
    file_size = int.from_bytes(file_size, byteorder="big", signed=False)
    label1 = audio.read(4)
    if title != HEADER1 or label1 != HEADER2:
        pass # error condition 1

    # Read the common chunk
    label2 = audio.read(4) # HEADER3
    if label2 != HEADER3:
        pass # error condition 2

    size = audio.read(4)
    size = int.from_bytes(size, byteorder="big", signed=False)
    common_chunk = audio.read(size)
    
    # Read the sound chunk
    label3 = audio.read(4) # HEADER4
    if label3 != HEADER4:
        pass # error condition 3

    sound_chunk_size = audio.read(4)
    sound_chunk_size = int.from_bytes(sound_chunk_size, byteorder="big", signed=False)
    
    # Read the offset and block size, which will probably be 0
    offset = audio.read(4)
    offset = int.from_bytes(offset, byteorder="big", signed=False)
    block_size = audio.read(4)
    block_size = int.from_bytes(block_size, byteorder="big", signed=False)
    
    # Read the rest of the file
    data = audio.read()
    