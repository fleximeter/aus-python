aus.operations
##############################

.. py:function:: adjust_level(audio: np.ndarray, max_level: float)

    Adjusts the level of audio to a specified dB level

    :param np.ndarray audio: The audio samples as a NumPy array
    :param float max_level: The max level for the audio
    :return: The scaled audio
    :rtype: np.ndarray

.. py:function:: beat_envelope(tempo, sample_rate, beat_sequence, envelope_type="hanning", envelope_duration=1000)
    
    Generates a beat envelope. You specify the tempo, and provide a list of beat durations in order.
    This function will generate a volume envelope that can be applied to a sound file to make it
    pulse with these beat durations.

    :param float tempo: The tempo
    :param int sample_rate: The audio sample rate
    :param list beat_sequence: A sequence of Fractions representing beat durations
    :param str envelope_type: The envelope used for fade-in and fade-out on each beat
    :param int envelope_duration: The envelope duration. The envelope will be split in half and applied to the beginning and end of the beat. If the beat is too short, a shorter envelope will be generated for that beat.
    :return: An array with the beat envelope
    :rtype: np.ndarray

.. py:function:: beat_envelope_multichannel(tempo: float, sample_rate: int, beat_sequence: list, num_channels: int, channel_levels: list, envelope_type="hanning", envelope_duration: int = 1000)
    
    Generates a multichannel beat envelope. You specify the tempo, and provide a list of *N* beat durations in order.
    You also specify the number of output channels M and a list of level tuples *N*x*M* - one level coefficient for each channel,
    for each beat.
    This function will generate a volume envelope that can be applied to a sound file to make it
    pulse with these beat durations. You will need to provide a multichannel sound file with the correct number of channels
    when you apply the envelope.

    :param float tempo: The tempo
    :param int sample_rate: The audio sample rate
    :param list beat_sequence: A sequence of Fractions representing beat durations
    :param int num_channels: The number of channels in the envelope
    :param list channel_levels: A list of channel level tuples (or lists). Each sublist corresponds to the level coefficients for the current beat.
    :param str envelope_type: The envelope used for fade-in and fade-out on each beat
    :param int envelope_duration: The envelope duration. The envelope will be split in half and applied to the beginning and end of the beat. If the beat is too short, a shorter envelope will be generated for that beat.
    :return: An array with the beat envelope
    :rtype: np.ndarray

.. py:function:: calculate_dc_bias(audio: np.ndarray)
    
    Calculates DC bias of an audio signal
    
    :param np.ndarray audio: The audio signal
    :return: The DC bias
    :rtype: float

.. py:function:: cpsmidi(freq: float)

    Calculates the MIDI note of a provided frequency

    :param float freq: The frequency in Hz
    :return: The MIDI note
    :rtype: float

.. py:function:: dbfs(audio)

    Calculates dbfs (decibels full scale) for an audio sequence or sample. 
    This function assumes that the audio is in float format where 1 is the highest possible peak.

    :param np.ndarray audio: The audio array or sample to calculate dbfs for
    :return: A float value representing the dbfs
    :rtype: float

.. py:function:: dbfs_audio(audio: np.ndarray)

    Calculates dbfs (decibels full scale) for a chunk of audio. This function will use the RMS method, 
    and assumes that the audio is in float format where 1 is the highest possible peak.

    :param np.ndarray audio: The audio to calculate dbfs for
    :return: A float value representing the dbfs
    :rtype: float

.. py:function:: dbfs_max_local(audio: np.ndarray, chunk_size: int = 10, hop_size: int = 5)
    
    Checks the maximum local dbfs (decibels full scale) of an audio file

    :param np.ndarray audio: The audio
    :param int chunk_size: The chunk size to check
    :param int hop_size: The number of frames to hop from chunk center to chunk center
    :return: The max local dbfs
    :rtype: float

.. py:function:: dbfs_min_local(audio: np.ndarray, chunk_size: int = 10, hop_size: int = 5)
    
    Checks the minimum local dbfs (decibels full scale) of an audio file

    :param np.ndarray audio: The audio
    :param int chunk_size: The chunk size to check
    :param int hop_size: The number of frames to hop from chunk center to chunk center
    :return: The min local dbfs
    :rtype: float

.. py:function:: exchanger(data: np.ndarray, hop: int)
    
    Exchanges samples in an audio file or STFT frames in a spectrum. Each sample (or STFT frame) 
    is swapped with the sample (or STFT frame) ``hop`` steps ahead or ``hop`` steps behind. If audio
    is being processed, it should be in the shape ``(channels, samples)``. If STFT data is being
    processed, it should be in the shape ``(channels, frames, bins)``.

    :param np.ndarray data: The audio (or spectrum) to process
    :param int hop: The hop size
    :return: The exchanged audio (or spectrum)
    :rtype: np.ndarray

.. py:function:: fade_in(audio: np.ndarray, envelope="hanning", duration: int = 100)
    
    Implements a fade-in on an array of audio samples.

    :param np.ndarray audio: The array of audio samples (may have multiple channels; the fade-in will be applied to all channels)
    :param str envelope: The shape of the fade-in envelope. Must be a NumPy envelope. The envelope will be divided in half, and only the first half will be used.
    :param int duration: The duration (in frames) of the fade-in envelope half. If the duration is longer than the audio, it will be truncated.
    :return: The audio with a fade in applied.
    :rtype: np.ndarray

