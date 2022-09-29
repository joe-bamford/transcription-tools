# -*- coding: utf-8 -*-
"""
Created on Sun Aug 28 18:54:01 2022

@author: bamjoe
"""

#%% IMPORTS AND SETUP

import numpy as np
import seaborn as sb
import yellowbrick as sb
import librosa as lb
import math
import time
import glob
import scipy
from scipy import signal as sg
from scipy import optimize as opt
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pandas as pd
import librosa.display as lbd
from IPython.display import Audio
import pychord as pc

# Font and style
plt.rcParams.update({
    "text.usetex": False,
    "font.family": "serif",
    'font.size': 14,
    "font.sans-serif": ["Computer Modern Roman"]})

plt.rcParams['mathtext.fontset'] = 'cm'
plt.rcParams['mathtext.rm'] = 'Computer Modern Roman'
plt.rcParams['mathtext.it'] = 'Computer Modern Roman:italic'
plt.rcParams['mathtext.bf'] = 'Computer Modern Roman:bold'
plt.rcParams["axes.grid"] = True

#%% VARS

fft_sr = 20
sr = 22050
frdown = 27.5
frup = 5000

#%% FUNCS

class tools:
    
    # Read chord from chord_dict by sample no.
    def crd(cd, sample):
        if not sample in cd.keys():
            print(sample,': N/C')
        else:
            print(sample,': ',cd[sample]['chord'])

    # Get notes from freqs through librosa and add to freqdict
    def get_notes(freqdict):
        for key in freqdict:
            notes = []
            for freq in freqdict[key]['freqs']:
                note = lb.hz_to_note(freq)
                # Remove numbers from note names and replace sharp character with hash
                note = ''.join([i for i in note if not i.isdigit()]).replace('♯','#')
                # Ensure no duplicates
                if not note in notes:
                    notes.append(note)
                else:
                    continue
            freqdict[key]['notes'] = notes
        return freqdict
    
    # Get manual key input
    def get_key():        
        key = str(input('Enter key: ').upper())
        if 'M' in key:
            key = key.replace('M','')
            key = key+':min'
        else:
            key = key+':maj'
        return key
    
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
    
    
    # Get notes from freqs through the note library and add to freqdict (OUTDATED)
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
                        # note = lb.hz_to_note(freq)
                        # Remove numbers from note names and split at /
                        note = ''.join([i for i in note if not i.isdigit()]).split('/', 1)[0]
                        match = True
                # Ensure no duplicates
                if not note in notes:
                    notes.append(note)
                else:
                    continue
            freqdict[key]['notes'] = notes
        return freqdict
    '''