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
#mpl.use("Qt5Agg")

#%% DEVICE SETUP

# def print_devices():
#     for n in range(pygame.midi.get_count()):
#         print (n,pygame.midi.get_device_info(n))

# pygame.midi.init()
# print_devices()

#%% STREAM

# Draw text to window
def draw_text(pos_x, pos_y, text, size):
    return ax.text(x=pos_x, y=pos_y, s=text, c='white', fontsize=size,
                   verticalalignment='center', horizontalalignment='center')
                    
# Stream
def read_input(input_device, fig, ax, main_text, sub_text, dev_id):
    
    main_text_fs = 170
    sub_text_fs = 100
    pressed = {'notes':[], 'nums':[]}
    while True:
        
        # Read changes from input device
        if input_device.poll():
            event = input_device.read(dev_id)[0]
            # print(event)
            data, timestamp = event[0], event[1]
            state, note_num = data[0], data[1]
            # Ignore pedal events (state 176)
            if state == 176:
                continue
            # Low note filter (for only picking up left hand)
            # if note_num > 67:
            #     continue
            
            note = tools.number_to_note(note_num)
            
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
                main_text.remove()
                sub_text.remove()
                main_text = draw_text(0.5, 0.6, note.replace('b', r'$^{\flat}$'), main_text_fs)
                sub_text = draw_text(0.5, 0.2, '', sub_text_fs)

            if len(pressed_notes) >= 3:
                global chords
                chords = tools.get_chords(pressed_notes)
                # Refresh display and print formatted chord names
                main_text.remove()
                sub_text.remove()
                main_text = draw_text(0.5, 0.6, tools.format_chord(chords[0]), main_text_fs)
                sub_text = draw_text(0.5, 0.2, tools.format_chord(chords[1]), sub_text_fs)
            
            # Or nothing, if no notes being played
            if not pressed_notes:
                time.sleep(0.1)
                main_text.remove()
                sub_text.remove()
                main_text = draw_text(0.5, 0.6, '', main_text_fs)
                sub_text = draw_text(0.5, 0.2, '', sub_text_fs)
        
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

# Execute
if __name__ == '__main__':
    
    # Initialise display
    fig, ax = plt.subplots(1,1, figsize=(18,10))
    ax.grid(False)
    ax.axis('off')
    fig.set_facecolor('black')
    main_text = draw_text(0.5, 0.6, '', 100)
    sub_text = draw_text(0.5, 0.2, '', 50)
    # Maximise figure window
    mng = plt.get_current_fig_manager()
    mng.window.state('zoomed')
    
    # Initialise pygame and call loop
    pg.midi.init()
    # EDIT THIS TO CHANGE INPUT DEVICE
    dev_id = 1
    read_input(pg.midi.Input(dev_id), fig, ax, main_text, sub_text, dev_id)
