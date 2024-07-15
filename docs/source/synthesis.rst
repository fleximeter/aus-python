audiopython.synthesis
##############################

.. py:function:: saw(freq: float, max_harmonic: int, len: int, sample_rate: int = 44100)
    
    Generates a sawtooth tone
    
    :param float freq: The frequency
    :param int max_harmonic: The maximum harmonic index
    :param int len: The length of the signal
    :param int sample_rate: The audio sample rate
    :return: The sawtooth signal
    :rtype: np.ndarray

.. py:function:: sine(freq: float, phase: float, len: int, sample_rate: int = 44100)
    
    Generates a sine tone

    :param float freq: The frequency
    :param float phase: The phase
    :param int len: The length of the signal
    :param int sample_rate: The audio sample rate
    :return: The sine signal
    :rtype: np.ndarray

.. py:function:: square(freq: float, max_harmonic: int, len: int, sample_rate: int = 44100)

    Generates a square tone

    :param float freq: The frequency
    :param int max_harmonic: The maximum harmonic index
    :param int len: The length of the signal
    :param int sample_rate: The audio sample rate
    :return: The square signal
    :rtype: np.ndarray

.. py:function:: triangle(freq: float, max_harmonic: int, len: int, sample_rate: int = 44100)
    
    Generates a triangle tone

    :param float freq: The frequency
    :param int max_harmonic: The maximum harmonic index
    :param int len: The length of the signal
    :param int sample_rate: The audio sample rate
    :return: The triangle signal
    :rtype: np.ndarray
