import audiopython.audiofile as audiofile
import audiopython.granulator as granulator
import audiopython.basic_operations as basic_operations
import pedalboard as pb
import numpy as np
import random

random.seed()

np.seterr(divide="ignore")

DIR = "D:\\Recording\\Samples"
DIR2 = "C:\\Users\\jeffr\\Recording\\Samples"

SUBDIR1 = "Iowa\\Viola.pizz.mono.2496"
SUBDIR2 = "Iowa\\Viola.temp"
DIR_OUT_1 = "D:\\Recording"
DIR_OUT_2 = "C:\\Users\\jeffr\\Recording"

files = audiofile.find_files(f"{DIR}\\{SUBDIR1}")
audio = []

for file in files:
    with pb.io.AudioFile(file, 'r').resampled_to(44100) as infile:
        audio_data = infile.read(infile.frames)
        audio_data = basic_operations.mix_if_not_mono(audio_data)
        audio.append(audio_data)

NUM_GRAINS = 50000
GRAIN_SIZE_MIN = 1000
GRAIN_SIZE_MAX = 10000

grains = []

for i in range(NUM_GRAINS):
    grain_size = random.randint(GRAIN_SIZE_MIN, GRAIN_SIZE_MAX)
    j = random.randint(0, len(audio)-1)
    start_frame = random.randint(0, audio[j].shape[-1] - grain_size)
    grain = granulator.extract_grain(audio[j], start_frame, grain_size, max_window_size=GRAIN_SIZE_MIN)
    grains.append(grain)

granulator.scale_grain_peaks(grains)
max_dbfs = granulator.find_max_grain_dbfs(grains)
grains2 = []
for grain in grains:
    if basic_operations.dbfs_audio(grain) / max_dbfs < 2:
        grains2.append(grain)

final_audio = granulator.merge_grains(grains2, GRAIN_SIZE_MIN // 2)
final_audio = pb.LowpassFilter(4000)(final_audio, 44100)
final_audio = pb.Compressor(-12, 4)(final_audio, 44100)

with pb.io.AudioFile(f"{DIR_OUT_1}\\grains.wav", 'w', 44100, 1, 24) as out:
    out.write(final_audio)
