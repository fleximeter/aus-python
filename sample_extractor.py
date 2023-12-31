"""
File: sample_extractor.py
Author: Jeff Martin
Date: 6/13/23

This file loads all audio files with a directory and its subdirectories,
and extracts individual samples from them.
"""

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
PEAK_VAL = 0.25
LOWCUT_FREQ = 32
LOWCUT = True
LEVEL = -6
filt = scipy.signal.butter(4, LOWCUT_FREQ, 'high', output='sos', fs=SAMPLE_RATE)


def extract_samples(audio_files, destination_directory):
    """
    Extracts samples from a list of provided audio files.
    :param audio_files: A list of audio file names
    :param destination_directory: The destination sample directory
    """
    for file in audio_files:
        short_name = re.sub(r'(\.wav$)|(\.aif+$)', '', os.path.split(file)[-1], re.IGNORECASE)
        
        # Read the audio file
        audio = audiofile.read_with_pedalboard(file)
        audio.samples = basic_operations.mix_if_not_mono(audio.samples)
        audio.samples = np.reshape(audio.samples, (1, audio.samples.shape[0]))
        audio.bits_per_sample = 16
        audio.num_channels = 1
        
        # Perform preprocessing
        if LOWCUT:
            audio.samples = scipy.signal.sosfilt(filt, audio.samples)
        audio.samples = basic_operations.leak_dc_bias(audio.samples)

        # Extract the samples. You may need to tweak some settings here to optimize sample extraction.
        amplitude_regions = sampler.identify_amplitude_regions(audio, 0.002, num_consecutive=22000)
        samples = sampler.extract_samples(audio, amplitude_regions, 500, 30000, 
                                                    pre_envelope_frames=500, post_envelope_frames=500)
        
        # Perform postprocessing, including scaling the audio
        for i, sample in enumerate(samples):
            sample.samples = basic_operations.leak_dc_bias(sample.samples)
            current_peak = np.max(np.abs(sample.samples))
            sample.samples *= PEAK_VAL / current_peak
            audiofile.write_with_pedalboard(sample, os.path.join(destination_directory, f"{short_name}.{i+1}.wav"))


if __name__ == "__main__":
    print("Starting sample extractor...")
    DIR = "D:\\Recording\\Samples\\Iowa\\Guitar.mono.2444.1"
    destination_directory = os.path.join(DIR, "temp")
    os.makedirs(destination_directory, 511, True)

    files = audiofile.find_files(DIR)
    # files = audio_files.bass_trombone_samples
    files2 = []
    # A basic file filter. We exclude samples that have already been created, because
    # they have "sample." in the file name. We also are targeting samples of a specific
    # dynamic level here.
    for file in files:
        if re.search(r'ff', file, re.IGNORECASE) and not re.search(r'sample\.', file, re.IGNORECASE):
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
