"""
File: dev.py

This file is for experimenting.
"""

import audiopython.spectrum as spectrum
import audiopython.audiofile as audiofile
import numpy as np
import scipy.fft as fft

x = audiofile.read("D:\\Recording\\grains.wav")
z = fft.rfft(x.samples[0, 16384:16384+4096])
spectrum.plot_spectrum(z, 44100, (0, 1000))
