# -*- coding: utf-8 -*-
"""
Created on Mon Aug 15 12:14:49 2022

@author: bamjo

INSPIRED BY TUTORIAL BY MEDALLION DATA SCIENCE: https://www.youtube.com/watch?v=ZqpSb5p1xQo
"""

#%% IMPORTS

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

#%% READ FILE

data = 'data/matilda.wav'
raw, sr = lb.load(data)
# raw = raw[10000:20000]
# compress raw time series
raw = raw[::5]

#%% PLOT TIME SERIES

raw_ts = plt.figure(figsize=(15,10))
plt.title('Raw time series')
plt.xlabel('Sample')
plt.plot(raw, lw=1)

#%% COMPUTE FFT AND SAVE RAW SPECTROGRAM TO CSV

# spec = np.abs(lb.stft(raw, hop_length = 20))
# specframe = pd.DataFrame(spec)
# specframe.to_csv('matilda-spec.csv')

#%% COMPUTE MELODIC SPECTROGRAM AND SAVE TO CSV

melspec = lb.feature.melspectrogram(y=raw, sr=sr, fmin=27, fmax=4200, n_mels=88)
melspecframe = pd.DataFrame(melspec)
melspecframe.to_csv('data/matilda-melspec.csv')

#%%

# abs_spec, ax = plt.subplots(figsize=(15,10))
# specplot = lb.display.specshow(spec_db,x_axis='time',y_axis='log',ax=ax)
# abs_spec.colorbar(specplot, ax=ax)

# #%% FIND PEAK FREQS WITH SAVGOL FILTER

# #spectrum with max value = 961

# subsamples = np.arange(0, len(spec_db[0]), 100)
# savgols = np.zeros_like(spec_db)
# sps = {}
# pkp = {}
# i=0
# for sample in subsamples:

#     sp = spec_db[:,sample]
#     savgol = sg.savgol_filter(sp,1025,9)
#     # bodge to fix mid-window filter spike
#     savgol[512] = 0.5*(savgol[511]+savgol[513])
#     peaks = sg.find_peaks(sp,prominence=20)[0]
#     peakvals = sp[peaks]
    
#     peakpowers =[]
#     strongpeaks = []
#     for peak in peaks:
#         if sp[peak] - savgol[peak] >= 20:
#             strongpeaks.append(peak)
#             peakpowers.append(sp[peak])
            
#     savgols[:,i] = savgol
#     # check if list not empty and if so dump into dict
#     if strongpeaks:     
#         sps[i] = strongpeaks
#         pkp[i] = peakpowers
#     i+=1

# # build array of 3-vectors for strong peaks
# filt2d = dic_to_coords(sps)
# filtpowers = dic_to_coords(pkp)
# strongpoints = np.hstack((filt2d, filtpowers))
# strongpoints = np.delete(strongpoints, 2, axis=1)

# #%% PLOT ANY SPECTRUM

# s = int(input('Spectrum to plot (0-'+str(len(subsamples)-1)+'): '))
# sp = spec_db[:,s]

# specfig = plt.figure(figsize=(12,8))
# plt.plot(sp, label='Spectrum')
# plt.plot(savgols[:,s], label='Savgol filter')
# plt.legend(loc='best')
# plt.xlabel('Freq / Hz')
# plt.ylabel('dB')
# plt.scatter(sps[s], sp[sps[s]],c='r')

# #%% 3D SAVGOL PLOT

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

