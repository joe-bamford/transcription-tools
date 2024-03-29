# -*- coding: utf-8 -*-
"""
Created on Fri Jan 20 14:09:11 2023

An outdated attempt to find every playable 3-note and 4-note chord in terms of note numbers.

@author: bamjo
"""

from tools import *
from itertools import combinations as combos

#%% FUNCS

# Get count of False values by row and add to new col
def bool_count(df):
    for i in df.index:
        row = df.loc[i, :]
        count = np.sum(row == False)
        df.loc[i, 'tot'] = count
    return df

# Combine a list of series together via AND operation
def combine_series_and(inlist):
    while len(inlist) > 1:
        inlist[0] = inlist[0] & inlist[1]
        del inlist[1]
    outseries = inlist[0]
    return outseries

# Combine a list of series together via OR operation
def combine_series_or(inlist):
    while len(inlist) > 1:
        inlist[0] = inlist[0] | inlist[1]
        del inlist[1]
    outseries = inlist[0]
    return outseries


# Build a 1D filter to remove combinations that contain an interval larger than
# a perfect 5th
def interval_filter(df, cols):
    # First get a boolean filter from each pair of cols
    intfilts = []
    for c in range(len(cols) - 1):
        # Check each interval
        intfilt = np.abs((df[c] - df[c+1])) < 7
        intfilts.append(intfilt)
    # Combine and return
    return combine_series_and(intfilts)


# Build a 1D filter to remove combinations containing 2 or more semitone intervals
def semitones_filter(df, cols):
    # First get a boolean filter from each pair of cols
    stfilts = pd.DataFrame()
    for c in range(len(cols) - 1):
        # Check each interval
        stfilt = np.abs(df[c] - df[c+1]) >= 2
        stfilts[c] = stfilt
    # Count number of semitone intervals per row
    global stf
    stf = bool_count(stfilts)
    # Filter rows where there are leq 1
    global st_filter
    st_filter = stf['tot'] <= 1
    return st_filter


def octave_filter(df, cols):
    oct_filter = []
    for c in cols:
        ofilts = []
        for i in [j for j in cols if j > c]:
            ofilt = np.abs(df[c] - df[i]) == 12
            ofilts.append(ofilt)
        if ofilts:
            # Inner combine
            oct_filter.append(combine_series_or(ofilts))
    # Combine and return
    return ~combine_series_or(oct_filter)
    

# Generate filtered array of possible combos for a given length
def n_groups(n, span):
    # Get combinations
    a = np.array(list(combos(span, n-1)))
    # Stack with zeros
    zeros = np.zeros(shape=(a.shape[0],1))
    a = np.hstack((zeros, a))
    # Convert to int
    a = np.array(a, dtype=int)
    # Convert to df
    df = pd.DataFrame(a)
    cols = df.columns
    
    # FILTERS
    # Cut out combinations that don't span at least a tritone (clusters)
    span_filter = (df[cols[-1]] - df[cols[0]]) >= 6
    df = df[span_filter]
    # Cut out combinations that contain an interval larger than a perfect 5th
    # (stretches)
    int_filter = interval_filter(df, cols)
    df = df[int_filter]
    # Cut out combinations that contain more than one minor 2nd interval
    # (clusters / stretched clusters)
    st_filter = semitones_filter(df, cols)
    df = df[st_filter]
    # Cut out combinations containing octave intervals (dupe notes)
    oct_filter = octave_filter(df, cols)
    df = df[oct_filter]
    return df, cols

# Generate combos over a range of lengths
def possible_qualities(span, nmin, nmax):   
    quals = []
    for n in range(nmin, nmax+1):
        groups = n_groups(n, span)
        quals.append(groups)
    return [frame for (frame, idx) in quals]

# Cast output to format in qualities file
def format_result(df):
    out_list = []
    for i in df.index:
        row = str(df.loc[i, :].tolist())
        row = row.replace('[','(').replace(']',')')
        # print('("",',row,')')
        out_list.append('("",'+row+'),')
    return out_list
    

#%% EXECUTE

start = time.time()

# Range of possible notes up to the 13th of the chord
space = np.arange(1,22,1)

df, cols = n_groups(4, space)
# q = possible_qualities(space, nmin=3, nmax=7)
out = format_result(df)

end = time.time()
runtime = end - start
print(runtime)

#%% TESTING CELL

idxs = [i for i in df.index if i < 76]
df2 = df.loc[idxs,:]
a=octave_filter(df, cols)




