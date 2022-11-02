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
    
    notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    return notes[number % 12]

def readInput(input_device, fig, ax, text):
    
    pressed = []
    while True:
        
        if input_device.poll():
            event = input_device.read(dev_id)[0]
            data = event[0]
            timestamp = event[1]
            note_num = data[1]
            note = number_to_note(note_num)
            
            if data[0] == 144:
                state = 'P'
                if not note in pressed:
                    pressed.append(note)               
            if data[0] == 128:
                state = 'R'
                if note in pressed:
                    pressed.remove(note)

            
            if len(pressed) == 1:
                text.remove()
                text = ax.text(x=0.5, y=0.5, s=note, verticalalignment='center', horizontalalignment='center', fontsize=100)
            if len(pressed) >= 3:
                chord = pc.find_chords_from_notes(pressed, slash='n')
                if type(chord) is None:
                    chord = pc.find_chords_from_notes(pressed, slash=pressed[0])
                text.remove()
                text = ax.text(x=0.5, y=0.5, s=re.sub('[<>]','',str(chord)), verticalalignment='center', horizontalalignment='center', fontsize=100)

        fig.canvas.draw()
        fig.canvas.flush_events()
    
        if kb.is_pressed('esc'):
            print('\nExiting')
            plt.close('all')
            break
        
    pg.midi.Input.close
    # Restart kernel to refresh device IDs
    os._exit(00)

if __name__ == '__main__':
    
    fig, ax = plt.subplots(1,1, figsize=(10,5))
    # Chord display
    ax.grid(False)
    ax.axis('off')
    text = ax.text(x=0.5, y=0.5, s='play some shi', verticalalignment='center', horizontalalignment='center', fontsize=100)
    
    pg.midi.init()
    dev_id = 1
    readInput(pg.midi.Input(dev_id), fig, ax, text)