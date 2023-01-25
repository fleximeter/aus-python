import read

a = read.read_wav("D:\\Recording\\Samples\\pianobook\\YamahaC7\\YamahaC7\\Samples\\A#5_T1B.wav")
print(a.sample_rate, a.num_channels, a.num_samples, a.bytes_per_sample)
print(a.samples[0, :100])