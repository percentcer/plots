#!/usr/bin/env python
# -*- encoding: utf-8 -#-

# https://axidraw.com/doc/py_api/
# https://github.com/evil-mad/axidraw
# http://axidraw.com/docs

from collections import Counter
import numpy as np
import random

import common.hexgrid as hg
from common.axidraw import axi_draw_svg, axi_draw_paths
from common.page import PAGE_WIDTH, PAGE_HEIGHT
from common.svg import svg_circles, svg_doc, svg_write, svg_rects
from common.math import clamp

# --- draw transforms ---------------------------------------------------------
CX = PAGE_WIDTH / 2
CY = PAGE_HEIGHT / 2
SX = 1
SY = 1

# --- drawing config ----------------------------------------------------------
EXT_W = 70 * hg.RADIUS_OUTER * 1.5  # (flat top)
EXT_H = 40 * hg.RADIUS_INNER * 2
STEPS = 500


def gen_walk(q, r, s):
    pos = [hg.HexPointCubic(q, r, s)]
    for _ in range(STEPS):
        # random q,r,s choice
        axis = random.randint(0, 2)
        # random +/- choice
        sign = random.randint(0, 1)*2-1
        # update it
        pos_next_mut = [*pos[-1]]
        pos_next_mut[(axis + 1) % 3] += sign
        pos_next_mut[(axis + 2) % 3] -= sign
        pos.append(hg.HexPointCubic(*pos_next_mut))
    return pos


# --- main --------------
def process(_walk, _radfn):
    WALK_CNT = Counter(_walk)

    _walk = np.array([hg.hex_to_cart_flat(hp) for hp in WALK_CNT])
    COUNT = [WALK_CNT[c] for c in WALK_CNT]

    _walk *= 2
    _walk += [CX, CY]

    # bounds filter
    def in_bounds(seg): return ((
        seg >= [CX-EXT_W+hg.RADIUS_OUTER, CY-EXT_H+hg.RADIUS_OUTER*2.5]
        ) & (
        seg <= [CX+EXT_W-hg.RADIUS_OUTER, CY+EXT_H-hg.RADIUS_OUTER*2.5]
        )).all(axis=0)


    _walk = [(p[0], p[1], _radfn(c))
            for p, c in zip(_walk, COUNT) if in_bounds(p)]
    return _walk



# svgcircles = svg_circles(*process(gen_walk(0, 0, 0), lambda c: clamp(c, 1, 3)*0.5))
svgcircles_small = svg_circles(*process(gen_walk(0, 0, 0), lambda c: 0.5))
svgcircles_mid = svg_circles(*process(gen_walk(0, 0, 0), lambda c: 0.5*2))
svgcircles_large = svg_circles(*process(gen_walk(0, 0, 0), lambda c: 0.5*3))

svgborder = svg_rects([CX-EXT_W, CY-EXT_H, EXT_W*2, EXT_H*2])

# doc = svg_doc(*svgborder)
# doc = svg_doc(*svgcircles)
# doc = svg_doc(*svgborder, *svgcircles)
# doc = svg_doc(*svgcircles_small, *svgcircles_mid, *svgcircles_large)
doc = svg_doc(*svgborder, *svgcircles_small, *svgcircles_mid, *svgcircles_large)

svg_write(doc)
# axi_draw_svg(doc)
