#!/usr/bin/env python
# -*- encoding: utf-8 -#-

# https://axidraw.com/doc/py_api/
# https://github.com/evil-mad/axidraw
# http://axidraw.com/docs

import sys
import math
import random
import numpy as np

from common.math import TAU
from common.page import PAGE_WIDTH, PAGE_HEIGHT, PAGE_MARGIN
from common.svg import svg_preview

# --- math --------------------------------------------------------------------
TAU = 6.28

# --- draw transforms ---------------------------------------------------------
CX = PAGE_WIDTH / 2
CY = PAGE_HEIGHT / 2
SX = 1
SY = 1

# --- drawing config ----------------------------------------------------------
POLYSIDES = 6
EXTENT = 100
STEP = 1

ARC = TAU / POLYSIDES
STEPS = 3000

BORDER = [
    [CX-EXTENT, CY-EXTENT],
    [CX+EXTENT, CY-EXTENT],
    [CX+EXTENT, CY+EXTENT],
    [CX-EXTENT, CY+EXTENT],
    [CX-EXTENT, CY-EXTENT]
]

CARDINAL = np.array([1,0])
PRECOMPUTED_DIRECTIONS = [
    np.matmul(np.array([
        [math.cos(ARC*t), -math.sin(ARC*t)],
        [math.sin(ARC*t),  math.cos(ARC*t)]
    ]), CARDINAL) for t in range(POLYSIDES)
]

def gen_walk(start_x, start_y):
    COORDS = [[start_x, start_y]]
    pos = np.array([0,0])
    dir = random.randint(0, len(PRECOMPUTED_DIRECTIONS)-1)
    for i in range(STEPS):
        # random left/right choice
        dir += (random.randint(0,1) % 2)*2-1
        dir = dir % len(PRECOMPUTED_DIRECTIONS)
        # update position (clipped to EXTENT)
        pos = np.add(pos, PRECOMPUTED_DIRECTIONS[dir]*STEP)
        pos = np.clip(pos, -EXTENT, EXTENT)
        # find position on paper (in mm)
        actual = np.add(pos, [start_x, start_y])
        COORDS.append(actual.tolist())
    return COORDS

# --- svg preview -------------------------------------------------------------
def svg_ptext(points):
    return ' '.join([f"{p[0]},{p[1]}" for p in points])
    
def svg_preview(*paths):
    polylines = [f'<polyline points="{svg_ptext(p)}" fill="none" stroke="black" stroke-width="0.2"/>' for p in paths]
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
WALK = gen_walk(CX,CY)
# axi_draw_paths(BORDER, WALK)
svg_preview(BORDER, WALK)
