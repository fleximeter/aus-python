import scipy.fft
import audiopython.sampler as sampler
import audiopython.spectrum as spectrum
import audiopython.audiofile as audiofile
import audio_files
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal
import audiopython.basic_operations as basic_operations


f = audiofile.read("D:\\Recording\\Samples\\Iowa\\Cello.arco.mono.1644.1\\ff\\Cello.arco.ff.sulA.A4A5.mono.aif")
print(type(f))
audiofile.convert(f, "float32")
print(f.num_frames)
print(np.max(f.samples))
print(basic_operations.dbfs(f.samples[:, 243590-5:243590+5]))