#!/usr/bin/env python
# -*- encoding: utf-8 -#-
# https://axidraw.com/doc/py_api/
# https://github.com/evil-mad/axidraw
# http://axidraw.com/docs

import sys
import math
import time
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
X = 9
Y = 1
Z = 1

A = 99
B = 11 # was 11
C = 1

# scale and center
SX = 2
SY = 1
CX = 50
CY = 100

for i in range(3000):
    Y += X - (X * Z - Y) / A
    X += (Y - X) / B
    Z += X * Y / Z - C
    p = [X * SX + CX, Y * SY + CY]
    COORDS.append(p)

ad.draw_path(COORDS)

# --- finit -------------------------------------------------------------------
ad.moveto(0,0)              # Pen-up return home
ad.disconnect()             # Close serial port to AxiDraw
