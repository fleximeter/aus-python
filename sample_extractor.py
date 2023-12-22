"""
File: loop_extractor.py
Author: Jeff Martin
Date: 6/13/23

This file loads all audio files with a directory and its subdirectories,
and extracts individual samples from them.
"""

import audio_files
import audiopython.analysis as analysis
import audiopython.audiofile as audiofile
import audiopython.basic_operations as basic_operations
import audiopython.sampler as sampler
import multiprocessing as mp
import numpy as np
import os
import re
import scipy.signal

CPU_COUNT = mp.cpu_count()
SAMPLE_RATE = 44100
LOWCUT_FREQ = 55
LOWCUT = True
filt = scipy.signal.butter(4, LOWCUT_FREQ, 'high', output='sos', fs=SAMPLE_RATE)


def extract_samples(audio_files, destination_directory):
    """
    Extracts samples from a list of provided audio files.
    :param audio_files: A list of audio file names
    :param destination_directory: The destination sample directory
    """
    for file in audio_files:
        short_name = re.sub(r'(\.wav$)|(\.aif+$)', '', os.path.split(file)[-1], re.IGNORECASE)
        print(short_name)
        audio = audiofile.read(file)
        if LOWCUT:
            audio.samples = scipy.signal.sosfilt(filt, audio.samples)
        audio.samples = basic_operations.leak_dc_bias(audio.samples)
        amplitude_regions = sampler.identify_amplitude_regions(audio, 0.02, num_consecutive=22000)
        samples = sampler.extract_samples(audio, amplitude_regions, 500, 10000, 
                                                    pre_envelope_frames=500, post_envelope_frames=500)
        for i, sample in enumerate(samples):
            midi = analysis.midi_estimation_from_pitch(analysis.pitch_estimation(basic_operations.mix_if_not_mono(sample.samples), 44100, 27.5, 3520))
            if not np.isnan(midi):
                sample.samples = basic_operations.midi_tuner(sample.samples, midi, 1, 44100)
                sample.num_frames = sample.samples.shape[-1]
                midi = int(np.round(midi))
            audiofile.write_wav(sample, os.path.join(destination_directory, f"sample.{midi}.{short_name}.wav"))


if __name__ == "__main__":
    print("Starting sample extractor...")
    destination_directory = os.path.join(audio_files._VIOLA_SAMPLES_DIR, "samples")
    os.makedirs(destination_directory, 511, True)

    files = audiofile.find_files(audio_files._VIOLA_SAMPLES_DIR)
    files2 = []
    for file in files:
        if re.search(r'ff', file, re.IGNORECASE):
            files2.append(file)
    
    # Distribute the audio files among the different processes. This is a good way to do it
    # because we assume that some files will be harder to process, and those will probably
    # be adjacent to each other in the folder, so we don't want to take blocks of files;
    # we want to distribute them individually.
    file_groups = [[] for i in range(CPU_COUNT)]
    for i, file in enumerate(files2):
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
