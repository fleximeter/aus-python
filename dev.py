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


audio = None

with pb.io.AudioFile("D:\\Recording\\Samples\\Iowa\\Viola.pizz.mono.1644.1\\Viola.pizz.sulA.mf.A4B4.mono.aif", 'r') as infile:
    sample_rate = infile.samplerate
    frames = infile.frames
    channels = infile.num_channels
    audio = infile.read(infile.frames)[:, 129186:467424]
    audio = np.reshape(audio, (audio.shape[-1]))

spec = scipy.fft.rfft(audio)
mag, phase = spectrum.fft_data_decompose(spec)
freqs = scipy.fft.rfftfreq(audio.shape[-1], 1/44100)

print(freqs)
print(mag)

slope, yint = analysis.spectral_slope(mag, freqs)
print(slope)
print(yint)