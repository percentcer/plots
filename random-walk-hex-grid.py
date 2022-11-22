#!/usr/bin/env python
# -*- encoding: utf-8 -#-

# https://axidraw.com/doc/py_api/
# https://github.com/evil-mad/axidraw
# http://axidraw.com/docs

import numpy as np
import random

import common.hexgrid as hg
from common.page import PAGE_WIDTH, PAGE_HEIGHT, gen_border
from common.svg import svg_preview

# --- draw transforms ---------------------------------------------------------
CX = PAGE_WIDTH / 2
CY = PAGE_HEIGHT / 2
SX = 1
SY = 1

# --- drawing config ----------------------------------------------------------
EXT_W = 80 * hg.RADIUS_OUTER * 1.5 # (flat top)
EXT_H = 60 * hg.RADIUS_INNER * 2
STEPS = 5000

def gen_walk(q,r,s):
    pos = [hg.HexPointCubic(q,r,s)]
    for _ in range(STEPS):
        # random q,r,s choice
        axis = random.randint(0,2)
        # random +/- choice
        sign = random.randint(0,1)*2-1
        # update it
        pos_next_mut = [*pos[-1]]
        pos_next_mut[(axis + 1) % 3] += sign
        pos_next_mut[(axis + 2) % 3] -= sign
        pos.append(hg.HexPointCubic(*pos_next_mut))
    return pos

# --- main --------------
WALK = gen_walk(0,0,0)
WALK = np.array([hg.hex_to_cart_flat(hp) for hp in WALK])
WALK *= 2
WALK += [CX, CY]

# for each path, remove all segments that are out of our bounds (this may produce new paths)
SPLITWALKS = []
_nwalk = []
for seg in WALK:
    if ((seg >= [CX-EXT_W, CY-EXT_H]) & (seg <= [CX+EXT_W, CY+EXT_H])).all(axis=0):
        _nwalk.append(seg.tolist())
    elif len(_nwalk):
        SPLITWALKS.append(_nwalk)
        _nwalk = []
    else:
        continue
SPLITWALKS.append(_nwalk)

BORDER = gen_border(CX, CY, EXT_W, EXT_H)

# axi_draw_paths(BORDER, WALK)
svg_preview(BORDER, *SPLITWALKS)
