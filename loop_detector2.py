import audiopython.sampler
import audiopython.wav
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
    audio = audiopython.wav.read_wav(f"{directory}\\{file}")
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
df.insert(0, "file_name")
for i in range(maxloops):
    df.insert(i+1, f"loop_{i+1}")
for loop in loops:
    df.loc[len(df.index)] = [loop] + [val for val in loops[loop]]

print(df)