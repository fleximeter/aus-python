"""
File: loop_detector.py
Author: Jeff Martin
Date: 2/18/23

This file uses the sampler functionality from audiopython to detect loop points
in all files contained within a directory.
"""

import sampler
import wav
import os

dir = "D:\\Recording\\ReaperProjects\\trombone_samples\\samples\\batch_norm_m"
files = os.listdir(dir)

# This contains the detected loops. Keys are file names and values are the loop point tuple.
loops = {}

for file in files:
    print(file)
    num_points = 100
    audio = wav.read_wav(f"{dir}\\{file}")
    points = sampler.detect_loop_points(audio, 0, num_points)

    # if no loop points were discovered, decrease the number of periods
    # and try again
    while not points and num_points > 50:
        num_points -= 1
        points = sampler.detect_loop_points(audio, 0, num_points)
    if points:
        loops[file] = points[0]

print(loops)
