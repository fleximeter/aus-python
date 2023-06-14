import scipy.fft
import audiopython.sampler as sampler
import audiopython.spectrum as spectrum
import audiopython.audiofile as audiofile
import numpy as np
import matplotlib.pyplot as plt

file_name = "D:\\Recording\\Samples\\Iowa\\Violin.arco.mono.1644.1\\Violin.arco.mf.sulE.C7E7.mono.aif"

# with open(file_name, "rb") as file:
#     a = file.read(12)
#     b = file.read(26)
#     c = file.read(28)
#     d = file.read(20)
#     e = file.read(14)
#     f = file.read(20)
    
    
#     print(a)
#     print(b)
#     print(c)
#     print(d)
#     print(e)
#     print(f)
    
a = audiofile.read(file_name)
print(a.num_frames)
print(type(a.samples))

