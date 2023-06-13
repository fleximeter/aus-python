"""
File: loop_extractor.py
Author: Jeff Martin
Date: 6/13/23

This file loads all audio files with a directory and its subdirectories,
and extracts individual samples from them.
"""

import audiopython.audiofile
import audiopython.sampler
import multiprocessing as mp
import os

DIRECTORY = "D:\\Recording\\Samples\\Iowa\\Violin.arco.mono.1644.1"
CPU_COUNT = mp.cpu_count()


def extract_samples(audio_files, destination_directory):
    """
    Extracts samples from a list of provided audio files.
    :param audio_files: A list of audio file names
    :param destination_directory: The destination sample directory
    """
    for file in audio_files:
        short_name = os.path.split(file)[-1]
        audio = audiopython.audiofile.read(file)
        amplitude_regions = audiopython.sampler.identify_amplitude_regions(audio, 0.0000001, num_consecutive=10000)
        samples = audiopython.sampler.extract_samples(audio, amplitude_regions, 500, 500, 
                                                    pre_envelope_frames=500, post_envelope_frames=500)
        for i, sample in enumerate(samples):
            audiopython.audiofile.write_wav(sample, os.path.join(destination_directory, f"sample_{short_name}_{i}.wav"))


if __name__ == "__main__":
    print("Starting sample extractor...")
    destination_directory = os.path.join(DIRECTORY, "samples")
    os.makedirs(destination_directory, 511, True)

    files = audiopython.audiofile.find_files(DIRECTORY)

    # Distribute the audio files among the different processes. This is a good way to do it
    # because we assume that some files will be harder to process, and those will probably
    # be adjacent to each other in the folder, so we don't want to take blocks of files;
    # we want to distribute them individually.
    file_groups = [[] for i in range(CPU_COUNT)]
    for i, file in enumerate(files):
        file_groups[i % CPU_COUNT].append(file)

    # Start the processes
    processes = []
    for i in range(CPU_COUNT):
        processes.append(mp.Process(target=extract_samples, args=(file_groups[i], destination_directory)))
        processes[-1].start()
    
    # Collect the processes
    for i in range(CPU_COUNT):
        processes[i].join()

    print("Sample extractor done.")
