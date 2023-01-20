# -*- coding: utf-8 -*-
"""
Created on Fri Jan 20 14:09:11 2023

@author: bamjo
"""

from tools import *
from itertools import combinations as comb

#%% FUNCS

# Build a 1D filter to remove combinations that contain an interval larger than
# a perfect 5th
def interval_filter(df, cols):
    
    # First get a boolean filter from each pair of cols
    intfilts = []
    for c in range(len(cols) - 1):
        intfilt = np.abs((df[c] - df[c+1])) < 7
        intfilts.append(intfilt)
        
    # Combine these into one series with the & operator
    while len(intfilts) > 1:
        intfilts[0] = intfilts[0] & intfilts[1]
        del intfilts[1]
    intfilt = intfilts[0]
    
    return intfilt
    

# Generate filtered array of possible combos for a given length
def n_groups(n, span):
    
    # Get combinations
    a = np.array(list(comb(span, n-1)))
    # Stack with zeros
    zeros = np.zeros(shape=(a.shape[0],1))
    a = np.hstack((zeros, a))
    # Convert to int
    a = np.array(a, dtype=int)
    
    # Convert to df
    df = pd.DataFrame(a)
    cols = df.columns
    
    # FILTERS
    
    # Cut out combinations that don't span at least a tritone
    span_filter = (df[cols[-1]] - df[cols[0]]) > 6
    df = df[span_filter]
    
    # Cut out combinations that contain an interval larger than a perfect 5th
    int_filter = interval_filter(df, cols)
    df = df[int_filter]
        
    return df, cols

# Generate combos over a range of lengths
def possible_qualities(span, nmin, nmax):
    
    quals = []
    for n in range(nmin, nmax+1):
        groups = n_groups(n, span)
        quals.append(groups)
        
    return quals

#%% EXECUTE

# Range of possible notes up to the 13th of the chord
space = np.arange(1,22,1)

df, cols = n_groups(4, space)
q = possible_qualities(space, nmin=3, nmax=7)




