# -*- coding: utf-8 -*-
"""
Created on Mon Aug 15 12:14:49 2022

@author: bamjoe

INSPIRED BY TUTORIAL BY MEDALLION DATA SCIENCE: https://www.youtube.com/watch?v=ZqpSb5p1xQo
"""

from tkinter import Tk
from tkinter.filedialog import askopenfilename
from tools import *
from scipy import optimize as opt
import math

plt.close('all')
# FFT SAMPLE RATE (Hz)
fft_sr = 20

#%% READ FILE

print("Please choose an audio file")
Tk().withdraw() 
file = askopenfilename() # Lets user search for file
print(file)

raw, sr = lb.load(file)
filename = file.split('/')[-1].split('.')[0]
# Length of audio clip in secs
clip_length = raw.size/sr

# raw = raw[10000:20000]
# compress raw time series
# raw = raw[::5]

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

# #%% COMPUTE MELODIC SPECTROGRAM AND SAVE TO CSV

# melspec = lb.feature.melspectrogram(y=raw, sr=sr, hop_length=sr//fft_sr, power=2, fmax=sr/2, n_mels=108)
# melspecframe = pd.DataFrame(melspec)
# melspecframe.to_csv('data/'+str(filename)+'-melspec.csv')

# #%% COMPUTE CHROMA STFT AND SAVE TO CSV

# S = np.abs(lb.stft(y=raw, n_fft=2048))**2
# chroma = lb.feature.chroma_stft(S=S, sr=sr, hop_length=sr//fft_sr, n_chroma=12)
# chromaframe = pd.DataFrame(chroma)
# chromaframe.to_csv('data/'+str(filename)+'-chroma.csv')


#%% LOG-FREQ SPECTROGRAM

fig, ax = plt.subplots(nrows=1, ncols=1, sharex=False)
spec_db = lb.amplitude_to_db(np.abs(lb.stft(raw, hop_length=sr//fft_sr)), ref=np.max)
# spec_db = lb.feature.melspectrogram(S=spec_db, hop_length=sr//fft_sr, fmax=sr/2)
img = lb.display.specshow(spec_db, y_axis='fft_note', sr=sr, hop_length=sr//20, x_axis='time', ax=ax)
ax.set(title='Log-frequency power spectrogram')
ax.label_outer()
fig.colorbar(img, ax=ax, format="%+2.f dB")
yl = ax.get_ylim()

#%% GET Y-AXIS ATTRIBUTES FROM SPECTROGRAM

# Y-axis object
yax = ax.yaxis
# List of attribute names for yax object...
attname = dir(yax)
# ...that contain 'get'
attname = [i for i in attname if 'get' in i]
# List of above attributes
att = [getattr(yax, attname[s]) for s in range(len(attname))]

#%% INPUT KEY

key = tools.get_key()

# #%% LOAD MELODIC SPECTROGRAM AND PLOT

# melfile = 'data/'+str(filename)+'-melspec.csv'
# spec = pd.read_csv(melfile).to_numpy()
# spec = np.delete(spec, 0, axis=1)
# spec_db = lb.amplitude_to_db(np.abs(spec), ref=np.max(spec))
# abs_spec, ax = plt.subplots(figsize=(20,10))
# specplot = lb.display.specshow(spec_db, x_axis='time', y_axis='mel', key=key, ax=ax, hop_length=sr//fft_sr, sr=sr, fmax=sr/2)
# abs_spec.colorbar(specplot, ax=ax, format="%+2.f dB")
# # Get y limits for later plotting of individual spectra
# yl = ax.get_ylim()

#%% FIT FREQUENCY CURVE

# def func(x, a, b, c):
#     # f = a*b**(x) + c
#     base = 2**(1/12)
#     # f = a*(np.log(b*x)/np.log(base)) + c
#     f = a*math.log(b*x, base) + c          #?????
#     return f

# fit = opt.curve_fit(func, frq, nums)[0]
# fig = plt.figure()
# plt.scatter(frq, nums)
# lr = np.linspace(0, 10000, 1000)
# plt.plot(func(lr, fit[0], fit[1], fit[2]))

# flim = 

#%% LOAD CHROMA DECOMP AND PLOT

chrfile = 'data/'+str(filename)+'-chroma.csv'
chroma = pd.read_csv(chrfile).to_numpy()
chroma = np.delete(chroma, 0, axis=1)
fig, ax = plt.subplots(nrows=1, sharex=True)
img = lb.display.specshow(chroma, y_axis='chroma', x_axis='time', ax=ax, hop_length=sr//fft_sr, key=key, fmin=frdown, fmax=frup)

#%% CHROMA COVARIANCE PLOT
    
ccov = np.cov(spec_db)
fig, ax = plt.subplots()
cp = lb.display.specshow(ccov, y_axis='chroma', x_axis='chroma', key=key, ax=ax)
ax.set(title='Chroma covariance heatmap')
fig.colorbar(cp, ax=ax)

#%% FIND PEAK FREQS

frange = np.linspace(yl[0], yl[1], len(spec_db[:,0]))
subsamples = np.arange(0, len(spec_db[0]), 1)
sps = {}
# pkp = {}
i=0
for sample in subsamples:
    sp = spec_db[:,sample]
    peaks = sg.find_peaks(sp, prominence=1)[0]
    freqs = frange[peaks]
    # peakvals = sp[peaks]
    # Remove values outside frequency range of the piano
    freqs = freqs[(freqs > frdown) & (freqs < frup)]
    # Check if list not empty, and if so dump into dict
    if peaks.tolist():
        sps[i] = {'indices':peaks,'freqs':freqs,'notes':[],'chord':[]}
        # pkp[i] = peakvals
    i+=1
    
#%% PLOT ANY SPECTRUM

s = int(input('Spectrum to plot (0-'+str(len(subsamples)-1)+'): '))
spectime = clip_length*s/(len(subsamples)-1)
print('Spectrum at t =', spectime, 's')
sp = spec_db[:,s]
idxs = sps[s]['indices']

melfreqs = lb.mel_frequencies(n_mels=len(sp), fmin=0, fmax=7902)

specfig = plt.figure(figsize=(12,8))
ax2 = specfig.add_subplot(1,1,1)
yax2 = ax2.yaxis
attname2 = dir(yax2)
attname2 = [i for i in attname2 if 'set' in i]

plt.plot(melfreqs, sp, label='Spectrum')
# plt.xscale('log')
plt.xlabel('Freq / Hz')
plt.ylabel('dB')
plt.scatter(melfreqs[idxs], sp[idxs],c='r',label='Strongest frequencies')
plt.legend(loc='best')

# STILL A FREQ SCALE ISSUE HERE

#%% PASS FREQS THROUGH LIBRARY TO IDENTIFY NOTES

sps = tools.get_notes(sps, notelib)
    
#%% USE PYCHORD TO GET CHORDS FROM NOTES

for key in sps:
    notes = sps[key]['notes']
    sps[key]['chord'] = pc.find_chords_from_notes(notes)
    
#%%



    
    
    
    
    
    
    
    
    
    
    
    
    
    