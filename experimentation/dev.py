"""
File: dev.py

This file is for experimenting.
"""

import scipy.fft as sfft
import audiopython.sampler as sampler
import audiopython.spectrum as spectrum
import audiopython.audiofile as audiofile
import audiopython.analysis as analysis
import sample_processing.audio_files as audio_files
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal
import audiopython.basic_operations as basic_operations
import pedalboard as pb
import time
import librosa
import sample_processing.sc_data_generator as sc_data_generator
import os
import platform
import re
import fft

x = audiofile.read("D:\\Recording\\grains.wav")
X1 = fft.dft(x.samples[0, 8192:8192+512])
X2 = fft.fft(x.samples[0, 8192:8192+512], 512, 2)
X3 = sfft.fft(x.samples[0, 8192:8192+512])

print(X1[:5])
print(X2[:5])
print(X3[:5])