# aus

## Introduction
This is a Python library for working with audio. It comes in two flavors - a regular Python version called `pyaus`, contained in the `pyaus` directory, and a Cython version called `caus`, contained in the `caus` directory.

## Building and installation
1. If you are running Windows, you can simply run the command `pip install aus-python` to install a prepackaged version from PyPi.

2. If you are not running Windows, or if you want to build and install the package manually, follow these instructions:
    
    1. Before building this package, first decide whether you wish to use the Python version or the Cython version. Copy all of the .py files from `pyaus` or `caus` to the `aus` directory.

    2. You will need to have a Python virtual environment with `build` installed in it. Alternatively, you can simply install `build` in your local Python installation. You may also need to install the packages `Cython`, `numpy`, and `setuptools` to build the package.

    3. Run the command `python -m build`. The package will be located in the `dist` directory, in both `.whl` and `.tar.gz` format.

    4. To install the package in your local Python installation, simply navigate to the `dist` directory and run the command `pip install filename.whl` (replace `filename` with the actual name of the file in the `dist` directory).

    5. You are now ready to import `aus` into your Python code. Note that the package name is `aus-python`, because PyPi would not let me use the name `aus`. However, when importing into your Python code, you use the line `import aus.audiofile` or `import aus.operations` etc.

## Documentation
Documentation is available at https://aus.readthedocs.io/en/latest/.

## Dependencies
You will need the following Python libraries: `matplotlib`, `numpy`, `pedalboard`, `regex`, `scipy`. You will also need `Cython` if you want to build the Cython version.

## Modules
The package is divided into 8 modules:

### `aus.analysis`
Tools for spectral analysis and analysis of audio waveforms. Many of these tools are based on formulas from Florian Eyben's "Real-Time Speech and Music Classification," published by Springer in 2016. Among other things, this module computes spectral centroid, entropy, slope, and flatness.

### `aus.audiofile`
This module is for reading and writing audio files, using either the `pedalboard` library or using (slower) code provided here.

### `aus.granulator`
Funtionality for grain extraction

### `aus.operations`
This module has various operations that can be performed on audio, such as spectral frame swapping, equal energy forcing, dc bias removal, and beat envelope generation.

### `aus.plot`
Plotting functionality for audio and spectrum

### `aus.sampler`
Tools for extracting samples from audio

### `aus.spectrum`
Tools for spectral analysis

### `aus.synthesis`
Tools for generating simple waveforms
