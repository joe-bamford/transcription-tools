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
    return ax.text(x=pos_x, y=pos_y, s=text, c='white', fontsize=size, verticalalignment='center', horizontalalignment='center')

# Rotate lists within dict
def rotate_lists(dct, cols):
    for col in cols:
        dct[col] = dct[col][1:] + dct[col][:1]
    return dct

# # Save recording file as csv
# def save_recording(dct):
#     save_path = os.getcwd().replace('\\','/') + '/recordings/'
#     save_str = save_path + str(dt.date.today()) + str(int(np.around(time.time(),0))) + '.csv'
#     df = pd.DataFrame(data=dct)
#     df.to_csv(save_str, index=False, encoding='utf-8-sig')
                    
# Stream
def read_input(input_device, fig, ax, main_text, sub_text, dev_id):
    
    def play(part, num, note_dur):
        part.play_note(num, volume=0, length=note_dur)
    
    main_text_fs = 170
    sub_text_fs = 100
    start_time = time.time()
    pressed = {'notes':[], 'nums':[], 'keys':[]}
    # recording = {'time':[], 'note':[], 'event':[]}
    
    s = scamp.Session()
    s.tempo = 120 #BPM
    quantization_simplicity = 4
    piano = s.new_part('piano')
    # Move this to avoid gap at start?
    s.start_transcribing()

    # event_ts = 0.0
    global events
    events = pd.DataFrame(columns=['Timestamp', 'Note', 'Event'])
    # i=0

    while True:
        
        # Read changes from input device
        if input_device.poll():
            # Log event timestamp
            # last_event_ts = event_ts
            # event_time = time.time()
            # event_ts = np.around(event_time - start_time, 3)
            # event_gap = event_ts - last_event_ts
            # Read event data
            event = input_device.read(dev_id)[0]
            data, timestamp = event[0], event[1]
            state, note_num = data[0], data[1]
            event = pd.DataFrame({'Timestamp':[timestamp], 'Note':[note_num], 'Event':[state]})
            events = pd.concat([events, event], ignore_index=True)
            # Map to 88-key layout
            key_num = note_num - 20
            # Ignore pedal events (state 176)
            if state == 176:
                continue
            # Low note filter (for only picking up left hand - 67 is G4)
            # if note_num > 67:
            #     continue
            
            # Convert note number to note
            note = tools.number_to_note(note_num)
            
            # Keep track of notes pressed down
            # Press event (state 144)
            if state == 144:
                if not note_num in pressed['nums']:
                    # Append to pressed
                    pressed['notes'].append(note)
                    pressed['nums'].append(note_num)
                    pressed['keys'].append(key_num)
                    
            # Release eveqnt (state 128)
            if state == 128:
                if note_num in pressed['nums']:
                    # Remove from pressed
                    pressed['notes'].remove(note)
                    pressed['nums'].remove(note_num)
                    pressed['keys'].remove(key_num)
                    # Find corresponding press event to calculate note duration
                    note_filter = (events['Note'] == note_num) & (events['Event'] == 144)
                    last_press_ts = events.loc[events[note_filter].index[-1], 'Timestamp']                                                                    
                    # Find note length in beats
                    note_length = (timestamp - last_press_ts)/1e3 * s.tempo/60
                    piano.play_note(note_num, volume=1, length=note_length)
                    # s.fork(play, args=[piano, note_num, note_length])
                    # s.wait_forever()
                    
            # Rotate pressed notes until lowest is first (avoids unnecessary slashes)
            if pressed['nums']:
                while not np.min(pressed['nums']) == pressed['nums'][0]:
                    pressed = rotate_lists(pressed, ['notes','nums','keys'])
            
            # print(event)
            # print(pressed)
            # print((pressed['time'], pressed['keys']))
            
            # Give pychord a copy of list of notes pressed, with duplicates removed
            pressed_notes = list(dict.fromkeys(pressed['notes']))
            # Display either single note or chord
            if len(pressed_notes) == 1:
                main_text.remove()
                sub_text.remove()
                main_text = draw_text(0.5, 0.6, note.replace('b', r'$^{\flat}$'), main_text_fs)
                sub_text = draw_text(0.5, 0.2, '', sub_text_fs)

            if len(pressed_notes) >= 3:
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
        # i+=1
        
        # Escape condition
        if kb.is_pressed('esc'):
            print('\nExiting')
            plt.close('all')
            # if save_record:
            #     save_recording(recording)
            break
    
    print(events)
    pg.midi.Input.close
    s.stop_transcribing().to_score(title='Test', composer='J.B.', simplicity_preference=quantization_simplicity).show_xml()
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
    dev_id = 1
    # save_record = True
    read_input(pg.midi.Input(dev_id), fig, ax, main_text, sub_text, dev_id)
