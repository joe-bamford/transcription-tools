# -*- coding: utf-8 -*-
"""
Created on Sun Aug 28 18:54:01 2022

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

#%%

class tools:
    
    # Extract prominent datapoints from dicts
    def dic_to_coords(dic):
        filtvals = []
        for key in dic:
            j=0
            for j in range(len(dic[key])):
                coord = np.array([key,dic[key][j]])
                filtvals.append(coord)
            j+=1
        return np.array(filtvals)