# aus

## Introduction
This is a Python library for working with audio. It comes in two flavors - a regular Python version called `pyaus`, contained in the `pyaus` directory, and a Cython version called `caus`, contained in the `caus` directory. There is a separate directory called `aus` that is set up for building a package - at the moment, this directory contains a copy of the Cython version.

You can install this library from PyPi by running the command `pip install aus`. This will install the Cython version, which is only compiled for Windows at the moment. You can also build the package yourself on your own computer if you wish. Or you can use individual modules in the `pyaus` or `caus` directories.

## Documentation
Documentation is available at https://aus.readthedocs.io/en/latest/.

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

## Dependencies
You will need the following Python libraries: `matplotlib`, `numpy`, `pedalboard`, `regex`, `scipy`. You will also need `Cython` if you want to build the Cython version.

## Building
To build this package, run `python -m build`.
