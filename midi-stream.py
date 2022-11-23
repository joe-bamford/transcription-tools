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

#%% DEVICE SETUP

# def print_devices():
#     for n in range(pygame.midi.get_count()):
#         print (n,pygame.midi.get_device_info(n))

# pygame.midi.init()
# print_devices()

#%% STREAM
        
def number_to_note(number):
    
    notes = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']
    # In case you prefer sharps (weirdo)
    # notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    return notes[number % 12]

def format_chord(chord):
    
    fmt_dict = {'(':r'$^($',
                ')':r'$^)$',
                'b':r'$^{\flat}$',
                '#':r'$^{\sharp}$',
                '°':r'$^{\mathrm{o}}$',
                'ø':r'$^{\o}$',
                '7':r'$^7$',
                '△':r'$\Delta$',
                'sus':r'$^{\mathrm{sus}}$',
                'add':r'$^{\mathrm{add}}$',
                'dim':r'$^{\mathrm{dim}}$',
                'omit':r'$^{\mathrm{omit}}$',
                '2':r'$^2$',
                '4':r'$^4$',
                '5':r'$^5$',
                '6':r'$^6$',
                '9':r'$^9$',
                '11':r'$^{11}$',
                '13':r'$^{13}$'}
    
    if not chord == '':
        
        # Remove junk
        chord = re.sub(r'[<>]|[\[\]]','',chord)
        chord = chord.replace('Chord: ','')
        for key in fmt_dict:
            # Ignore already replaced substrings
            if str(fmt_dict[key]) in chord:
                continue
            # Replace ones not yet done
            if str(key) in chord:
                chord = chord.replace(key, fmt_dict[key])                
    return chord

def read_input(input_device, fig, ax, text, dev_id):
    
    pressed = {'notes':[], 'nums':[]}
    while True:
        
        # Read changes from input device
        if input_device.poll():
            event = input_device.read(dev_id)[0]
            data, timestamp = event[0], event[1]
            state, note_num = data[0], data[1]
            note = number_to_note(note_num)
            
            # Keep track of notes pressed down
            # Press event (state 144)
            if state == 144:
                if not note_num in pressed['nums']:
                    pressed['notes'].append(note)
                    pressed['nums'].append(note_num)
            # Release event (state 128)
            if state == 128:
                if note_num in pressed['nums']:
                    pressed['notes'].remove(note)
                    pressed['nums'].remove(note_num)
            
            # Rotate pressed notes until lowest is first (avoids unnecessary slashes)
            if pressed['nums']:
                while not np.min(pressed['nums']) == pressed['nums'][0]:
                    pressed['nums'] = pressed['nums'][1:] + pressed['nums'][:1]
                    pressed['notes'] = pressed['notes'][1:] + pressed['notes'][:1]
         
            # Give pychord a copy of list of notes pressed, with duplicates removed
            pressed_notes = list(dict.fromkeys(pressed['notes']))
            # Display either single note or chord
            if len(pressed_notes) == 1:
                text.remove()
                text = ax.text(x=0.5, y=0.5, s=note.replace('b', r'$^{\flat}$'), verticalalignment='center', horizontalalignment='center', fontsize=130)
            if len(pressed_notes) >= 3:
                chord = tools.get_chord(pressed_notes)
                # Refresh display and print formatted chord name
                text.remove()
                text = ax.text(x=0.5, y=0.5, s=format_chord(chord), verticalalignment='center', horizontalalignment='center', fontsize=130)
            
            # Or nothing, if no notes being played
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
    read_input(pg.midi.Input(dev_id), fig, ax, text, dev_id)