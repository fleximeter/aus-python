# audiopython

## Introduction
This is a Python library for working with audio.

## Dependencies
You will need the following Python libraries: `matplotlib`, `numpy`, `pedalboard`, `regex`, `scipy`

## Building
To build this package, run `python -m build`. To upload to PyPi, run `twine upload dist/*`.
You should take care to copy the latest files from the `caudiopython` directory to the `audiopython` directory before building, and also make sure to update the package version in `pyproject.toml`.

## Directories
The `audiopython` directory contains the files that will be incorporated into the package. The `caudiopython` directory is a development directory for the Cython version of `audiopython`, and the `pyaudiopython` directory is the development directory for the Python version of `audiopython`.
