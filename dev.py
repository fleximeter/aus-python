import scipy.fft
import audiopython.sampler as sampler
import audiopython.spectrum as spectrum
import audiopython.audiofile as audiofile
import numpy as np
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
file_name11 = "D:\\Recording\\Samples\\Iowa\\Violin.arco.mono.1644.1\\Violin.arco.ff.sulA.A4B4.mono.aif"

# a = audiofile.read_wav(file_name2)
# b = audiofile.read_wav(file_name3)

# audiofile.convert(a, "float32")
# audiofile.convert(a, "int24")
# audiofile.write_wav(a, "D:\\Desktop\\temp.wav")

f = "D:\\Recording\\Samples\\pianobook\\YamahaC7\\YamahaC7\\Samples\\C#4_T1D.wav"

a = audiofile.read(file_name11)

regions = sampler.identify_amplitude_regions(a, 0.000001, num_consecutive=10000)

samples = sampler.extract_samples(a, regions, 10000, 10000, pre_envelope_frames=5000, post_envelope_frames=5000)
for i in range(len(samples)):
    audiofile.write_wav(samples[i], f"D:\\Recording\\Temp\\sample{i}.wav")

# audiofile.write_wav(a, "D:\\Desktop\\temp.wav")