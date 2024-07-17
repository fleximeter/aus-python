aus.granulator
######################

.. py:function:: extract_grain(audio: np.ndarray, start_point: cython.int = -1, grain_size: cython.int = -1, window="hanning", max_window_size: cython.int = -1)

    Extracts a single grain from an array of samples.

    :param np.ndarray audio: A numpy array of audio samples
    :param int start_point: The starting frame of the grain. If -1, this will be randomly chosen.
    :param int grain_size: The size of the grain in frames. If -1, this will be randomly chosen.
    :param str window: The window that will be applied to the grain.
    :param int max_window_size: If not -1, the window will not be larger than this size. If the grain is longer, the window will be split and only applied to the start and end of the grain.
    :return: A Numpy array with the grain
    :rtype: np.ndarray

.. py:function:: find_max_grain_dbfs(grains: list)

    Finds the maximum overall dbfs (by grain) of a list of grains. Useful
    for getting rid of grains with a low dbfs.
    
    :param list grains: A list of grains
    :return: The dbfs of the grain with the loudest dbfs
    :rtype: float

.. py:function:: merge_grains(grains: list, overlap_size: cython.int = 10)

    Merges a list of grains, with some overlap between grains

    :param list grains: A list of grains
    :param int overlap_size: The number of samples to overlap from grain to grain
    :return: An array with the combined grains
    :rtype: np.ndarray

.. py:function:: scale_grain_peaks(grains: list)

    Scales the peaks of a list of grains so they all have the same peak amplitude.
    The grains will be scaled in place.

    :param list grains: The list of grains
