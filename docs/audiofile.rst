aus.audiofile
##############################

.. py:class:: AudioFile

    .. py:method:: __init__(self, **kwargs)

        Initializes an ``AudioFile`` object. You can pass the following keyword parameters to this method (from https://ccrma.stanford.edu/courses/422-winter-2014/projects/WaveFormat/):

        ``audio_format``: The audio format (should generally be 1)
        ``bits_per_sample``: The number of bits per sample (often 8, 16, 24, or 32)
        ``block_align``: The block align setting (size in bytes of one frame of audio, including all channels)
        ``byte_rate``: Number of bytes per second
        ``bytes_per_sample``: The number of bytes per sample (corresponding to ``bits_per_sample``)
        ``duration``: The duration in seconds
        ``file_name``: The full path of the file_name
        ``num_channels``: The number of channels
        ``frames``: The number of frames
        ``sample_rate``: The sample byte_rate
    
    .. py:method:: copy_header(other)

        Copies the header of another ``AudioFile`` object and returns a new ``AudioFile`` object with the header copied. Does not copy the audio samples.

        :param other: The ``AudioFile`` to copy the header from
        :return: A new ``AudioFile`` object
        :rtype: AudioFile

.. py:function:: convert(file: AudioFile, format: str)

    Converts an AudioFile from one sample format to another. Use this to change between
    int and float format, or to change bit depth (e.g. 16 to 24 bit).
    Supported conversion types: ``'int16'``, ``'int24'``, ``'int32'``, ``'float32'``, ``'float64'``

    :param AudioFile file: An ``AudioFile``
    :param str format: The destination format

.. py:function:: find_files(directory_name: str)

    Finds all WAV and AIFF files within a directory and its subdirectories

    :param str directory_name: The directory name
    :return: A list of file names
    :rtype: list

.. py:function:: read(file_name: str, target_sample_rate: int)

    Reads an audio file (AIFF or WAV) and returns an ``AudioFile`` object containing the contents of the
    file. It uses the ``pedalboard`` library for speed.

    :param str file_name: The name of the file
    :param target_sample_rate: The target sample rate of the audio
    :return: An AudioFile
    :rtype: AudioFile

.. py:function:: write_with_pedalboard(audio: AudioFile, file_name: str)

    Writes an audio file using the ``pedalboard`` library

    :param AudioFile audio: The AudioFile object
    :param str file_name: The file name to use
