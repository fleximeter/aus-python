aus.spectrum
##############################

.. py:function:: fft_data_decompose(fft_data: np.ndarray)

    Decomposes FFT data from a Numpy array into arrays of amplitudes and phases.
    This function can handle Numpy arrays of any dimension.

    :param np.ndarray fft_data: The data from a FFT function
    :return: Two arrays: one for amplitudes and one for phases
    :rtype: np.ndarray, np.ndarray

.. py:function:: fft_data_recompose(amps: np.ndarray, phases: np.ndarray)

    Recomposes FFT data from arrays of amplitudes and phases
    This function can handle Numpy arrays of any dimension.

    :param np.ndarray amps: An array of amplitudes
    :param np.ndarray phases: An array of phases
    :return: An array of FFT data
    :rtype: np.ndarray
