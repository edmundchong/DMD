import getch
import os
import numpy as np
import matplotlib.pyplot as plt
import ALP
import Patterns
import time
import spot

#===initalize ALP===
ALP.init()
bitnum = 1L
picnum = 1L
stimon_time = 10000L
stimoff_time = 0L

seq_id=ALP.seq_alloc(bitnum,picnum)
ALP.seq_timing(seq_id, stimon_time, stimoff_time)

'''
gridsize=16
spot_loc = {'center':(3,2),
          'north': (4,2),
          'south': (2,2),
          'east': (3,1),
          'west': (3,3),
          'NW':   (4,3),
          'NE':   (4,1),
          'SW':   (2,3),
          'SE':   (2,1)}

'''
gridsize=8
spot_loc = {'center':(6,5),
          'north': (7,5),
          'south': (5,5),
          'east': (6,4),
          'west': (6,6),
          'NW':   (7,6),
          'NE':   (7,4),
          'SW':   (5,6),
          'SE':   (5,4)}

gridsize=4
spot_loc['center']=(12,10);
x=spot_loc['center'][0]
y=spot_loc['center'][1]
shift=1
spot_loc = {
          'north': (x+shift,y),
          'south': (x-shift,y),
          'east': (x,y-shift),
          'west': (x,y+shift),
          'NW':   (x+shift,y+shift),
          'NE':   (x+shift,y-shift),
          'SW':   (x-shift,y+shift),
          'SE':   (x-shift,y-shift)
          }



spots={}

for loc in spot_loc:
    s=spot.Spot('ALP')
    s.set_xy(spot_loc[loc], gridsize)
    spots[loc]=s.ptn


stimulated=spots['north']+spots['south']+spots['east']+spots['west']
ALP.stop()
ALP.seq_upload(seq_id, [stimulated])
ALP.seq_start(seq_id)
raw_input()

stimulated=spots['north']
ALP.stop()
ALP.seq_upload(seq_id, [stimulated])
ALP.seq_start(seq_id)
raw_input()

stimulated=spots['south']
ALP.stop()
ALP.seq_upload(seq_id, [stimulated])
ALP.seq_start(seq_id)
raw_input()

stimulated=spots['east']
ALP.stop()
ALP.seq_upload(seq_id, [stimulated])
ALP.seq_start(seq_id)
raw_input()

stimulated=spots['west']
ALP.stop()
ALP.seq_upload(seq_id, [stimulated])
ALP.seq_start(seq_id)
raw_input()



ALP.stop()
ALP.shutdown()



