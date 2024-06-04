"""
File: sample_shifting.py

An experimentation with shifting samples and STFT frames in time
"""

import audiopython.audiofile as audiofile
import audiopython.basic_operations as basic_operations
import numpy as np
import scipy.signal as signal
import random

_rng = random.Random()


def exchanger(data: np.ndarray, hop: int):
    """
    Exchanges samples in an audio file or STFT frames in a spectrum. Each sample (or STFT frame) 
    is swapped with the sample (or STFT frame) *hop* steps ahead or *hop* steps behind. If audio
    is being processed, it should be in the shape (channels, samples). If STFT data is being
    processed, it should be in the shape (channels, frames, bins).
    :param data: The audio (or spectrum) to process
    :param hop: The hop size
    :return: The exchanged audio (or spectrum)
    """
    new_data = np.empty(data.shape, dtype=data.dtype)
    for i in range(data.shape[0]):
        for j in range(0, data.shape[1] - data.shape[1] % (hop * 2), hop * 2):
            for k in range(j, j+hop):
                new_data[i, k] = data[i, k+hop]
                new_data[i, k+hop] = data[i, k]
    return new_data


def stochastic_exchanger(data: np.ndarray, max_hop: int):
    """
    Stochastically exchanges samples in an audio file or STFT frames in a spectrum. Each sample 
    (or STFT frame) is swapped with the sample (or STFT frame) up to *hop* steps ahead or *hop* 
    steps behind. If audio is being processed, it should be in the shape (channels, samples). 
    If STFT data is being processed, it should be in the shape (channels, frames, bins).
    :param data: The audio (or spectrum) to process
    :param hop: The hop size
    :return: The exchanged audio (or spectrum)
    """
    new_data = np.empty(data.shape, dtype=data.dtype)

    for i in range(data.shape[0]):
        future_indices = set()
        past_indices = set()
        idx = 0
        while len(future_indices) + len(past_indices) < data.shape[1] and idx < data.shape[1]:
            # We can only perform a swap if this index has not been swapped yet
            if idx not in future_indices:
                # Get all possible future indices we might be able to swap with
                possible_indices = {z for z in range(idx, min(idx + max_hop, data.shape[1]))}
                possible_indices = possible_indices - future_indices

                # Randomly choose which index to swap with, and perform the swap
                swap_idx = _rng.choice(tuple(possible_indices))
                new_data[i, idx] = data[i, swap_idx]
                new_data[i, swap_idx] = data[i, idx]
                # print(f"Swap {idx} {swap_idx}")

                # Update the future and past indices
                future_indices.add(swap_idx)
                past_indices.add(idx)
                future_indices -= past_indices
            
            idx += 1

    return new_data


FILE = "D:\\Recording\\Samples\\freesound\\creative_commons_0\\wind_chimes\\eq\\217800__minian89__wind_chimes_eq.wav"
FFT_SIZE = 1024
audio = audiofile.read(FILE)
lpf = signal.butter(2, 10000, "low", output="sos", fs=audio.sample_rate)
# new_samples1 = signal.sosfilt(lpf, exchanger(audio.samples, 8))
STFT = signal.ShortTimeFFT(signal.windows.hann(FFT_SIZE), FFT_SIZE // 2, audio.sample_rate)
stft_data = STFT.stft(audio.samples)
stft_data = stochastic_exchanger(stft_data, 16)
out1 = audiofile.AudioFile.copy_header(audio)
out1.samples = np.array(STFT.istft(stft_data))
audiofile.write_with_pedalboard(out1, "D:\\Recording\\Samples\\freesound\\creative_commons_0\\wind_chimes\\eq\\temp1.wav")
