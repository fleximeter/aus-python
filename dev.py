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

audiofile.read_wav("D:\\temp.wav")