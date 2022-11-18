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

# --- math --------------------------------------------------------------------
TAU = 6.28

# --- draw transforms ---------------------------------------------------------
CX = PAGE_WIDTH / 2
CY = PAGE_HEIGHT / 2
SX = 1
SY = 1

# --- drawing config ----------------------------------------------------------
POLYSIDES = 6
EXT_WIDTH = (PAGE_WIDTH // 2) * 0.8
EXT_HEIGHT = (PAGE_HEIGHT // 2) * 0.8
STEP = 1

ARC = TAU / POLYSIDES
STEPS = 100

BORDER = [
    [CX-EXT_WIDTH, CY-EXT_HEIGHT],
    [CX+EXT_WIDTH, CY-EXT_HEIGHT],
    [CX+EXT_WIDTH, CY+EXT_HEIGHT],
    [CX-EXT_WIDTH, CY+EXT_HEIGHT],
    [CX-EXT_WIDTH, CY-EXT_HEIGHT]
]

CARDINAL = np.array([1,0])
PRECOMPUTED_DIRECTIONS = [
    np.matmul(np.array([
        [math.cos(ARC*t), -math.sin(ARC*t)],
        [math.sin(ARC*t),  math.cos(ARC*t)]
    ]), CARDINAL) for t in range(POLYSIDES)
]

def gen_walk(start_x, start_y):
    COORDS = [np.array([start_x, start_y])]
    pos = np.array([0,0])
    dir = random.randint(0, len(PRECOMPUTED_DIRECTIONS)-1)
    for i in range(STEPS):
        # random left/right choice
        dir += (random.randint(0,1) % 2)*2-1
        dir = dir % len(PRECOMPUTED_DIRECTIONS)
        # update position
        pos = np.add(pos, PRECOMPUTED_DIRECTIONS[dir]*STEP)
        # offset to actual position on paper (in mm)
        actual = np.add(pos, [start_x, start_y])
        COORDS.append(actual)
    return COORDS

def axi_draw(*paths):
    # --- init ----------------------------------------------------------------
    ad = axidraw.AxiDraw() # Initialize class
    ad.interactive()            # Enter interactive mode

    ad.options.speed_pendown = 40  # set pen-down speed to slow
    ad.options.units = 2           # Switch to mm units

    connected = ad.connect()    # Open serial port to AxiDraw
    if not connected:
        sys.exit() # end script

    # ad.update()                  # Process changes to options
    ad.moveto(0,0)                 # Pen-up return home

    # --- actual draw ---------------------------------------------------------
    for p in paths:
        ad.draw_path(p)

    # --- finit ---------------------------------------------------------------
    ad.moveto(0,0)              # Pen-up return home
    ad.disconnect()             # Close serial port to AxiDraw

# --- svg preview -------------------------------------------------------------
def svg_pointlist(points):
    return ' '.join([f"{p[0]},{p[1]}" for p in points])
    
def svg_preview(*paths):
    polylines = [f'<polyline points="{svg_pointlist(p)}" fill="none" stroke="black" stroke-width="0.2"/>' for p in paths]
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
            {polylines}
        </g>
        </svg>
        """
    with open('preview.svg','w') as fsvg:
        fsvg.write(svgout)

# --- main --------------
_wid = 10
_gap = 18
WALKS = [
    gen_walk(
        CX + (i % _wid - (_wid - 1) * 0.5) * _gap,
        CY + (i // _wid - (_wid - 1) * 0.5) * _gap
        ) 
        for i in range(100)
    ]
SPLITWALKS = []

# for each path, remove all segments that are out of our bounds (this may produce new paths)
for w in WALKS:
    _nwalk = []
    for seg in w:
        if ((seg >= [CX-EXT_WIDTH, CY-EXT_HEIGHT]) & (seg <= [CX+EXT_WIDTH, CY+EXT_HEIGHT])).all(axis=0):
            _nwalk.append(seg.tolist())
        elif len(_nwalk):
            SPLITWALKS.append(_nwalk)
            _nwalk = []
        else:
            continue
    SPLITWALKS.append(_nwalk)

# axi_draw(BORDER, *WALKS)
svg_preview(BORDER, *SPLITWALKS)
