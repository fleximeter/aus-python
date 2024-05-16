"""
File: sample_extractor_tuner.py
Author: Jeff Martin
Date: 12/22/23

This file loads all audio files with a directory and its subdirectories,
and extracts individual samples from them. It also tunes samples to the nearest MIDI note.
"""

import audiopython.analysis as analysis
import audiopython.audiofile as audiofile
import audiopython.basic_operations as basic_operations
import audiopython.sampler as sampler
import multiprocessing as mp
import numpy as np
import os
import platform
import re
import scipy.signal

# Directory roots. We automatically detect if we're on Windows or Mac.
WINROOT = "D:\\"
MACROOT = "/Volumes/AudioJeff"
PLATFORM = platform.platform()
ROOT = WINROOT
if re.search(r'macos', PLATFORM, re.IGNORECASE):
    ROOT = MACROOT

# This stuff needs to be set manually. Set the directory location and the sample dynamic level to use.
DIR = os.path.join(ROOT, "Recording", "Samples", "Iowa", "Xylophone.rosewood")
DYNAMIC = "ff"

# multiprocessing stuff
CPU_COUNT = mp.cpu_count()

# Basic audio stuff
PEAK_VAL = 0.25
SAMPLE_RATE = 44100
LOWCUT_FREQ = 55
LOWCUT = True
MIN_SAMPLE_LENGTH = 11000

# The filter we use to remove DC bias and any annoying low frequency stuff
filt = scipy.signal.butter(4, LOWCUT_FREQ, 'high', output='sos', fs=SAMPLE_RATE)


def extract_samples(audio_files, destination_directory):
    """
    Extracts samples from a list of provided audio files.
    :param audio_files: A list of audio file names
    :param destination_directory: The destination sample directory
    """
    for file in audio_files:
        short_name = re.sub(r'(\.wav$)|(\.aif+$)', '', os.path.split(file)[-1], re.IGNORECASE)
        
        # Read the audio file and force it to the right number of dimensions
        audio = audiofile.read(file)
        audio.samples = basic_operations.mix_if_not_mono(audio.samples, 2)
        audio.num_channels = 1
        
        # Perform preprocessing
        if LOWCUT:
            audio.samples = scipy.signal.sosfilt(filt, audio.samples)
        
        # Extract the samples. You may need to tweak some settings here to optimize sample extraction.
        amplitude_regions = sampler.identify_amplitude_regions(audio=audio, level_delimiter=-36, num_consecutive=MIN_SAMPLE_LENGTH)
        samples = sampler.extract_samples(audio=audio, amplitude_regions=amplitude_regions, pre_frames_to_include=500, 
                                          post_frames_to_include=11000, pre_envelope_frames=500, post_envelope_frames=500)
        
        # Perform postprocessing, including scaling dynamic level and tuning
        for i, sample in enumerate(samples):
            sample.samples = basic_operations.leak_dc_bias_averager(sample.samples)
            current_peak = np.max(np.abs(sample.samples))
            sample.samples *= PEAK_VAL / current_peak
            midi = analysis.midi_estimation_from_pitch(analysis.pitch_estimation(basic_operations.mix_if_not_mono(
                sample.samples
                ), 44100, 27.5, 5000, 0.5))
            if not np.isnan(midi) and not np.isinf(midi) and not np.isneginf(midi):
                sample.samples = basic_operations.midi_tuner(sample.samples, midi, 1, 44100)
                sample.num_frames = sample.samples.shape[-1]
                midi = int(np.round(midi))
            audiofile.write_with_pedalboard(sample, os.path.join(destination_directory, f"{short_name}.{i+1}.wav"))



if __name__ == "__main__":
    print("Starting sample extractor...")
    destination_directory = os.path.join(DIR, "samples")
    os.makedirs(destination_directory, 511, True)

    files = audiofile.find_files(DIR)
    files2 = []
    # A basic file filter. We exclude samples that have already been created, because
    # they have "sample." in the file name. We also are targeting samples of a specific
    # dynamic level here.
    for file in files:
        if re.search(DYNAMIC, file, re.IGNORECASE) and not re.search(r'sample\.', file, re.IGNORECASE):
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
