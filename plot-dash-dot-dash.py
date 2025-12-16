#!/usr/bin/env python
# -*- encoding: utf-8 -#-

# https://axidraw.com/doc/py_api/
# https://github.com/evil-mad/axidraw
# http://axidraw.com/docs

from collections import Counter
import math
import random
# import numpy as np

from common.axidraw import axi_draw_svg, axi_draw_paths
from common.math import TAU, SQRT2
from common.page import PAGE_WIDTH, PAGE_HEIGHT
from common.quad_trees import quarter_space
from common.svg import svg_polylines, svg_doc, svg_write, svg_rects

# --- draw transforms ---------------------------------------------------------
CX = PAGE_WIDTH / 2  # (mm)
CY = PAGE_HEIGHT / 2  # (mm)
SX = 1
SY = 1

# # --- drawing config ----------------------------------------------------------
# EXT = 256
# EXT_W = EXT
# EXT_H = EXT


def gen(gapsize):
    n = PAGE_HEIGHT / gapsize

    result = []
    # endpoints have an acceleration and velocity
    aL = 0
    vL = 0
    pL = PAGE_WIDTH * 0.25
    aR = 0
    vR = 0
    pR = PAGE_WIDTH * 0.75
    for i in range(math.floor(n)):
        # apply some jitter to accelerations
        aL = 1.0 - random.random() * 2.0
        aR = 1.0 - random.random() * 2.0
        # new endpoints:
        vL += aL
        pL += vL
        vR += aR
        pR += vR
        # height based on current line (top is 0)
        height = i * gapsize
        pM = pR - pL  # midpoint

        # write line segments (- . -)
        left_section = [[pL, height], [pM - 2, height]]
        result.append(left_section)

        # center dot looks weird, omitting

        right_section = [[pM + 2, height], [pR, height]]
        result.append(right_section)

    return result


# --- main --------------
lines = gen(3)
svglines = svg_polylines(*lines)
# svgborder = svg_rects([CX - EXT_W, CY - EXT_H, CX + EXT_W, CY + EXT_H])
# doc = svg_doc(*svgborder, *svglines)
doc = svg_doc(*svglines)

svg_write(doc)
# axi_draw_svg(doc)
