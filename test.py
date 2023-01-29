import numpy as np
import matplotlib.pyplot as plt
import sampler
import wav

file_name = "D:\\Recording\\ReaperProjects\\trombone_samples\\samples\\trombone_sample_mute_9-19-22_a45_f.wav"
a = wav.read_wav(file_name)

env_amp = sampler.fit_amplitude_envelope(a, 500, 0)
y = [tup[1] for tup in env_amp]
x = [tup[0] for tup in env_amp]
fig, ax = plt.subplots()
ax.plot(x, y)
plt.show()

peaks = sampler.detect_peaks(a, 0)
peak_difs = [peaks[i] - peaks[i-1] for i in range(1, len(peaks))]
print(peak_difs[:100])
