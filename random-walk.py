#!/usr/bin/env python
# -*- encoding: utf-8 -#-
# https://axidraw.com/doc/py_api/
# https://github.com/evil-mad/axidraw
# http://axidraw.com/docs

import sys
import math
import random
import time
import numpy as np
from pyaxidraw import axidraw

# --- boilerplate -------------------------------------------------------------
ad = axidraw.AxiDraw() # Initialize class

ad.interactive()            # Enter interactive mode
connected = ad.connect()    # Open serial port to AxiDraw

if not connected:
    sys.exit() # end script

ad.options.speed_pendown = 40  # set pen-down speed to slow
ad.options.units = 2           # Switch to mm units
ad.update()                    # Process changes to options

ad.moveto(0,0)                 # Pen-up return home
# --- end boilerplate ---------------------------------------------------------

# lorenz from https://github.com/ubilabs/axidraw/blob/master/src/draw-lorenz.js
COORDS = []
TAU = 6.28

# scale and center
SX = 1
SY = 1
CX = 170
CY = 100

EXTENT = 100
ARC = TAU * 0.125

pos = np.array([0,0])
dir = np.array([1,0])

for i in range(2000):
    # random left/right choice
    sign = (random.randint(0,1) % 2)*2-1
    # rotate feeler
    mrot = np.array([
        [math.cos(ARC * sign), -math.sin(ARC * sign)],
        [math.sin(ARC * sign),  math.cos(ARC * sign)]
        ])
    dir = np.matmul(mrot, dir)
    # update position (clipped to EXTENT)
    pos = np.add(pos, dir)
    pos = np.clip(pos, -EXTENT, EXTENT)
    # find position on paper (in mm)
    actual = np.add(pos, [CX, CY])
    COORDS.append(actual.tolist())

ad.draw_path(COORDS)

# --- finit -------------------------------------------------------------------
ad.moveto(0,0)              # Pen-up return home
ad.disconnect()             # Close serial port to AxiDraw
