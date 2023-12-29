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

x = ["apple", 5, {"able": 1, "baker": 2, "charlie": 3}, ["apple", "cat", {"able": "alpha", "baker": "beta"}]]
s = sc_data_generator.make_sc_from_nested_objects(x)
print(s)