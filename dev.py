import numpy as np
from scipy.io.wavfile import read
import sampler
import wav

file_name = "D:\\Recording\\ReaperProjects\\trombone_samples\\samples\\trombone_sample_mute_9-19-22_a45_f.wav"
file_name1 = "D:\\Recording\\Samples\\pianobook\\YamahaC7\\YamahaC7\\Samples\\A#5_T1B.wav"
file_name2 = "D:\\Desktop\\sample24.wav"
file_name3 = "D:\\Desktop\\sample32.wav"
file_name4 = "C:\\Users\jeff_martin\Desktop\sample24.wav"
file_name5 = "C:\\Users\jeff_martin\Desktop\sample32.wav"

b_rate, b = read(file_name2)
print(f"Sample rate: {b_rate}, number of frames: {len(b)}")
a = wav.read_wav(file_name2)

print(b.shape)
print(len(b), a.num_frames)
print(a.bits_per_sample)

print(b[100, 0], a.samples[0, 100])
for i in range(10):
    if b[i, 1] == a.samples[1, i] * 256:
        pass
        #print(f"Match {i}")
    else:
        print(f"No match for sample index {i}: {b[i, 1]} {a.samples[1, i]}")

wav.visualize_wav(a, (0, 1), (1000, 2000))
# scaler, b_scaled = wav.scale_wav(b)

wav.write_wav(a, "D:\\Desktop\\temp.wav", True)

# regions = sampler.identify_amplitude_regions(b_scaled, 0.001, 1000, 0)
# print(regions)

