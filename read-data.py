# -*- coding: utf-8 -*-
"""
Created on Mon Aug 15 12:14:49 2022

@author: bamjoe

INSPIRED BY TUTORIAL BY MEDALLION DATA SCIENCE: https://www.youtube.com/watch?v=ZqpSb5p1xQo
"""

from tools import *
plt.close('all')

#%% READ FILE

kws = ['matilda', 'mgr', 'mgr-lick']
sel = int(input('Select audio file: \n\n(1) '+str(kws[0])+'\n(2) '+str(kws[1])+'\n(3) '+str(kws[2])+'\n\n'))
kw = kws[sel-1]
data = 'data/'+str(kw)+'.wav'
raw, sr = lb.load(data)
# Length of audio clip in secs
clip_length = raw.size/sr
# raw = raw[10000:20000]
# compress raw time series
# raw = raw[::5]

#%% PLOT TIME SERIES

# raw_ts = plt.figure(figsize=(15,10))
# plt.title('Raw time series')
# plt.xlabel('Sample')
# plt.plot(raw, lw=1)

#%% SPLIT HARMONIC AND PERCUSSIVE COMPONENTS, PLOT TIME SERIES

fig, ax = plt.subplots(nrows=1, sharex=True)
y_harm, y_perc = lb.effects.hpss(raw)
lb.display.waveshow(y_harm, sr=sr, alpha=0.5, ax=ax, label='Harmonic')
lb.display.waveshow(y_perc, sr=sr, color='r', alpha=0.5, ax=ax, label='Percussive')
ax.set(title='Harmonic and percussive waveforms')
ax.legend(loc='best')

raw = y_harm

#%% READ IN NOTE LIBRARY FROM TXT

notelib = pd.read_csv('note-lib.txt', sep="\s", header=None)
notelib.columns = ["Note", "Freq", "fmin", "fmax"]
# notelib = notelib.iloc[9:97]
frdown, frup = notelib.iloc[0]['fmin'], notelib.iloc[-1]['fmax']

#%% COMPUTE MELODIC SPECTROGRAM AND SAVE TO CSV

melspec = lb.feature.melspectrogram(y=raw, sr=sr, hop_length=sr//20, power=1)
melspecframe = pd.DataFrame(melspec)
melspecframe.to_csv('data/'+str(kw)+'-melspec.csv')

#%% COMPUTE CHROMA STFT AND SAVE TO CSV

S = np.abs(lb.stft(y=raw, n_fft=2048))**2
chroma = lb.feature.chroma_stft(S=S, sr=sr, n_chroma=24)
chromaframe = pd.DataFrame(chroma)
chromaframe.to_csv('data/'+str(kw)+'-chroma.csv')


