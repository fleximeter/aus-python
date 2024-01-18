"""
File: dev.py

This file is for experimenting.
"""

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
import sc_data_generator
import os
import platform
import re

print(basic_operations.midicps(65))
print(basic_operations.midicps(69))
print(basic_operations.midicps(72))
print(basic_operations.midicps(76))

x = audiofile.read("D:\\NoiseMaker.wav")
x.num_channels = 1
x.samples = basic_operations.force_equal_energy(x.samples, -12, 8192)
x.samples = basic_operations.fade_in(x.samples, duration=8192)
x.samples = basic_operations.fade_out(x.samples, duration=8192)
audiofile.write_with_pedalboard(x, "D:\\NoiseMaker1.wav")
