# chord-transcriber (WIP)

## Aim: to identify chords from songs recorded as .wav files.

# Current functionality of _ct.py_
## Loads a .wav and splits the waveform into harmonic and percussive components, computes a fast Fourier transform at many time samples to generate and plot a log-scaled spectrogram, picks out the strongest frequencies in each spectrum and maps these to notes.

# Desired functionality
## To map each set of notes to a chord.
