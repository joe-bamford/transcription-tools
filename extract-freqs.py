# -*- coding: utf-8 -*-
"""
Created on Sun Aug 28 18:48:35 2022

@author: Joe
"""

import numpy as np
import seaborn as sb
import yellowbrick as sb
import librosa as lb
import time
import glob
import scipy
from scipy import signal as sg
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pandas as pd
import librosa.display as lbd
from IPython.display import Audio

from tools import *

#%% LOAD MELODIC SPECTROGRAM AND PLOT

file1 = 'data/matilda-melspec.csv'
spec = pd.read_csv(file1).to_numpy()
spec = np.delete(spec, 0, axis=1)
spec_db = lb.amplitude_to_db(np.abs(spec), ref=np.max(spec))
abs_spec, ax = plt.subplots(figsize=(15,10))
specplot = lb.display.specshow(spec_db,x_axis='time',y_axis='linear',ax=ax)
abs_spec.colorbar(specplot, ax=ax)

#%% FIND PEAK FREQS

subsamples = np.arange(0, len(spec_db[0]), 1)
sps = {}
pkp = {}
i=0
for sample in subsamples:

    sp = spec_db[:,sample]
    peaks = sg.find_peaks(sp, prominence=40)[0]
    peakvals = sp[peaks]

    # check if list not empty and if so dump into dict
    if peaks.tolist():
        sps[i] = {'freqs':peaks,'notes':[]}
        pkp[i] = peakvals
    i+=1

# build array of 3-vectors for strong peaks
# filt2d = tools.dic_to_coords(sps)
# filtpowers = tools.dic_to_coords(pkp)
# strongpoints = np.hstack((filt2d, filtpowers))
# strongpoints = np.delete(strongpoints, 2, axis=1)
# freqframe = pd.DataFrame(strongpoints, columns=['Timestamp', 'Frequency', 'Power'])

#%% PLOT ANY SPECTRUM

s = int(input('Spectrum to plot (0-'+str(len(subsamples)-1)+'): '))
sp = spec_db[:,s]

specfig = plt.figure(figsize=(12,8))
plt.plot(sp, label='Spectrum')
plt.legend(loc='best')
plt.xlabel('Freq / Hz')
plt.ylabel('dB')
plt.scatter(sps[s]['freqs'], sp[sps[s]['freqs']],c='r')

#%% READ IN NOTE LIBRARY FROM TXT

notelib = pd.read_csv('note-lib.txt', sep="\s", header=None)
notelib.columns = ["Note", "Freq", "fmin", "fmax"]

#%% PASS FREQS THROUGH LIBRARY TO IDENTIFY NOTES

# ts = freqframe['Timestamp'][0]
# rows = freqframe.where(freqframe['Timestamp'] == ts)
# for row in freqframe:

# length = len(strongpoints[:,0])    
# ts = strongpoints[0][0]
# #?????
#     rows = np.where(strongpoints[:,0] == ts)[0]
#     notes = []
#     for idx in rows:
#         freq = strongpoints[:,1][idx]
#         r = 0
#         match = False
#         while not match:
#             if not notelib['fmin'][r] < freq < notelib['fmax'][r]:
#                 r += 1
#             else:
#                 note = notelib['Note'][r]
#                 match = True
#         notes.append(note)
#     ts = strongpoints[0][rows[-1]+1]

#%% PASS FREQS THROUGH LIBRARY TO IDENTIFY NOTES

for key in sps:
    notes = []
    for freq in sps[key]['freqs']:
        r = 0
        match = False
        while not match:
            if not notelib['fmin'][r] < freq < notelib['fmax'][r]:
                r += 1
            else:
                note = notelib['Note'][r]
                match = True
        notes.append(note)
    sps[key]['notes'] = notes
    


    
    


