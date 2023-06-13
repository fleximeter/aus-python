"""
File: loop_detector2.py
Author: Jeff Martin
Date: 2/19/23

This file uses the sampler functionality from audiopython to detect loop points
in all files contained within a directory.
"""

import audiopython.sampler
import audiopython.audiofile
import os
import pandas

print("Loop Detector")
directory = input("Enter the folder to scan: ")
num_periods = int(input("Enter the number of wave periods for the desired loop length: "))

print("Detecting loops...")

files = os.listdir(directory)
loops = {}

maxloops = 0
for file in files:
    num_periods1 = num_periods
    audio = audiopython.audiofile.read_wav(f"{directory}\\{file}")
    points = audiopython.sampler.detect_loop_points(audio, 0, num_periods1)

    # if no loop points were discovered, decrease the number of periods
    # and try again
    while not points and num_periods1 > 50:
        num_periods1 -= 1
        points = audiopython.sampler.detect_loop_points(audio, 0, num_periods1)
    if points:
        loops[file] = points
        if len(points) > maxloops:
            maxloops = len(points)

df = pandas.DataFrame()
df.insert(0, "file_name", [])
for i in range(maxloops):
    df.insert(2 * i + 1, f"loop_{i+1}_start", [])
    df.insert(2 * i + 2, f"loop_{i+1}_end", [])

for loop in loops:
    looplist = [loop]
    for val in loops[loop]:
        looplist.append(val[0])
        looplist.append(val[1])
    for i in range(len(looplist), maxloops * 2 + 1):
        looplist.append(None)
    df.loc[len(df.index)] = looplist

df.to_excel("loops.xlsx")

print("Done. Output to loops.xlsx")
