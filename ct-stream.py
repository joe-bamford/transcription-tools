# -*- coding: utf-8 -*-
"""
Created on Thu Oct 13 11:24:02 2022

@author: bamjo

THIS IS A MODIFIED VERSION OF: https://www.youtube.com/watch?v=AShHJdSIxkY
"""

from tools import *
plt.close('all')

#%% SETUP

CHUNK = 2048
FORMAT = pa.paInt16
CHANNELS = 1
RATE = 44100

#%% BUILD STREAM

p = pa.PyAudio()
stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, output=True, frames_per_buffer=CHUNK)

#%% PLOT IN (ALMOST) REAL TIME

fig, ax = plt.subplots(3,1, figsize=(18,9), gridspec_kw=dict(height_ratios=[4,4,1]))
x = np.arange(0, 2*CHUNK, 2)
x_fft = np.linspace(0, RATE, CHUNK)

ts, = ax[0].plot(x, np.random.rand(CHUNK), '-', lw=2)
sp, = ax[1].semilogx(x_fft, np.random.rand(CHUNK), '-', lw=2)

# Time series
ax[0].set_title('Audio stream')
ax[0].set_ylim(-2**15, 2**15)
ax[0].set_xlim(0,CHUNK)
ax[0].set_xlabel('Samples')
ax[0].set_ylabel('Volume')

# Spectrum
ax[1].set_ylabel('Power')
ax[1].set_xlabel('Frequency')
ax[1].set_xlim(20, RATE/2)

# Chord display
ax[2].grid(False)
ax[2].axis('off')
text = ax[2].text(x=0.5, y=0, s='', verticalalignment='center', fontsize=30)

# For FPS calculation
start = time.time()
frames = 0

while True:
    # Time series
    data = stream.read(CHUNK)
    data_int = np.frombuffer(data, dtype=np.int16)
    ts.set_ydata(data_int)
    
    # Spectrum
    data_fft = fft(data_int)
    data_fft = np.abs(data_fft[0:CHUNK] / (128*CHUNK))**4
    # Normalise spectrum
    data_fft /= np.max(data_fft)
    sp.set_ydata(data_fft)
    
    # Get strong freqs
    peaks = sg.find_peaks(data_fft, prominence=0.3)[0].tolist()
    # Keep only the ones in audible range
    peaks = [i for i in peaks if i < 1024]
    notes = []
    # Convert to notes if not empty
    if peaks:
        notes = lb.hz_to_note(x_fft[peaks])
    
    # Convert to chord if enough notes
    if len(notes) >= 3:
        notes = [re.sub('[0-9]','',j) for j in notes]
        notes = [re.sub('♯','#',j) for j in notes]
        # Remove duplicate notes
        notes = list(dict.fromkeys(notes))
        chord = pc.find_chords_from_notes(notes, slash='n')
        text.remove()
        text = ax[2].text(x=0.5, y=0, s=re.sub('[<>]','',str(chord)), verticalalignment='center', horizontalalignment='center', fontsize=30)
    else:
        text.remove()
        text = ax[2].text(x=0.5, y=0, s=str(', '.join(notes)), verticalalignment='center', horizontalalignment='center', fontsize=30)
        
    # Draw all and update frame
    fig.canvas.draw()
    fig.canvas.flush_events()
    frames += 1
    q
    if kb.is_pressed('q'):
        print('\nExiting')
        plt.close('all')
        fps = frames / (time.time() - start)
        print('Avg. FPS = ', np.around(fps,0))
        break

#%%





















