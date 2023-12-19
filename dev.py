import scipy.fft
import audiopython.sampler as sampler
import audiopython.spectrum as spectrum
import audiopython.audiofile as audiofile
import audiopython.analysis as analysis
import audio_files
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal
import audiopython.basic_operations as basic_operations
import pedalboard as pb
import time

audio = None

with pb.io.AudioFile("D:\\Recording\\Samples\\Iowa\\Viola.pizz.mono.1644.1\\Viola.pizz.sulA.mf.A4B4.mono.aif", 'r') as infile:
    sample_rate = infile.samplerate
    frames = infile.frames
    channels = infile.num_channels
    audio = infile.read(infile.frames)[:, 129186:467424]
    audio = np.reshape(audio, (audio.shape[-1]))

white_noise = np.random.normal(0, 1, size=audio.size)
x1 = time.time()

audio_analysis = analysis.analyzer(audio, 44100)
print(audio_analysis)

audio_analysis = analysis.analyzer(white_noise, 44100)
print(audio_analysis)

x2 = time.time() - x1

print(x2, "seconds")