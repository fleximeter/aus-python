"""
A pedalboard-based file converter

Date: 12/19/23
"""

import os
import multiprocessing as mp
import pathlib
import pedalboard as pb
import queue
import re
from audiopython import audiofile


IN_DIR = "D:\\Recording\\Samples\\Iowa\\Viola.arco.mono.2496"
OUT_DIR = "D:\\Recording\\Samples\\Iowa\\Viola.arco.mono.2444.1"
NEW_SAMPLE_RATE = 44100
NEW_BIT_DEPTH = 24
NEW_EXTENSION = "wav"

pathlib.Path(OUT_DIR).mkdir(parents=True, exist_ok=True)
audio_files = audiofile.find_files(IN_DIR)
subber = re.compile(r'(\.aif+$)|(\.wav$)')


def file_converter(files):
    for file in files:
        filename = os.path.split(file)[1]
        filename = subber.sub('', filename)
        filename = f"{filename}.{NEW_EXTENSION}"
        with pb.io.AudioFile(file, 'r').resampled_to(NEW_SAMPLE_RATE) as infile:
            with pb.io.AudioFile(os.path.join(OUT_DIR, filename), 'w', NEW_SAMPLE_RATE, infile.num_channels, NEW_BIT_DEPTH) as outfile:
                while infile.tell() < infile.frames:
                    outfile.write(infile.read(1024))


if __name__ == "__main__":
    print("Converting...")
    num_processes = mp.cpu_count()
    num_files_per_process = len(audio_files) // num_processes + 1
    processes = [mp.Process(target=file_converter, args=(audio_files[num_files_per_process * i:num_files_per_process * (i + 1)],)) for i in range(num_processes)]
    for p in processes:
        p.start()
    for p in processes:
        p.join()
    print("Done")
