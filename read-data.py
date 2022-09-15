# -*- coding: utf-8 -*-
"""
Created on Mon Aug 15 12:14:49 2022

@author: bamjoe

INSPIRED BY TUTORIAL BY MEDALLION DATA SCIENCE: https://www.youtube.com/watch?v=ZqpSb5p1xQo
"""

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

