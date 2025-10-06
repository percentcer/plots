#!/usr/bin/env python
# -*- encoding: utf-8 -#-

# https://axidraw.com/doc/py_api/
# https://github.com/evil-mad/axidraw
# http://axidraw.com/docs

import numpy as np
from typing import NamedTuple
from common.axidraw import axi_draw_svg, axi_draw_paths
from common.math import TAU, SQRT2
from common.page import PAGE_WIDTH, PAGE_HEIGHT
from common.svg import svg_polylines, svg_doc, svg_write, svg_rects

# --- draw transforms ---------------------------------------------------------
CX = PAGE_WIDTH / 2
CY = PAGE_HEIGHT / 2
SX = 1
SY = 1

# --- drawing config ----------------------------------------------------------
EXT = 1024
EXT_W = EXT
EXT_H = EXT

def gen(w,h):
    pass

def walk(maze):
    return []

# --- main --------------
maze = gen(w=8,h=8)
maze_lines = walk(maze)
svg_lines = svg_polylines(*maze_lines)
# svgborder = svg_rects([CX - EXT_W, CY - EXT_H, EXT_W * 2, EXT_H * 2])
doc = svg_doc(*svg_lines)

svg_write(doc)
# axi_draw_svg(doc)
