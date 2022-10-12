# -*- coding: utf-8 -*-
"""
Created on Mon Aug 15 12:14:49 2022

@author: bamjoe

INSPIRED BY TUTORIAL BY MEDALLION DATA SCIENCE: https://www.youtube.com/watch?v=ZqpSb5p1xQo
"""

from tools import *
plt.close('all')

#%% WELCOME AND READ FILE

print("Please choose an audio file")
Tk().withdraw() 
# Prompt user to search for file
file = askopenfilename()

# Read wav file
raw, sr = lb.load(file)
filename = file.split('/')[-1].split('.')[0]
# Length of audio clip in secs
clip_length = raw.size/sr

# Compress raw time series
# raw = raw[::5]

# Input key
key = tools.get_key()

#%% SPLIT HARMONIC AND PERCUSSIVE COMPONENTS, PLOT TIME SERIES, GET TEMPO

# Plot split time series
fig, ax = plt.subplots(nrows=1, sharex=True)
y_harm, y_perc = lb.effects.hpss(raw)
lb.display.waveshow(y_harm, sr=sr, alpha=0.5, ax=ax, label='Harmonic')
lb.display.waveshow(y_perc, sr=sr, color='r', alpha=0.5, ax=ax, label='Percussive')
ax.set(title='Harmonic and percussive waveforms')
ax.legend(loc='best')

# Tempo estimation
tempo = lb.beat.tempo(y=raw, sr=sr)
# FFT sample rate (Hz) (= 4x beat frequency)
fft_sr = int(np.around(tempo/15, 0)) # 1/15 = 4/60
fft_win = 2048

# Use harmonic component from here on
raw = y_harm

#%% LOG-FREQ SPECTROGRAM

# Plot spectrogram
fig, ax = plt.subplots(nrows=1, ncols=1, sharex=False)
spec_db = lb.amplitude_to_db(np.abs(lb.stft(raw, hop_length=sr//fft_sr, n_fft=fft_win)**2), ref=np.max)
img = lb.display.specshow(spec_db, y_axis='fft_note', sr=sr, hop_length=sr//fft_sr, x_axis='time', ax=ax, n_fft=fft_win)
ax.set(title='Log-frequency power spectrogram')
ax.label_outer()
# ax.grid(visible=True, which='major', axis='x', alpha=1, color='white')
fig.colorbar(img, ax=ax, format="%+2.f dB")
yl = ax.get_ylim()

#%% LOAD CHROMA DECOMP AND PLOT

# Chromagram
S = np.abs(lb.stft(y=raw, n_fft=2048))**2
chroma = lb.feature.chroma_stft(S=S, sr=sr, hop_length=sr//fft_sr, n_chroma=12)
chroma = np.delete(chroma, 0, axis=1)
fig, ax = plt.subplots(nrows=1, sharex=True)
img = lb.display.specshow(chroma, y_axis='chroma', x_axis='time', ax=ax, hop_length=sr//fft_sr, key=key, fmin=frdown, fmax=frup)

#%% FIND PEAK FREQS

frange = np.linspace(yl[0], yl[1], len(spec_db[:,0]))
subsamples = np.arange(0, len(spec_db[0]), 1)
freqdict = {'Timestamp':[],'Indices':[],'Freqs':[]}

i=0
for sample in subsamples:
    sp = spec_db[:,sample]
    peaks = sg.find_peaks(sp, prominence=30)[0]
    freqs = frange[peaks]
    # peakvals = sp[peaks]
    # Remove values outside frequency range of the piano
    freqs = freqs[(freqs > frdown) & (freqs < frup)]
    # Check if list not empty, and if so dump into dict
    if peaks.tolist():
        freqdict['Timestamp'].append(i)
        freqdict['Indices'].append(peaks)
        freqdict['Freqs'].append(freqs)
    i+=1

# Convert to dataframe
chordframe = pd.DataFrame.from_dict(freqdict)
        
#%% PLOT ANY SPECTRUM

# Choose spectrum by timestamp
s = -1
while not s in chordframe['Timestamp'].tolist():
    try:
        s = input('Spectrum to plot (0-'+str(len(subsamples)-1)+'): ')
        if len(s) == 0:
            break
        else:
            s = int(s)
    except ValueError:
        continue

# Plot corresponding timeslice of spectrogram
if len(str(s)) > 0:
    spectime = np.around(clip_length*s/(len(subsamples)-1),2)
    sp = spec_db[:,s]
    df_idx = chordframe[chordframe['Timestamp'] == s].index.item()
    idxs = chordframe.loc[df_idx,'Indices']
    fftfreqs = lb.fft_frequencies(sr=sr, n_fft=fft_win) 
    specfig = plt.figure(figsize=(12,8))
    plt.plot(fftfreqs, sp, label='Spectrum')
    plt.xscale('log')
    plt.xlabel('Freq / Hz')
    plt.ylabel('dB')
    plt.scatter(fftfreqs[idxs], sp[idxs],c='r',label='Strongest frequencies')
    plt.title('Spectrum '+str(s)+' at t = '+str(spectime)+'s', fontsize=20)
    plt.legend(loc='best', fontsize=16)
else:
    pass

#%% IDENTIFY NOTES THEN USE PYCHORD TO GET CHORDS FROM NOTES

from tools import *

# First, get notes
chordframe = tools.get_notes(chordframe)

# Remove rows with fewer than 3 distinct notes
chordframe = chordframe[chordframe['Notes'].map(len) >= 3]

# First pass at chord finding
chordframe = tools.get_chords(chordframe, force_slash=False)

# Filter out failed rows
empties = chordframe[chordframe['Chord'].map(len) == 0]

# Second pass to deal with awkward slashes
empties = tools.get_chords(empties, force_slash=True)

# Add forced slash chords to chordframe
forced_slashes = empties[empties['Chord'].map(len) > 0]
for i in forced_slashes.index:
    chordframe.loc[i, 'Chord'] = forced_slashes['Chord'][i]

# Delete all rows still chordless
chordframe = chordframe[chordframe['Chord'].map(len) > 0]

#%% TEST CELL
















    
    
    