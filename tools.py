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
import re

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

pd.set_option('mode.chained_assignment', None)

#%% VARS

fft_sr = 20
sr = 22050
frdown = 27.5
frup = 5000

#%% FUNCS

class tools:
    
    # Read chord from chord_dict by sample no.
    def crd(cd: dict, sample: int) -> print:
        if not sample in cd.keys():
            print(sample,': N/C')
        else:
            print(sample,': ',cd[sample]['chord'])
            
            
    # Get notes from freqs through librosa and add to dataframe
    def get_notes(df: pd.DataFrame()) -> pd.DataFrame:
        notes_col = []
        for i in df.index:
            notes = lb.hz_to_note(df['Freqs'][i])
            # Remove numbers from note names and replace sharp character with hash
            notes = [re.sub('[0-9]','',j) for j in notes]
            notes = [re.sub('♯','#',j) for j in notes]
            # Remove duplicate notes
            notes = list(dict.fromkeys(notes))
            notes_col.append(notes)
        df['Notes'] = notes_col
        return df
    
    
    # Get chords from notes through pychord and add to dataframe
    def get_chords(df: pd.DataFrame(), force_slash: bool) -> pd.DataFrame:
        chords_col = []
        for i in df.index:
            notes = df.at[i,'Notes']
            if force_slash == False:
                chord = pc.find_chords_from_notes(notes, slash='n')
            else:
                chord = pc.find_chords_from_notes(notes[1:], slash=notes[0])
            chords_col.append(chord)
        df['Chord'] = chords_col
        return df


    # # Get notes from freqs through librosa and add to freqdict
    # def get_notes(freqdict):
    #     for key in freqdict:
    #         notes = []
    #         for freq in freqdict[key]['freqs']:
    #             note = lb.hz_to_note(freq)
    #             # Remove numbers from note names and replace sharp character with hash
    #             note = ''.join([i for i in note if not i.isdigit()]).replace('♯','#')
    #             # Ensure no duplicates
    #             if not note in notes:
    #                 notes.append(note)
    #             else:
    #                 continue
    #         freqdict[key]['notes'] = notes
    #     return freqdict
    
    
    # Get manual key input
    def get_key() -> str:        
        key = str(input('Enter key: ').upper())
        # if type(key) is None:
        #     print('none')
        #     key = 'C'
        if 'M' in key:
            key = key.replace('M','')
            key = key+':min'
        else:
            key = key+':maj'
        return key
