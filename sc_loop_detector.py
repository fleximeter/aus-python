"""
File: sc_loop_detector2.py
Author: Jeff Martin
Date: 6/10/23

This file uses the sampler functionality from audiopython to detect loop points
in all files contained within a directory and its subfolders, and generates a
SuperCollider .scd file with data structures containing the audio file paths
and the loop points.
"""

import audiofile
import multiprocessing as mp
import sampler

PATH = "D:\\Recording\\Samples\\pianobook"
CPU_COUNT = mp.cpu_count()


def make_loops(audio_files, queue):
    """
    Makes loops from a list of audio files
    :param obj: The list of audio files
    """
    MIN_PERIODS = 2  # The minimum number of periods to allow for a set of loop points to be valid
    data = {}

    for file in audio_files:
        af = audiofile.read(file)
        num_periods = 20
        loop_points = []
        while len(loop_points) < 1 and num_periods >= MIN_PERIODS:
            loop_points = sampler.detect_loop_points(af, num_periods=num_periods, maximum_amplitude_variance=0.1)
            num_periods -= 2
        data[file] = loop_points

    queue.put(data)


if __name__ == "__main__":
    audio_files = audiofile.find_files(PATH)
    loop_data = {}

    # Distribute the audio files among the different processes. This is a good way to do it
    # because we assume that some files will be harder to process, and those will probably
    # be adjacent to each other in the folder, so we don't want to take blocks of files;
    # we want to distribute them individually.
    audio_file_chunks = [[] for i in range(CPU_COUNT)]
    for i, file in enumerate(audio_files):
        audio_file_chunks[i % CPU_COUNT].append(file)
    

    # Start the processes
    processes = []
    queues = [mp.Queue() for i in range(CPU_COUNT)]
    for i in range(CPU_COUNT):
        processes.append(mp.Process(target=make_loops, args=(audio_file_chunks[i], queues[i])))
        processes[-1].start()
    
    # Collect the results
    for i in range(CPU_COUNT):
        data = queues[i].get()
        for key, val in data.items():
            loop_data[key] = val

    # Collect the processes
    for i in range(CPU_COUNT):
        processes[i].join()
        
    for item in loop_data:
        print(item, loop_data[item])
