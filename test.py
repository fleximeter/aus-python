import wav

a = wav.read_wav("D:\\Recording\\Samples\\pianobook\\YamahaC7\\YamahaC7\\Samples\\A#5_T1B.wav")
print(a.sample_rate, a.num_channels, a.num_samples, a.bytes_per_sample)
print(a.header)
wav.write_wav(a, "D:\\Desktop\\temp.wav")