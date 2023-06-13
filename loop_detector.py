"""
File: loop_detector.py
Author: Jeff Martin
Date: 2/18/23

This file uses the sampler functionality from audiopython to detect loop points
in all files contained within a directory.
"""

import audiopython.sampler
import audiopython.audiofile
import os

# set the directory here, and the number of periods for the loop length you want
directory = "D:\\Recording\\ReaperProjects\\trombone_samples\\samples\\batch_norm_m"
num_periods = 100

# you don't need to change anything below here
files = os.listdir(directory)

# This contains the detected loops. Keys are file names and values are the loop point tuple.
loops = {}

for file in files:
    # print(file)
    num_periods1 = num_periods
    audio = audiopython.audiofile.read_wav(f"{directory}\\{file}")
    points = audiopython.sampler.detect_loop_points(audio, 0, num_periods1)

    # if no loop points were discovered, decrease the number of periods
    # and try again
    while not points and num_periods1 > 50:
        num_periods1 -= 1
        points = audiopython.sampler.detect_loop_points(audio, 0, num_periods1)
    if points:
        loops[file] = points[0]

for loop in loops:
    print(loop, loops[loop])
