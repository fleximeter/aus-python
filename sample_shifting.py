"""
File: sample_shifting.py

An experimentation with shifting samples and STFT frames in time
"""

import audiopython.audiofile as audiofile
import audiopython.operations as operations
import numpy as np
import scipy.signal as signal

if __name__ == "__main__":
    FILE = "D:\\Recording\\Samples\\freesound\\creative_commons_0\\wind_chimes\\eq\\217800__minian89__wind_chimes_eq.wav"
    FFT_SIZE = 512
    audio = audiofile.read(FILE)
    lpf = signal.butter(2, 10000, "low", output="sos", fs=audio.sample_rate)
    # new_samples1 = signal.sosfilt(lpf, exchanger(audio.samples, 8))
    STFT = signal.ShortTimeFFT(signal.windows.hann(FFT_SIZE), FFT_SIZE // 2, audio.sample_rate)
    stft_data = STFT.stft(audio.samples)
    stft_data = operations.stochastic_exchanger(stft_data, 48)
    out1 = audiofile.AudioFile.copy_header(audio)
    out1.samples = np.array(STFT.istft(stft_data))
    audiofile.write_with_pedalboard(out1, "D:\\Recording\\Samples\\freesound\\creative_commons_0\\wind_chimes\\eq\\temp1.wav")
