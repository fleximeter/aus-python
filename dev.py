import scipy.fft
import audiopython.sampler as sampler
import audiopython.spectrum as spectrum
import audiopython.audiofile as audiofile
import audio_files
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal


f = audiofile.read("D:\\Recording\\Samples\\Iowa\\Cello.arco.mono.1644.1\\ff\\Cello.arco.ff.sulA.A4A5.mono.aif")
print(f.num_frames)
print(np.max(f.samples))
print(f.samples[:, :5])
sampler.identify_amplitude_regions(f, 0.3)
    
# a = audiofile.read(sample_files)
# print(a.num_frames)
# print(type(a.samples))

# f, t, Zxx = scipy.signal.stft(a.samples[0, :], 44100, window='hann', nperseg=4096)

# print(f[:20])