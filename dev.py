import numpy as np
from scipy.io.wavfile import read
import sampler
import wav

file_name = "D:\\Recording\\ReaperProjects\\trombone_samples\\samples\\trombone_sample_mute_9-19-22_a45_f.wav"
file_name1 = "D:\\Recording\\Samples\\pianobook\\YamahaC7\\YamahaC7\\Samples\\A#5_T1B.wav"
file_name2 = "D:\\Desktop\\sample24.wav"
file_name3 = "D:\\Desktop\\sample32.wav"

b_rate, b = read(file_name3)
print(f"Sample rate: {b_rate}, number of frames: {len(b)}")
a = wav.read_wav(file_name3)

print(len(b), a.num_frames)
print(a.bits_per_sample)

for i in range(100):
    if b[i, 0] == a.samples[0, i]:
        print(f"Match {i}")
    else:
        print(f"No match for sample index {i}: {b[i]} {a.samples[0, i]}")
# scaler, b_scaled = wav.scale_wav(b)

# regions = sampler.identify_amplitude_regions(b_scaled, 0.001, 1000, 0)
# print(regions)

# with open(file_name1, "rb") as audio_file:
#     num_bytes = 1000
#     block_size = 3
#     offset = 44
#     offset2 = 36
#     header = audio_file.read(offset)
#     junk1 = audio_file.read(offset2)
#     data = audio_file.read(421715 * 3)
#     junk2 = audio_file.read()
#     print(header)
#     print(junk1)
    # print(len(data) // block_size)


    # for i in range(0, num_bytes):
    #     current = int.from_bytes(data[i:i+block_size], byteorder="little", signed=True)
    #     if current == b[0] // 256:
    #         print(f"Match: {i}")        

    # for i in range(0, len(data), block_size):
    #     j = i // block_size

    #     current_block = data[i:i+block_size]
    #     current_b = b[j]
    #     current = int.from_bytes(current_block, byteorder="little", signed=True)
        
    #     if current == current_b // 256:
    #         # print(f"Match: {j}")
    #         pass
    #     else:
    #         print(f"{j} Found bytes {current_block}, converted as {current}, scipy has {current_b}")

    # print(f"The length of junk1 is {len(junk1)} and the length of junk2 is {len(junk2)}")
    # print(junk1)
    # print(junk2)

# print(int(b'a'))