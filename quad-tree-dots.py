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
EXT = 1024
EXT_W = EXT
EXT_H = EXT


def find_quadrant(point: hg.CPoint, center: hg.CPoint, ext: int):
    #          ^
    #    1     |     0
    #          |
    #          |
    # ---------+--------->
    #          |
    #          |
    #    2     |     3
    #          |
    pass


def gen(n: int, depth: int, ext: int):
    # pick n random positions
    pos = [hg.CPoint(random.randint(-ext, ext), random.randint(-ext, ext))
           for _ in range(n)]
    # generate quad tree
    # generate circles based on child count
    # return circles
    return pos


# --- main --------------
svgcircles = svg_circles(gen(5, 4, EXT_W))
svgborder = svg_rects([CX-EXT_W, CY-EXT_H, EXT_W*2, EXT_H*2])
doc = svg_doc(*svgborder, *svgcircles)

svg_write(doc)
# axi_draw_svg(doc)
