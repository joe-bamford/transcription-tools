# -*- coding: utf-8 -*-
"""
Created on Sun Aug 28 18:48:35 2022

@author: bamjoe
"""

from tools import *

#%% READ IN NOTE LIBRARY FROM TXT

notelib = pd.read_csv('note-lib.txt', sep="\s", header=None)
notelib.columns = ["Note", "Freq", "fmin", "fmax"]
notelib = notelib.iloc[9:97]
frdown, frup = notelib.iloc[0]['fmin'], notelib.iloc[-1]['fmax']

#%% LOAD MELODIC SPECTROGRAM AND PLOT

file1 = 'data/matilda-melspec.csv'
spec = pd.read_csv(file1).to_numpy()
spec = np.delete(spec, 0, axis=1)
spec_db = lb.amplitude_to_db(np.abs(spec), ref=np.max(spec))
abs_spec, ax = plt.subplots(figsize=(15,10))
specplot = lb.display.specshow(spec_db,x_axis='time',y_axis='chroma',key='D:maj',ax=ax)
abs_spec.colorbar(specplot, ax=ax, format="%+2.f dB")

#%% FIND PEAK FREQS

subsamples = np.arange(0, len(spec_db[0]), 1)
sps = {}
# pkp = {}
i=0
for sample in subsamples:
    sp = spec_db[:,sample]
    peaks = sg.find_peaks(sp, prominence=30)[0]
    # peakvals = sp[peaks]
    print(peaks)    
    # Remove values outside frequency range of the piano
    peaks = peaks[(peaks > frdown) & (peaks < frup)]
    print(peaks)
    # Check if list not empty, and if so dump into dict
    if peaks.tolist():
        sps[i] = {'freqs':peaks,'notes':[]}
        # pkp[i] = peakvals
    i+=1

#%% PLOT ANY SPECTRUM

s = int(input('Spectrum to plot (0-'+str(len(subsamples)-1)+'): '))
sp = spec_db[:,s]

specfig = plt.figure(figsize=(12,8))
plt.plot(sp, label='Spectrum')
plt.xlabel('Freq / Hz')
plt.ylabel('dB')
plt.xlim(frdown)
plt.scatter(sps[s]['freqs'], sp[sps[s]['freqs']],c='r',label='Strongest freqs')
plt.legend(loc='best')

#%% PASS FREQS THROUGH LIBRARY TO IDENTIFY NOTES

sps = tools.get_notes(sps, notelib)
    
#%% CHROMA COVARIANCE PLOT
    
ccov = np.cov(spec_db)
fig, ax = plt.subplots()
cp = lb.display.specshow(ccov, y_axis='chroma', x_axis='chroma', key='D:maj', ax=ax)
ax.set(title='Chroma covariance heatmap')
fig.colorbar(cp, ax=ax)


