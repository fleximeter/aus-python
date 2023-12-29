"""
A sample loader for SuperCollider

Date: 12/28/23
"""

import audiopython.audiofile as audiofile
import audiopython.basic_operations as basic_operations
import audiopython.sampler as sampler
import sc_data_generator
import os
import re

DIR = "D:\\Recording\\Samples\\Iowa\\Viola.pizz.mono.2444.1\\samples"

files = audiofile.find_files(DIR)
dynamics = {'pppp': -5, 'ppp': -4, 'pp': -3, 'p': -2, 'mp': -1, 'm': 0, 'mf': 1, 'f': 2, 'ff': 3, 'fff': 4, 'ffff': 5}
strings = {'C': 0, 'G': 1, 'D': 2, 'A': 3}
sc_samples = {
    "mf": {
        "C": {},
        "G": {},
        "D": {},
        "A": {}
    },
    "ff": {
        "C": {},
        "G": {},
        "D": {},
        "A": {}
    }
}

for file in files:
    filename = os.path.split(file)[1]
    filename = re.sub(r'(\.wav$)|(\.aif+$)', '', filename, re.IGNORECASE)
    filename_components = filename.split('.')
    audio = audiofile.read_with_pedalboard(file)
    sample = sampler.Sample(audio.samples, 44100, file)
    sample.frames = audio.samples.shape[-1]
    sample.duration = audio.duration
    sample.pitched = True
    sample.string_name = filename_components[4][3:]
    sample.string_id = strings[sample.string_name]
    sample.dynamic_name = filename_components[5]
    sample.dynamic_id = dynamics[sample.dynamic_name]
    sample.instrument_type = filename_components[2].lower()
    sample.midi = filename_components[1]
    sample_dict = {
        "midi": sample.midi,
        "duration": sample.duration,
        "frames": sample.frames,
        "pitched": sample.pitched,
        "dynamic_name": sample.dynamic_name,
        "dynamic_id": sample.dynamic_id,
        "instrument_type": sample.instrument_type,
        "path": sample.path,
        "string_name": sample.string_name,
        "string_id": sample.string_id
    }
    sc_samples[sample_dict["dynamic_name"]][sample_dict["string_name"]][str(sample_dict["midi"])] = sample_dict

with open("D:\\Recording\\viola.scd", "w") as outfile:
    outfile.write(sc_data_generator.make_sc_from_nested_objects(sc_samples))
