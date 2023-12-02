import scipy.fft
import audiopython.sampler as sampler
import audiopython.spectrum as spectrum
import audiopython.audiofile as audiofile
import audio_files
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal
import audiopython.basic_operations as basic_operations
import pedalboard as pb


#f = audiofile.read("D:\\Recording\\Samples\\Iowa\\Cello.arco.mono.1644.1\\ff\\Cello.arco.ff.sulA.A4A5.mono.aif")
#print(type(f))
#audiofile.convert(f, "float32")
#print(f.num_frames)
#print(np.max(f.samples))
#print(basic_operations.dbfs(f.samples[:, 243590-5:243590+5]))

audio = None

with pb.io.AudioFile("D:\\Recording\\ReaperProjects\\electronic_music_production\\final_project\\audio\\walk_sign_clinton1.wav", 'r') as infile:
    sample_rate = infile.samplerate
    frames = infile.frames
    channels = infile.num_channels
    audio = infile.read(infile.frames)
    audio_chunk = audio[:, 180000:190000]
    hpf = pb.HighpassFilter(200)
    audio_chunk = hpf(audio_chunk, sample_rate)
    audio_chunk = basic_operations.fade_in(audio_chunk, "hanning", 200)
    audio_chunk = basic_operations.fade_out(audio_chunk, "hanning", 600)
    audio_chunk = np.hstack((np.zeros((2, sample_rate)), audio_chunk, np.zeros((2, sample_rate))))
    with pb.io.AudioFile("D:\\Recording\\ReaperProjects\\electronic_music_production\\final_project\\audio\\walk_sign_word.wav", 'w', sample_rate, channels, 24) as out:
        out.write(audio_chunk)