.. py:function:: fade_out(audio: np.ndarray, envelope="hanning", duration: int = 100)
    
    Implements a fade-out on an array of audio samples.

    :param np.ndarray audio: The array of audio samples (may have multiple channels; the fade-out will be applied to all channels)
    :param str envelope: The shape of the fade-out envelope. Must be a NumPy envelope. The envelope will be divided in half, and only the second half will be used.
    :param int duration: The duration (in frames) of the fade-out envelope half. If the duration is longer than the audio, it will be truncated.
    :return: The audio with a fade-out applied.
    :rtype: np.ndarray

.. py:function:: force_equal_energy(audio: np.ndarray, dbfs: float = -6.0, window_size: int = 8192)
    
    An algorithm that forces equal energy on a mono signal over time. 
    For example, if a signal initially has high energy, and gets less energetic, this will adjust 
    the energy level so that it does not decrease.
    Better results come with using a larger window size, so the energy changes more gradually.

    :param np.ndarray audio: The array of audio samples
    :param float dbfs: The target level of the entire signal, in dbfs
    :param int window_size: The window size to consider when detecting RMS energy
    :return: An adjusted version of the signal
    :rtype: np.ndarray

.. py:function:: leak_dc_bias_averager(audio: np.ndarray)
    
    Leaks DC bias of an audio signal
    
    :param np.ndarray audio: The audio signal
    :return: The bias-free signal
    :rtype: np.ndarray

.. py:function:: leak_dc_bias_filter(audio: np.ndarray)
    
    Leaks DC bias of an audio signal using a highpass filter, described on pp. 762-763
    of "Understanding Digital Signal Processing," 3rd edition, by Richard G. Lyons
    
    :param np.ndarray audio: The audio signal
    :return: The bias-free signal
    :rtype: np.ndarray

.. py:function:: midicps(midi_note: float)
    
    Calculates the frequency of a specified MIDI note

    :param float midi_note: The MIDI note
    :return: The frequency in Hz
    :rtype: float

.. py:function:: midiratio(interval: float)
    
    Calculates the MIDI ratio of a specified MIDI interval

    :param freq interval: The MIDI interval in half steps
    :return: The ratio
    :rtype: float

.. py:function:: mixdown(audio: np.ndarray)

    Mixes a multichannel signal to a mono signal. 

    :param np.ndarray audio: The audio to mix if it isn't mono
    :return: The mixed audio
    :rtype: np.ndarray

.. py:function:: pan_level_adjuster(pan_levels: np.ndarray)

    Adjusts pan levels in a list for a power sum of 1. The values in the list should be fractional 
    volume levels that sum to 1. After applying this operations, the values in the list will be adjusted
    so that their squares now sum to 1. The levels are adjusted in place.

    The idea is that you might want to arbitrarily divide the total volume of a sound over several
    channels. However, you want the sum of the signal power to equal to 1. So you need to
    adjust these fractional levels so that the power sum is correct. This function computes
    a scalar that is applied to all of the pan levels to make the summed power level equal to 1.

    :param np.ndarray pan_levels: A list of pan levels (one level for each channel)

.. py:function:: pan_mapper(pan_coefficients: np.ndarray, mapper: np.ndarray)
    
    Maps pan positions to actual speaker positions. You pass a mapping array 
    that lists the speaker numbers in panning order.
    
    This is useful if you want to use a different numbering system for your 
    pan positions than the numbering system used for the actual output channels.
    For example, you might want to pan in a circle for a quad-channel setup,
    but the hardware is set up for stereo pairs.

    Example: Suppose you have a quad setup. Your mapper would be ``[0, 1, 3, 2]`` 
    if you are thinking clockwise, or ``[1, 0, 2, 3]`` if you are thinking counterclockwise. 
    If you have an 8-channel setup, your mapper would be ``[0, 1, 3, 5, 7, 6, 4, 2]`` 
    for clockwise and ``[1, 0, 2, 4, 6, 7, 5, 3]`` for counterclockwise.
    
    :param np.ndarray pan_coefficients: A list of pan coefficient lists
    :param np.ndarray mapper: The mapper for reordering the pan coefficients
    :return: A new, mapped pan coefficient list
    :rtype: np.ndarray

.. py:function:: panner(num_channels: int, start_pos: int, end_pos: int, num_iterations: int, pan_law: str = "constant_power")
    
    Multichannel panner, moving from ``start_pos`` to ``end_pos`` over ``num_iterations``.
    It generates a list of pan coefficients (each coefficient is the volume coefficient
    for the corresponding channel).
    (https://www.cs.cmu.edu/~music/icm-online/readings/panlaws/panlaws.pdf)

    :param int num_channels: The number of channels
    :param float start_pos: The start panning position
    :param float end_pos: The end panning position
    :param int num_iterations: The number of steps to take to move from start_pos to end_pos
    :param str pan_law: The pan law ("linear", "constant_power", "neg_4_5_db")
    :return: An array of pan coefficients
    :rtype: np.ndarray

.. py:function:: stochastic_exchanger(data: np.ndarray, max_hop: int)

    Stochastically exchanges samples in an audio file or STFT frames in a spectrum. Each sample 
    (or STFT frame) is swapped with the sample (or STFT frame) up to ``max_hop`` steps ahead or ``max_hop`` 
    steps behind. If audio is being processed, it should be in the shape ``(channels, samples)``. 
    If STFT data is being processed, it should be in the shape ``(channels, frames, bins)``.
    
    .. WARNING::
        If you try to run this on sampled audio rather than STFT data, this will take a *very* long time!

    :param np.ndarray data: The audio (or spectrum) to process
    :param int hop: The hop size
    :return: The exchanged audio (or spectrum)
    :rtype: np.ndarray
