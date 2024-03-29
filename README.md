## transcription-tools

This repo contains scripts I wrote to streamline my process of transcribing music by ear. Required packages can be installed with `pip install -r requirements.txt` (NOTE: this will also install [my forked version of pychord](https://github.com/joe-bamford/pychord)).

### List of module dependencies (between all scripts)

- numpy
- matplotlib
- pychord
- pygame
- librosa
- pandas
- scipy
- pyaudio
- keyboard

## _midi-stream.py_

Useful as an aid for learning chord shapes & qualities, as well as for quick identification of uncommon shapes. Requires a keyboard with MIDI output and appropriate computer connectivity (MIDI/USB).

> NOTE: Setting up this script requires identifying which audio device is your piano. If getting a MidiException error then try changing the value of the _dev_id_ variable. The commented-out cell 'DEVICE SETUP' will list all detected audio devices on your system; you can then change _dev_id_ to the desired device. A kernel restart may be required after doing this.

### Current functionality
Takes live midi input from a digital piano and reactively displays notes & chords through a matplotlib window.

### Desired functionality
Quicker response time, as some lag is noticeable when playing very quickly.

## _spectrogram.py_

Useful as a transcription aid, especially for solos.

### Current functionality
Loads a .wav and splits the waveform into harmonic and percussive components, plots a log-scaled spectrogram with only the harmonic component, picks out the strongest frequencies in each spectrum and maps these to notes. Notes in the spectrogram plot can be moused over to show their labels.

## Desired functionality
Where possible, groups of notes should mapped to chords. Have tested this with mixed results so far.

## _ct-stream.py_

> NOTE: Essentially a clone of the program in [this video](https://www.youtube.com/watch?v=AShHJdSIxkY).

### Current functionality
Plots a live waveform and spectrum from microphone input stream, identifies notes from the spectrum. How well this works depends heavily on your microphone.
