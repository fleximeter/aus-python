"""
A pedalboard-based file converter

Date: 12/19/23
"""

import audiopython.basic_operations as basic_operations
import os
import multiprocessing as mp
import pathlib
import pedalboard as pb
import queue
import re
import scipy.signal
from audiopython import audiofile

WINROOT = "D:"
MACROOT = "/Volumes/AudioJeff"
ROOT = WINROOT
IN_DIR = f"{ROOT}/Recording/Samples/Iowa/TenorTrombone"
OUT_DIR = f"{ROOT}/Recording/Samples/Iowa/TenorTrombone/process"
LOWCUT_FREQ = 20
OUT_SAMPLE_RATE = 44100
OUT_BIT_DEPTH = 24
NEW_EXTENSION = "wav"

pathlib.Path(OUT_DIR).mkdir(parents=True, exist_ok=True)
audio_files = audiofile.find_files(IN_DIR)
subber = re.compile(r'(\.aif+$)|(\.wav$)')
filt = scipy.signal.butter(8, LOWCUT_FREQ, 'high', output='sos', fs=OUT_SAMPLE_RATE)


def file_converter_resample(files):
    for file in files:
        filename = os.path.split(file)[1]
        filename = subber.sub('', filename)
        filename = f"{filename}.{NEW_EXTENSION}"
        with pb.io.AudioFile(file, 'r').resampled_to(OUT_SAMPLE_RATE) as infile:
            with pb.io.AudioFile(os.path.join(OUT_DIR, filename), 'w', OUT_SAMPLE_RATE, infile.num_channels, OUT_BIT_DEPTH) as outfile:
                while infile.tell() < infile.frames:
                    outfile.write(infile.read(1024))


def file_converter_resample_filter(files):
    for file in files:
        filename = os.path.split(file)[1]
        filename = subber.sub('', filename)
        filename = f"{filename}.{NEW_EXTENSION}"
        with pb.io.AudioFile(file, 'r').resampled_to(OUT_SAMPLE_RATE) as infile:
            audio = infile.read(infile.frames)
            audio = scipy.signal.sosfilt(filt, audio)
            with pb.io.AudioFile(os.path.join(OUT_DIR, filename), 'w', OUT_SAMPLE_RATE, infile.num_channels, OUT_BIT_DEPTH) as outfile:
                outfile.write(audio)


def file_converter_filter(files):
    for file in files:
        filename = os.path.split(file)[1]
        filename = subber.sub('', filename)
        filename = f"{filename}.{NEW_EXTENSION}"
        with pb.io.AudioFile(file, 'r') as infile:
            audio = infile.read(infile.frames)
            audio = basic_operations.mix_if_not_mono(audio)
            audio = scipy.signal.sosfilt(filt, audio)
            with pb.io.AudioFile(os.path.join(OUT_DIR, filename), 'w', OUT_SAMPLE_RATE, 1, OUT_BIT_DEPTH) as outfile:
                outfile.write(audio)


if __name__ == "__main__":
    print("Converting...")
    num_processes = mp.cpu_count()
    num_files_per_process = len(audio_files) // num_processes + 1
    processes = [mp.Process(target=file_converter_filter, args=(audio_files[num_files_per_process * i:num_files_per_process * (i + 1)],)) for i in range(num_processes)]
    for p in processes:
        p.start()
    for p in processes:
        p.join()
    print("Done")
