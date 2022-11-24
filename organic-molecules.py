#!/usr/bin/env python
# -*- encoding: utf-8 -#-

# https://axidraw.com/doc/py_api/
# https://github.com/evil-mad/axidraw
# http://axidraw.com/docs

import math
import random
import numpy as np

from common.axidraw import axi_draw_svg
from common.math import TAU
from common.page import PAGE_WIDTH, PAGE_HEIGHT
from common.svg import svg_polylines, svg_doc, svg_rects, svg_write

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
STEPS = 16

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

# --- main --------------
BORDER = svg_rects([CX-EXT_WIDTH, CY-EXT_HEIGHT, EXT_WIDTH*2, EXT_HEIGHT*2])
SPLITWALKS = svg_polylines(*SPLITWALKS)
doc = svg_doc(*BORDER, *SPLITWALKS)

svg_write(doc)
# axi_draw_svg(doc)
