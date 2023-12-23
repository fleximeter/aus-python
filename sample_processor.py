"""
File: sample_processor.py
Author: Jeff Martin
Date: 12/22/23

This file loads all samples files within a directory and its subdirectories,
and processes them. It is useful for performing postprocessing after sample extraction,
for naming samples properly and for applying some filtering and tuning.
"""

import audiopython.analysis as analysis
import audiopython.basic_operations as basic_operations
import json
import numpy as np
import os
import pedalboard
import re
import scipy.signal


if __name__ == "__main__":
    print("Starting sample processor...")
    with open("process.viola.arco.mf.json", "r") as f:
        data = json.loads(f.read())
        for file in data:
            with pedalboard.io.AudioFile(file["file"], "r") as a:
                audio = a.read(a.frames)
                audio = scipy.signal.sosfilt(
                    scipy.signal.butter(12, 440 * 2 ** ((file["midi"] - 5 - 69) / 12), 'high', output='sos', fs=44100), 
                    audio
                    )
                midi_est = analysis.midi_estimation_from_pitch(
                    analysis.pitch_estimation(
                        basic_operations.mix_if_not_mono(audio), 
                        44100, 
                        440 * 2 ** ((file["midi"] - 4 - 69) / 12), 
                        440 * 2 ** ((file["midi"] + 4 - 69) / 12), 
                        0.5
                    ))
                if not np.isnan(midi_est) and not np.isinf(midi_est) and not np.isneginf(midi_est):
                    audio = basic_operations.midi_tuner(audio, midi_est, 1, 44100, file["midi"])
                new_filename = re.sub(r'\.[0-9]+\.wav$', '', os.path.split(file["file"])[-1])
                with pedalboard.io.AudioFile(os.path.join("D:\\Recording\\Samples\\Iowa\\Viola.arco.mono.2444.1\\samples", f"sample.{file['midi']}.{new_filename}.wav"), 'w', 44100, 1, 24) as outfile:
                    outfile.write(audio)

    print("Sample processor done.")
