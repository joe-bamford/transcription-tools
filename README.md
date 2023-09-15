## chord-detector (WIP)


### List of module dependencies (between all scripts)

- numpy
- matplotlib
- pychord
- pygame
- librosa
- pandas
- scipy
- pyaudio
- struct
- keyboard
- yellowbrick (optional, only for plot aesthetics)

> NOTE: These scripts will only work if you install my forked version of pychord.

## _midi-stream.py_

> NOTE: Setting up this script requires identifying which audio device is your piano. The commented-out cell 'DEVICE SETUP' will list all detected audio devices on your system; you can then change the _dev_id_ variable to the desired device. A kernel restart may be required after doing this.

### Current functionality
Takes live midi input from a digital piano and reactively displays notes/chords through a matplotlib window.

### Desired functionality
Quicker response time, especially with complex chords.

## _ct.py_

### Current functionality
Loads a .wav and splits the waveform into harmonic and percussive components, generates and plots a log-scaled spectrogram, picks out the strongest frequencies in each spectrum and maps these to notes. Where possible, groups of notes are then mapped to chords.

## Desired functionality
Greater reliability with chord identification.

## _ct-stream.py_

> NOTE: Essentially a clone of the program in this video - https://www.youtube.com/watch?v=AShHJdSIxkY.

### Current functionality
Plots a live waveform and spectrum from microphone input stream, identifies notes from the spectrum.

### Desired functionality
Greater stability in chord detection.
