# Density of States (DOS) Plotter

A Python tool for plotting electronic Density of States (DOS) data from `.DOS` files.

## Features

* Automatic detection of DOS files
* Multiple DOS comparison
* Fermi level alignment
* Automatic band gap detection
* Publication-quality figures
* High-resolution PNG output

## Author

Ashen Deemantha Liyanage

Zayak's Lab

Department of Physics and Astronomy

Bowling Green State University

## Requirements

```bash
pip install numpy matplotlib
```

## Usage

Place one or more `.DOS` files in the same directory as the script:

```bash
python dos_plotter.py
```

The program will ask for the Fermi level and generate a DOS plot.

## Input Format

Expected file format:

```text
Energy DOS
-10.0 0.0
-9.9 0.0
-9.8 0.1
```

or multiple DOS columns:

```text
Energy DOS1 DOS2 DOS3
```

## Output

* DOS plot (`.png`)
* Band gap detection
* Fermi level alignment

## License

MIT License

# density-of-states-plotter
Python tool for plotting Density of States (DOS) data with automatic Fermi level alignment and band gap detection.
