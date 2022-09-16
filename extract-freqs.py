# -*- coding: utf-8 -*-
"""
Created on Sun Aug 28 18:48:35 2022

@author: bamjoe
"""

from tools import *
plt.close('all')
sr = 22050

#%% FILE SELECTION

kws = ['matilda', 'mgr', 'mgr-lick']
keys = ['D:maj', 'G:min', 'G:min']
sel = int(input('Select audio file: \n\n(1) '+str(kws[0])+'\n(2) '+str(kws[1])+'\n(3) '+str(kws[2])+'\n\n'))
kw = kws[sel-1]
key = keys[sel-1]

#%% INPUT KEY

# key = str(input('Enter key: '))

# if 'm' in key:
#     key = key.replace('m','')
#     key = key+':min'
# else:
#     key = key+':maj'

#%% READ IN NOTE LIBRARY FROM TXT

notelib = pd.read_csv('note-lib.txt', sep="\s", header=None)
notelib.columns = ["Note", "Freq", "fmin", "fmax"]
# notelib = notelib.iloc[9:97]
# frdown, frup = notelib.iloc[0]['fmin'], notelib.iloc[-1]['fmax']
frdown = 27.5
frup = 5000

#%% LOAD MELODIC SPECTROGRAM AND PLOT

melfile = 'data/'+str(kw)+'-melspec.csv'
spec = pd.read_csv(melfile).to_numpy()
spec = np.delete(spec, 0, axis=1)
spec_db = lb.amplitude_to_db(np.abs(spec), ref=np.max(spec))
abs_spec, ax = plt.subplots(figsize=(20,10))
specplot = lb.display.specshow(spec_db, x_axis='time', y_axis='mel', key=key, ax=ax, hop_length=sr//20, sr=sr)
abs_spec.colorbar(specplot, ax=ax, format="%+2.f dB")
# Get y limits for later plotting of individual spectra
yl = ax.get_ylim()

#%% LOAD CHROMA DECOMP AND PLOT

chrfile = 'data/'+str(kw)+'-chroma.csv'
chroma = pd.read_csv(chrfile).to_numpy()
chroma = np.delete(chroma, 0, axis=1)
fig, ax = plt.subplots(nrows=1, sharex=True)
img = lb.display.specshow(chroma, y_axis='chroma', x_axis='time', ax=ax, key=key)

#%% CHROMA COVARIANCE PLOT
    
ccov = np.cov(spec_db)
fig, ax = plt.subplots()
cp = lb.display.specshow(ccov, y_axis='chroma', x_axis='chroma', key='D:maj', ax=ax)
ax.set(title='Chroma covariance heatmap')
fig.colorbar(cp, ax=ax)

#%% FIND PEAK FREQS

frange = np.linspace(0, yl[1], len(spec_db[:,0]))
subsamples = np.arange(0, len(spec_db[0]), 1)
sps = {}
# pkp = {}
i=0
for sample in subsamples:
    sp = spec_db[:,sample]
    peaks = sg.find_peaks(sp, prominence=20)[0]
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
sp = spec_db[:,s]
idxs = sps[s]['indices']

specfig = plt.figure(figsize=(12,8))
plt.plot(frange, sp, label='Spectrum')
plt.xlabel('Freq / Hz')
plt.ylabel('dB')
plt.xlim(frdown)
plt.scatter(frange[idxs], sp[idxs],c='r',label='Strongest frequencies')
plt.legend(loc='best')

#%% PASS FREQS THROUGH LIBRARY TO IDENTIFY NOTES

sps = tools.get_notes(sps, notelib)
    
#%% USE PYCHORD TO GET CHORDS FROM NOTES

for key in sps:
    notes = sps[key]['notes']
    sps[key]['chord'] = pc.find_chords_from_notes(notes)


