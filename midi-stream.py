# -*- coding: utf-8 -*-
"""
Created on Wed Nov  2 11:40:45 2022

@author: bamjo

Adapted from code written by stack overflow users Fusselgesicht and Etiaro:
https://stackoverflow.com/questions/15768066/reading-piano-notes-on-python
https://stackoverflow.com/questions/67642570/pygame-midi-how-to-detect-simultaneous-inputs-from-a-synthesizer
"""

from tools import *
plt.close('all')

#%%
        
def number_to_note(number):
    
    notes = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']
    # Would prefer to use flats personally but pychord is built to use sharps
    # notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    return notes[number % 12]

def readInput(input_device, fig, ax, text, dev_id):
    
    pressed = {'notes':[], 'nums':[]}
    while True:
        
        # Read changes from input device
        if input_device.poll():
            event = input_device.read(dev_id)[0]
            data = event[0]
            timestamp = event[1]
            note_num = data[1]
            note = number_to_note(note_num)
            
            # Keep track of notes pressed down
            # Press event (state 144)
            if data[0] == 144:
                state = 'P'
                if not note_num in pressed['nums']:
                    pressed['notes'].append(note)
                    pressed['nums'].append(note_num)
            # Release event (state 128)
            if data[0] == 128:
                state = 'R'
                if note_num in pressed['nums']:
                    pressed['notes'].remove(note)
                    pressed['nums'].remove(note_num)
            
            # Rotate pressed notes until lowest is first (avoids unnecessary slashes)
            if pressed['nums']:
                while not np.min(pressed['nums']) == pressed['nums'][0]:
                    pressed['nums'] = pressed['nums'][1:] + pressed['nums'][:1]
                    pressed['notes'] = pressed['notes'][1:] + pressed['notes'][:1]
         
            print(pressed)
            # Give pychord a copy of list of notes pressed, with duplicates removed
            pressed_notes = list(dict.fromkeys(pressed['notes']))
            # Display either single note or chord
            if len(pressed_notes) == 1:
                text.remove()
                text = ax.text(x=0.5, y=0.5, s=note, verticalalignment='center', horizontalalignment='center', fontsize=120)
            if len(pressed_notes) >= 3:
                chord = pc.find_chords_from_notes(pressed_notes, slash='n')
                if not chord:
                    chord = pc.find_chords_from_notes(pressed_notes, slash=pressed_notes[0])
                if not chord:
                    chord = '404: chord not found'
                text.remove()
                text = ax.text(x=0.5, y=0.5, s=re.sub(r'[<>]|[\[\]]','',str(chord).split(',')[0]), 
                               verticalalignment='center', horizontalalignment='center', fontsize=110)
            # Or nothing
            if not pressed_notes:
                time.sleep(0.1)
                text.remove()
                text = ax.text(x=0.5, y=0.5, s='', verticalalignment='center', horizontalalignment='center', fontsize=110)
        
        # Draw and refresh
        fig.canvas.draw()
        fig.canvas.flush_events()
        
        # Escape condition
        if kb.is_pressed('esc'):
            print('\nExiting')
            plt.close('all')
            break
        
    pg.midi.Input.close
    # Restart kernel to refresh device IDs
    os._exit(00)

if __name__ == '__main__':
    
    # Initialise display
    fig, ax = plt.subplots(1,1, figsize=(18,10))
    ax.grid(False)
    ax.axis('off')
    text = ax.text(x=0.5, y=0.5, s='play me summin real nice', verticalalignment='center', horizontalalignment='center', fontsize=80)
    
    # Initialise pygame and call loop
    pg.midi.init()
    dev_id = 1
    readInput(pg.midi.Input(dev_id), fig, ax, text, dev_id)