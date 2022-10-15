# chord-transcriber (WIP)

## List of module dependencies
- numpy
- matplotlib
- tkinter
- pychord
- librosa
- pandas

# _ct.py_

## Current functionality
Loads a .wav and splits the waveform into harmonic and percussive components, computes a fast Fourier transform at many time samples to generate and plot a log-scaled spectrogram, picks out the strongest frequencies in each spectrum and maps these to notes. Notes are then mapped to chords but not all are yet recognised.

## Desired functionality
To map each set of notes to a chord.

# _ct_stream.py_

## Current functionality
Plots a live waveform and spectrum from microphone input stream, identifies notes and chords from the spectrum.

## Desired functionality
Greater stability in chord detection.
