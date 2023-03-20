# -*- coding: utf-8 -*-
"""
Created on Mon Feb  6 13:07:32 2023

@author: bamjo
"""

from tools import *
from pychord.analyzer import *
from pychord.quality import *
from pychord.constants.qualities import DEFAULT_QUALITIES


notes = ['C','E','G']

chord = str(pc.find_chords_from_notes(notes))

#%%

qm = QualityManager()

qls = qm.load_default_qualities()

rot = get_all_rotated_notes(notes)

pos = notes_to_positions(notes, notes[0])

quality = qm.find_quality_from_components(0, pos)

od = OrderedDict([(q, Quality(q, c)) for q, c in DEFAULT_QUALITIES])

# sus2 = Quality(('sus2', (0, 2, 7)))
