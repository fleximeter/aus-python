import numpy as np
import sampler
import wav

a = wav.read_wav("D:\\Recording\\Samples\\pianobook\\YamahaC7\\YamahaC7\\Samples\\A#5_T1B.wav")
print(a.sample_rate, a.num_channels, a.num_frames, a.bytes_per_sample)

print(a.samples[0, :20])

regions = sampler.identify_amplitude_regions(a, 0.001, 100, 0)
print(regions)

# wav.write_wav(a, "D:\\Desktop\\temp.wav")