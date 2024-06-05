"""
File: dev.py

This file is for experimenting.
"""

import audiopython.spectrum as spectrum
import audiopython.audiofile as audiofile
import numpy as np
import scipy.fft as fft
import datetime

import temp

temp.say_hello_to("Jeff")
print(temp.integrate_f(52432, 32, 59024 ))


# x = audiofile.read("D:\\Recording\\grains.wav")
# z = fft.rfft(x.samples[0, 16384:16384+4096])
# spectrum.plot_spectrum(z, 44100, (0, 1000))
