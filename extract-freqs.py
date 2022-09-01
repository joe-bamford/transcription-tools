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

#%% LOAD SPECTROGRAM AND PLOT

# file = 'data/matilda-spec.csv'
# spec = pd.read_csv(file)
# spec_db = lb.amplitude_to_db(spec, ref=np.max(spec))
# abs_spec, ax = plt.subplots(figsize=(15,10))
# specplot = lb.display.specshow(spec_db,x_axis='time',y_axis='log',ax=ax)
# abs_spec.colorbar(specplot, ax=ax)

#%% LOAD MELODIC SPECTROGRAM AND PLOT

file1 = 'data/matilda-melspec.csv'
spec = pd.read_csv(file1).to_numpy()
spec = np.delete(spec, 0, axis=1)
spec_db = lb.amplitude_to_db(np.abs(spec), ref=np.max(spec))
abs_spec, ax = plt.subplots(figsize=(15,10))
specplot = lb.display.specshow(spec_db,x_axis='time',y_axis='linear',ax=ax)
abs_spec.colorbar(specplot, ax=ax)

#%% FIND PEAK FREQS WITH SAVGOL FILTER

#spectrum with max value = 961

subsamples = np.arange(0, len(spec_db[0]), 1)
# savgols = np.zeros_like(spec_db)
sps = {}
pkp = {}
i=0
for sample in subsamples:

    sp = spec_db[:,sample]
    # if len(sp)%2 == 1:
    #     winlen = int(len(sp))
    # else:
    #     winlen = int(len(sp) - 1)
    # savgol = sg.savgol_filter(sp,winlen,5)
    # bodge to fix mid-window filter spike
    # midwin = len(sp)//2
    # savgol[midwin] = 0.5*(savgol[midwin - 1]+savgol[midwin])
    # savgol[255] = 0.5*(savgol[254] + savgol[256])
    peaks = sg.find_peaks(sp, prominence=40)[0]
    peakvals = sp[peaks]
    
    # peakpowers = []
    # strongpeaks = []
    # for peak in peaks:
    #     if sp[peak] - savgol[peak] >= 20:
    #         strongpeaks.append(peak)
    #         peakpowers.append(sp[peak])
            
    # savgols[:,i] = savgol
    # check if list not empty and if so dump into dict
    if peaks.tolist():
        sps[i] = peaks
        pkp[i] = peakvals
    i+=1

# build array of 3-vectors for strong peaks
filt2d = tools.dic_to_coords(sps)
filtpowers = tools.dic_to_coords(pkp)
strongpoints = np.hstack((filt2d, filtpowers))
strongpoints = np.delete(strongpoints, 2, axis=1)

#%% PLOT ANY SPECTRUM

s = int(input('Spectrum to plot (0-'+str(len(subsamples)-1)+'): '))
sp = spec_db[:,s]

specfig = plt.figure(figsize=(12,8))
plt.plot(sp, label='Spectrum')
# plt.plot(savgols[:,s], label='Savgol filter')
plt.legend(loc='best')
plt.xlabel('Freq / Hz')
plt.ylabel('dB')
plt.scatter(sps[s], sp[sps[s]],c='r')

#%% 3D SAVGOL PLOT

# fig = plt.figure(figsize=(15,10))
# ax = fig.add_subplot(111, projection='3d')
# Z = savgols
# y = np.linspace(0,len(spec[:,0]),len(spec[:,0]))
# x = np.linspace(1,len(spec[0]),len(spec[0]))
# X, Y = np.meshgrid(x,y)
# ax.plot_surface(X,Y,Z,label='Savgol surface')
# ax.scatter(strongpoints[:,0],strongpoints[:,1],strongpoints[:,2],c='r',label='Strong freqs')
# ax.set_ylabel('Freq / Hz')
# ax.set_xlabel('Time sample (/10)')
# ax.set_zlabel('Power / dB')
# # ax.legend(loc='best')

#%% READ IN NOTE LIBRARY FROM TXT

notelib = pd.read_csv('note-lib.txt', sep="\s", header=None)
notelib.columns = ["Note", "Freq", "fmin", "fmax"]

#%% PASS FREQS THROUGH LIBRARY TO IDENTIFY NOTES



