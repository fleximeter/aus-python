audiopython.sampler
##############################

.. py:function:: detect_loop_points(audio: np.ndarray, num_periods: int = 5, effective_zero: float = 0.001, maximum_amplitude_variance: float = 0.1, sample_amplitude_level_boundary: float = 0.1, loop_left_padding: int = 100, loop_right_padding: int = 100)

    Detects loop points in an audio sample. Loop points are frame indices that could be used for
    a seamless repeating loop in a sampler. Ideally, if you choose loop points correctly, no crossfading
    would be needed within the loop.

    We have several requirements for a good loop:
    1. The standard deviation of peak amplitudes should be minimized (i.e. the loop is not increasing or decreasing in amplitude)
    2. The distance between successive wave major peaks should be consistent (i.e. we are looking for periodic waveforms)
    3. The frames at which looping begins and ends should have values as close to 0 as possible (we want to avoid clicks)
    
    :param np.ndarray audio: An audio array
    :param int num_periods: The number of periods to include from the waveform
    :param float effective_zero: The threshold below which we just consider the amplitude to be 0. This is assumed to be a floating-point value between 0 (no amplitude) and 1 (max amplitude). If your file is fixed format, this will be automatically scaled.
    :param float maximum_amplitude_variance: The maximum percentage difference between the biggest and smallest major peak in the loop
    :param float sample_amplitude_level_boundary: Used to determine where the sample sits in the provided audio file. This is useful because we don't want to detect loop points in just any region of the sample - the loop points should have a similar dynamic level to the rest of the sample.
    :param int loop_left_padding: The number of frames to ignore at the start of the amplitude region. This is needed to keep the loop from being in the attack portion of the sound.
    :param int loop_right_padding: The number of frames to ignore at the end of the amplitude region. This is needed to keep the loop from being too close to the decay portion of the sound.
    :return: A list of tuples that are channel index, start frame, and end frame for looping
    :rtype: list

.. py:function:: detect_major_peaks(audio: np.ndarray, min_percentage_of_max: float = 0.9, chunk_width: int = 5000)
    
    Detects major peaks in an audio file. A major peak is a sample peak that is one of the highest in its "local region."
    This is useful for identifying the period length (and therefore the fundamental frequency) of audio with a strong
    first harmonic, since the first harmonic will create the highest peak of the waveform. It will not
    work very well on Gaussian noise or audio with a very weak fundamental.
    
    The "local region" is specified by the chunk width. We segment the audio file into C segments of width chunk_width,
    and search for the highest peak P in that chunk. Then we identify all other peaks that are close in height
    to the highest peak P. A peak is close in height to said peak P if it is greater than or equal to min_percentage_of_max
    of that peak. (For example, suppose the highest peak is 1, and the min_percentage_of_max is 0.9. Then any peak with
    amplitude from 0.9 to 1 will be considered a major peak.)
    
    :param np.ndarray audio: An audio array
    :param float min_percentage_of_max: A peak must be at least this percentage of the maximum peak to be included as a major peak.
    :param int chunk_width: The width of the chunk to search for the highest peak
    :return: Returns a list of tuples; the tuple has a channel index, a frame index, and an amplitude value.
    :rtype: list

.. py:function:: detect_peaks(audio: np.ndarray)

    Detects peaks in an audio file. A peak is located at a sample N where the waveform changes direction.

    :param np.ndarray audio: An AudioFile object with the contents of a WAV file
    :return: Returns a list of indices; each index corresponds to a frame with a peak in the selected channel.
    :rtype: list

.. py:function:: extract_samples(audio: np.ndarray, amplitude_regions: list, pre_frames_to_include: int = 0, post_frames_to_include: int = 0, pre_envelope_type="hanning", pre_envelope_frames: int = 20, post_envelope_type="hanning", post_envelope_frames: int = 20)
    
    Extracts samples from an AudioFile.
    
    :param np.ndarray audio: A 2D numpy ndarray of audio samples
    :param list amplitude_regions: A list of amplitude regions from the identify_amplitude_regions function
    :param int pre_frames_to_include: If this is set to greater than 0, the sample will be extended backward to include these additional frames. This is useful for ensuring a clean sample onset.
    :param int post_frames_to_include: If this is set to greater than 0, the sample will be extended forward to include these additional frames. This is useful for ensuring a clean sample release.
    :param str pre_envelope_type: The envelope type to apply to the beginning of the sound, for a clean onset. Supported envelope types are Bartlett, Blackman, Hamming, and Hanning.
    :param int pre_envelope_frames: The duration in frames of the pre envelope
    :param str post_envelope_type: The envelope type to apply to the end of the sound, for a clean release. Supported envelope types are Bartlett, Blackman, Hamming, and Hanning.
    :param int post_envelope_frames: The duration in frames of the post envelope
    :return: A list of AudioFile objects with the samples
    :rtype: list

.. py:function:: fit_amplitude_envelope(audio: np.ndarray, chunk_width: int = 5000)
    
    Fits an amplitude envelope to a provided audio file.
    Detects peaks in an audio file. Peaks are identified by being surrounded by lower absolute values to either side.
    
    :param np.ndarray audio: An audio array
    :param int chunk_width: The audio is segmented into adjacent chunks, and we look for the highest peak amplitude in each chunk.
    :return: Returns a list of tuples; the tuple has a channel, an index, and an amplitude value.
    :rtype: list

.. py:function:: identify_amplitude_regions(audio: np.ndarray, level_delimiter: float = -30, num_consecutive: int = 10, scale_level_delimiter: bool = True)
    
    Identifies amplitude regions in a sound. You provide a threshold, and any time the threshold is
    breached, we start a new amplitude region which ends when we return below the threshold. This is
    useful for pulling out individual samples from a file that has multiple samples in it.

    :param np.ndarray audio: An audio array
    :param float level_delimiter: The lowest level (dBFS) allowed in a region. This will be scaled by the maximum amplitude in the audio file channel that is being analyzed, unless that feature is turned off by the next parameter. 
    :param int num_consecutive: The number of consecutive samples below the threshold required to end a region. Note that these samples will not be included in the amplitude region; they will only be used to determine if an amplitude region is ending.
    :param bool scale_level_delimiter: Whether or not to scale the level delimiter by the maximum amplitude in the audio file channel that is being analyzed
    :return: A list of tuples. Each tuple contains the starting and ending frame index of an amplitude region.
    :rtype: list
