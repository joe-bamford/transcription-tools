# -*- coding: utf-8 -*-
"""
Created on Mon Aug 15 12:14:49 2022

@author: bamjo

FOLLOWS TUTORIAL BY MEDALLION DATA SCIENCE: https://www.youtube.com/watch?v=ZqpSb5p1xQo
"""

#%% IMPORTS

import numpy as np
import seaborn as sb
import yellowbrick as sb
import librosa as lb
import time
import glob
import matplotlib.pyplot as plt
import pandas as pd
import librosa.display as lbd

#%% READ FILE

data = 'data/test.wav'
y, sr = lb.load(data)
y = y[60000:100000]

#%% PLOT TIME SERIES

raw_ts = plt.figure(figsize=(15,10))
plt.title('Raw time series')
plt.xlabel('Sample')
plt.plot(y, lw=1)

#%% FFT

spec = np.abs(lb.stft(y))
spec_db = lb.amplitude_to_db(spec, ref=np.max(spec))

#%% PLOT FFT

abs_spec, ax = plt.subplots(figsize=(15,10))
specplot = lb.display.specshow(spec_db,x_axis='time',y_axis='log',ax=ax)

#%%

plt.plot(spec[:,0])
