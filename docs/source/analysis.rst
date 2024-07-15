audiopython.analysis
##############################

Audio analysis tools developed from Eyben, "Real-Time Speech and Music Classification."
These tools expect audio as a 1D array of samples. The ``analyzer`` function runs all of the spectral
analysis tools, so it is more convenient than trying to run all of those tools individually.

.. py:function:: analyzer(audio: np.ndarray, sample_rate: int)

    Runs a suite of analysis tools on a provided NumPy array of audio samples

    :param np.ndarray audio: A 1D NumPy array of audio samples
    :param int sample_rate: The sample rate of the audio
    :return: A dictionary with the analysis results
    :rtype: dict

.. py:function:: energy(audio: np.ndarray)

    Extracts the RMS energy of the signal. Reference: Eyben, pp. 21-22.

    :param np.ndarray audio: A NumPy array of audio samples
    :return: The RMS energy of the signal

.. py:function:: spectral_centroid(magnitude_spectrum: np.ndarray, magnitude_freqs: np.ndarray, magnitude_spectrum_sum)
    
    Calculates the spectral centroid from provided magnitude spectrum. Reference: Eyben, pp. 39-40.

    :param np.ndarray magnitude_spectrum: The magnitude spectrum
    :param np.ndarray magnitude_freqs: The magnitude frequencies
    :param magnitude_spectrum_sum: The sum of the magnitude spectrum
    :return: The spectral centroid
    :rtype: float

.. py:function:: spectral_entropy(spectrum_pmf: np.ndarray)

    Calculates the spectral entropy from provided power spectrum. Reference: Eyben, pp. 23, 40, 41.

    :param np.ndarray spectrum_pmf: The spectrum power mass function PMF
    :return: The spectral entropy
    :rtype: float

.. py:function:: spectral_flatness(magnitude_spectrum: np.ndarray, magnitude_spectrum_sum)
    
    Calculates the spectral flatness from provided magnitude spectrum. References: Eyben, p. 39, https://en.wikipedia.org/wiki/Spectral_flatness.
    
    :param np.ndarray magnitude_spectrum: The magnitude spectrum
    :param magnitude_spectrum_sum: The sum of the magnitude spectrum
    :return: The spectral flatness, in dBFS
    :rtype: float

.. py:function:: spectral_kurtosis(spectrum_pmf: np.ndarray, magnitude_freqs: np.ndarray, spectral_centroid: float, spectral_variance: float)

    Calculates the spectral kurtosis. Reference: Eyben, pp. 23, 39-40.

    :param np.ndarray spectrum_pmf: The spectrum power mass function PMF
    :param np.ndarray magnitude_freqs: The magnitude frequencies
    :param float spectral_centroid: The spectral centroid
    :param float spectral_variance: The spectral variance
    :return: The spectral kurtosis
    :rtype: float
     
.. py:function:: spectral_roll_off_point(power_spectrum: np.ndarray, magnitude_freqs: np.ndarray, n: float, power_spectrum_sum)
    
    Calculates the spectral roll off frequency from provided power spectrum. Reference: Eyben, p. 41.

    :param np.ndarray power_spectrum: The power spectrum
    :param np.ndarray magnitude_freqs: The magnitude frequencies
    :param float n: The roll-off, as a fraction :math:`(0 \leq n \leq 1.00)`
    :param power_spectrum_sum: The sum of the power spectrum
    :return: The roll-off frequency
    :rtype: float

.. py:function:: spectral_skewness(spectrum_pmf: np.ndarray, magnitude_freqs: np.ndarray, spectral_centroid: float, spectral_variance: float)
    
    Calculates the spectral skewness. Reference: Eyben, pp. 23, 39-40.

    :param np.ndarray spectrum_pmf: The spectrum power mass function PMF
    :param np.ndarray magnitude_freqs: The magnitude frequencies
    :param float spectral_centroid: The spectral centroid
    :param float spectral_variance: The spectral variance
    :return: The spectral skewness
    :rtype: float

.. py:function:: spectral_slope(power_spectrum: np.ndarray)

    Calculates the spectral slope from provided power spectrum. Reference: Eyben, pp. 35-38.

    :param np.ndarray power_spectrum: The power spectrum
    :return: The slope
    :rtype: float

.. py:function:: spectral_slope_region(power_spectrum: np.ndarray, rfftfreqs: np.ndarray, f_lower: float, f_upper: float, sample_rate: int)

    Calculates the spectral slope from provided power spectrum, between the frequencies
    specified. The frequencies specified do not have to correspond to exact bin indices. Reference: Eyben, pp. 35-38.

    :param np.ndarray power_spectrum: The power spectrum
    :param np.ndarray rfftfreqs: The FFT freqs for the power spectrum bins
    :param float f_lower: The lower frequency
    :param float f_upper: The upper frequency
    :param int sample_rate: The sample rate of the audio
    :return: The slope
    :rtype: float

.. py:function:: spectral_variance(spectrum_pmf: np.ndarray, magnitude_freqs: np.ndarray, spectral_centroid: float)
    
    Calculates the spectral variance. Reference: Eyben, pp. 23, 39-40.

    :param np.ndarray spectrum_pmf: The spectrum power mass function PMF
    :param np.ndarray magnitude_freqs: The magnitude frequencies
    :param float spectral_centroid: The spectral centroid
    :return: The spectral variance
    :rtype: float

.. py:function:: zero_crossing_rate(audio: np.ndarray, sample_rate: int)
    
    Extracts the zero-crossing rate. Reference: Eyben, p. 20.
    
    :param np.ndarray audio: A NumPy array of audio samples
    :param float sample_rate: The sample rate of the audio
    :return: The zero-crossing rate
    :rtype: float
