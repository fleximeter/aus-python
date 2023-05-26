import numpy as np
from scipy.io.wavfile import read
import scipy.fft
import sampler
import audiofile
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

a = audiofile.read_wav(file_name2)
b = audiofile.read_wav(file_name3)

audiofile.convert(a, "float32")
audiofile.convert(a, "int24")
audiofile.write_wav(a, "D:\\Desktop\\temp.wav")


# audiofile.write_aiff(b, "D:\\Desktop\\temp.aiff")

# x = a.samples[0, 16384:16384+4096]
# print(x.shape)

# s = scipy.fft.rfft(x)
# f = scipy.fft.rfftfreq(4096, 1/a.sample_rate)

# print(s.shape)
# print(f.shape)

# fig, ax = plt.subplots()
# ax.plot(f, np.abs(s))
# plt.show()


