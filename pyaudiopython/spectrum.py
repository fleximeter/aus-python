"""
File: spectrum.py
Author: Jeff Martin
Date: 2/11/23

This file contains functionality for spectral analysis.
"""

import numpy as np
import matplotlib.pyplot as plt


def fft_data_decompose(fft_data):
    """
    Decomposes FFT data from a Numpy array into arrays of amplitudes and phases.
    This function can handle Numpy arrays of any dimension.
    :param fft_data: The data from a FFT function
    :return: Two arrays: one for amplitudes and one for phases
    """
    amps = np.abs(fft_data)
    phases = np.angle(fft_data)
    return amps, phases


def fft_data_recompose(amps, phases):
    """
    Recomposes FFT data from arrays of amplitudes and phases
    This function can handle Numpy arrays of any dimension.
    :param amps: An array of amplitudes
    :param phases: An array of phases
    :return: An array of FFT data
    """
    real = np.cos(phases) * amps
    imag = np.sin(phases) * amps
    return real + (imag * 1j)
