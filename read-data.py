# -*- coding: utf-8 -*-
"""
Created on Mon Aug 15 12:14:49 2022

@author: bamjoe

INSPIRED BY TUTORIAL BY MEDALLION DATA SCIENCE: https://www.youtube.com/watch?v=ZqpSb5p1xQo
"""

from tkinter import Tk
from tkinter.filedialog import askopenfilename
from tools import *
plt.close('all')

#%% READ FILE

print("Please choose an audio file")
Tk().withdraw() 
file = askopenfilename() #Lets user search for datacube file
print(file)

# kws = ['matilda', 'mgr', 'mgr-lick', 'test-A']
# sel = int(input('Select audio file: \n\n(1) '+str(kws[0])+'\n(2) '+str(kws[1])+'\n(3) '+str(kws[2])+'\n(4) '+str(kws[3])+'\n\n'))
# kw = kws[sel-1]
# data = 'data/'+str(kw)+'.wav'

raw, sr = lb.load(file)
filename = file.split('/')[-1].split('.')[0]
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

melspec = lb.feature.melspectrogram(y=raw, sr=sr, hop_length=sr//20, power=2, fmin=frdown, fmax=frup)
melspecframe = pd.DataFrame(melspec)
melspecframe.to_csv('data/'+str(filename)+'-melspec.csv')

#%% COMPUTE CHROMA STFT AND SAVE TO CSV

S = np.abs(lb.stft(y=raw, n_fft=2048))**2
chroma = lb.feature.chroma_stft(S=S, sr=sr, n_chroma=12)
chromaframe = pd.DataFrame(chroma)
chromaframe.to_csv('data/'+str(filename)+'-chroma.csv')


