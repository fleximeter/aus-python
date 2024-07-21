aus.plot
##############################

.. py:function:: plot_audio(audio: np.ndarray)

    Visualizes audio using matplotlib.
    :param np.ndarray audio: A numpy array of audio samples

.. py:function:: plot_spectrogram(audio: np.ndarray, sample_rate: int, window_size: int = 1024)
    
    Plots FFT data.
    
    :param np.ndarray audio: A 1D array of audio samples
    :param int sample_rate: The sample rate of the audio
    :param int window_size: The window size that will be analyzed
    
.. py:function:: plot_spectrum(spectrum, sample_rate, frequency_range=None)
    
    Plots FFT data. The FFT data should be in original imaginary form.
    It will be converted to a normalized power spectrum in decibels.
    
    :param np.ndarray spectrum: An imaginary spectrum to plot
    :param int sample_rate: The sample rate (for determining frequencies)
    :param frequency_range: If not ``None``, only the frequencies within this range will be plotted.
