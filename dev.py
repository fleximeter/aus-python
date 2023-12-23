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
import librosa

audio_a4 = None
audio_c4 = None

with pb.io.AudioFile("D:\\Recording\\Samples\\Iowa\\Viola.pizz.mono.2444.1\\samples\\sample.48.Viola.pizz.sulC.ff.C3B3.mono.wav", 'r') as infile:
    sample_rate = infile.samplerate
    frames = infile.frames
    channels = infile.num_channels
    audio = infile.read(infile.frames)
    print(basic_operations.dbfs_audio(audio))
    audio = basic_operations.adjust_level(audio, -6)
    print(basic_operations.dbfs_audio(audio))
