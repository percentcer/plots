#!/usr/bin/env python
# -*- encoding: utf-8 -#-

# https://axidraw.com/doc/py_api/
# https://github.com/evil-mad/axidraw
# http://axidraw.com/docs

import sys
import math
import random
import numpy as np
from pyaxidraw import axidraw

# --- page setup (mm) ---------------------------------------------------------
PAGE_WIDTH = 350
PAGE_HEIGHT = 250
PAGE_MARGIN = 5
# -----------------------------------------------------------------------------

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
TAU = 6.28

# scale and center
CX = PAGE_WIDTH / 2
CY = PAGE_HEIGHT / 2
SX = 1
SY = 1

POLYSIDES = 6
EXTENT = 80
STEP = 2

ARC = TAU / POLYSIDES
STEPS = 3000

BORDER = [
    [CX-EXTENT, CY-EXTENT],
    [CX+EXTENT, CY-EXTENT],
    [CX+EXTENT, CY+EXTENT],
    [CX-EXTENT, CY+EXTENT],
    [CX-EXTENT, CY-EXTENT]
]
COORDS = []

pos = np.array([0,0])
dir = np.array([1,0])
for i in range(STEPS):
    # random left/right choice
    sign = (random.randint(0,1) % 2)*2-1
    # rotate feeler
    mrot = np.array([
        [math.cos(ARC * sign), -math.sin(ARC * sign)],
        [math.sin(ARC * sign),  math.cos(ARC * sign)]
        ])
    dir = np.matmul(mrot, dir)
    # update position (clipped to EXTENT)
    pos = np.add(pos, dir*STEP)
    pos = np.clip(pos, -EXTENT, EXTENT)
    # find position on paper (in mm)
    actual = np.add(pos, [CX, CY])
    COORDS.append(actual.tolist())

ad.draw_path(BORDER)
ad.draw_path(COORDS)

# # --- finit -------------------------------------------------------------------
ad.moveto(0,0)              # Pen-up return home
ad.disconnect()             # Close serial port to AxiDraw
# # --- finit -------------------------------------------------------------------

# --- svg write ---------------------------------------------------------------
def ptext(points):
    return ' '.join([f"{p[0]},{p[1]}" for p in points])

svgout = f"""<?xml version="1.0" encoding="UTF-8" standalone="no"?>
    <svg
        xmlns:dc="http://purl.org/dc/elements/1.1/"
        xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
        xmlns:svg="http://www.w3.org/2000/svg"
        xmlns="http://www.w3.org/2000/svg"
        version="1.1"
        id="test"
        viewBox="0 0 {PAGE_WIDTH + PAGE_MARGIN * 2} {PAGE_HEIGHT + PAGE_MARGIN * 2}"
        height="{PAGE_HEIGHT + PAGE_MARGIN * 2}mm"
        width="{PAGE_WIDTH + PAGE_MARGIN * 2}mm">
      <g transform="translate({PAGE_MARGIN},{PAGE_MARGIN})">
        <rect fill="none" stroke="blue" stroke-width="0.2" width="{PAGE_WIDTH}" height="{PAGE_HEIGHT}"/>
        <polyline points="{ptext(COORDS)}" fill="none" stroke="black" stroke-width="0.2"/>
        <polyline points="{ptext(BORDER)}" fill="none" stroke="black" stroke-width="0.2"/>
      </g>
    </svg>
    """
with open('preview.svg','w') as fsvg:
    fsvg.write(svgout)
# --- end svg write -----------------------------------------------------------
