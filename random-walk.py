#!/usr/bin/env python
# -*- encoding: utf-8 -#-

# https://axidraw.com/doc/py_api/
# https://github.com/evil-mad/axidraw
# http://axidraw.com/docs

import math
import random
import numpy as np

from common.math import TAU
from common.page import PAGE_WIDTH, PAGE_HEIGHT
from common.axidraw import axi_draw_svg
from common.svg import svg_polylines, svg_doc, svg_rects, svg_write

# --- draw transforms ---------------------------------------------------------
CX = PAGE_WIDTH / 2
CY = PAGE_HEIGHT / 2
SX = 1
SY = 1

# --- drawing config ----------------------------------------------------------
EXT = 100

POLYSIDES = 6
STEP = 1

ARC = TAU / POLYSIDES
STEPS = 3000

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
    for _ in range(STEPS):
        # random left/right choice
        dir += random.randint(0,1)*2-1
        dir = dir % len(PRECOMPUTED_DIRECTIONS)
        # update position (clipped to EXTENT)
        pos = np.add(pos, PRECOMPUTED_DIRECTIONS[dir]*STEP)
        pos = np.clip(pos, -EXT, EXT)
        # find position on paper (in mm)
        actual = np.add(pos, [start_x, start_y])
        COORDS.append(actual.tolist())
    return COORDS

# --- main --------------
WALK = svg_polylines(gen_walk(CX,CY))
BORDER = svg_rects([CX-EXT, CY-EXT, EXT*2, EXT*2])
doc = svg_doc(*BORDER, *WALK)

svg_write(doc)
# axi_draw_svg(doc)
