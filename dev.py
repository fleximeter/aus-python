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
import crepe

audio_a4 = None
audio_c4 = None

with pb.io.AudioFile("D:\\Recording\\Samples\\Iowa\\Viola.pizz.mono.2444.1\\Viola.pizz.sulG.mf.C4B4.mono.wav", 'r') as infile:
    sample_rate = infile.samplerate
    frames = infile.frames
    channels = infile.num_channels
    audio = infile.read(infile.frames)
    audio_c4 = audio[:, 39282:72576]
    audio_a4 = audio[:, 2563026:2585448]
    audio_c4 = audio_c4.reshape((audio_c4.size))
    audio_a4 = audio_a4.reshape((audio_a4.size))


white_noise = np.random.normal(0, 1, size=audio_c4.size)
x1 = time.time()

t, frequency, confidence, activation = crepe.predict(audio_c4, 44100, viterbi=True)
print(t)
print(frequency)
print(confidence)
print(activation)
x2 = time.time() - x1

print(x2, "seconds")

# audio_analysis = analysis.analyzer(audio_c4, 44100)
# print("C4")
# print(audio_analysis)

# audio_analysis = analysis.analyzer(audio_a4, 44100)
# print("A4")
# print(audio_analysis)

# print("Gaussian noise")
# audio_analysis = analysis.analyzer(white_noise, 44100)
# print(audio_analysis)

