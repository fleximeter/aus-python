import numpy as np
import matplotlib.pyplot as plt
import sampler
import wav

file_name = "D:\\Recording\\ReaperProjects\\trombone_samples\\samples\\trombone_sample_mute_9-19-22_a45_f.wav"
a = wav.read_wav(file_name)

env_amp = sampler.fit_amplitude_envelope(a, 500, 0)
peaks = sampler.detect_peaks(a, 0)
peak_difs = [peaks[i] - peaks[i-1] for i in range(1, len(peaks))]
# print(peak_difs[:100])

major_peaks = sampler.detect_major_peaks(a, 0.1, 5000, 0)
major_peak_difs = [major_peaks[i][0] - major_peaks[i-1][0] for i in range(1, len(major_peaks))]

y = major_peak_difs
x = [i for i in range(len(major_peak_difs))]
fig, ax = plt.subplots()
ax.plot(x, y)
plt.show()
