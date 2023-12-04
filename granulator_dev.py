import audiopython.audiofile as audiofile
import audiopython.granulator as granulator
import audiopython.basic_operations as basic_operations
import pedalboard as pb
import numpy as np
import random

random.seed()

DIR = "D:\\Recording\\Samples\\BBC_non_commercial\\Africa 2 - The Natural World"

files = audiofile.find_files(DIR)
audio = []

for file in files:
    with pb.io.AudioFile(file, 'r') as infile:
        audio_data = infile.read(infile.frames)
        audio_data = basic_operations.mix_if_not_mono(audio_data)
        audio.append(audio_data)

NUM_GRAINS = 1000
GRAIN_SIZE_MIN = 100
GRAIN_SIZE_MAX = 10000

grains = []

for i in range(NUM_GRAINS):
    grain_size = random.randint(GRAIN_SIZE_MIN, GRAIN_SIZE_MAX)
    j = random.randint(0, len(audio)-1)
    start_frame = random.randint(0, audio[j].shape[-1] - grain_size)
    grain = granulator.extract_grain(audio[j], start_frame, grain_size, max_window_size=GRAIN_SIZE_MIN)
    grains.append(grain)

granulator.scale_grain_peaks(grains)
final_audio = granulator.merge_grains(grains, GRAIN_SIZE_MIN // 4)
final_audio = pb.LowpassFilter(4000)(final_audio, 44100)

with pb.io.AudioFile("D:\\Recording\\grains.wav", 'w', 44100, 1, 24) as out:
    out.write(final_audio)
