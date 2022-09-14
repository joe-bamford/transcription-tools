# -*- coding: utf-8 -*-
"""
Created on Sun Aug 28 18:54:01 2022

@author: Joe
"""
#hi
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

#%%

class tools:
    
    # Get notes from freqs through the note library and add to freqdict
    def get_notes(freqdict, notelib):
        for key in freqdict:
            notes = []
            for freq in freqdict[key]['freqs']:
                r = notelib.index[0]
                match = False
                while not match:
                    if not notelib['fmin'][r] < freq < notelib['fmax'][r]:
                        r += 1
                    else:
                        note = notelib['Note'][r]
                        match = True
                notes.append(note)
            freqdict[key]['notes'] = notes
        return freqdict
    
    '''
    # Extract prominent datapoints from dicts (OUTDATED)
    def dic_to_coords(dic):
        filtvals = []
        for key in dic:
            j=0
            for j in range(len(dic[key])):
                coord = np.array([key,dic[key][j]])
                filtvals.append(coord)
            j+=1
        return np.array(filtvals)
    '''