#!/usr/bin/env python
# -*- encoding: utf-8 -#-

# https://axidraw.com/doc/py_api/
# https://github.com/evil-mad/axidraw
# http://axidraw.com/docs

from collections import Counter
import numpy as np

from common.axidraw import axi_draw_svg, axi_draw_paths
from common.math import TAU, SQRT2
from common.page import PAGE_WIDTH, PAGE_HEIGHT
from common.quad_trees import quarter_space
from common.svg import svg_circles, svg_doc, svg_write, svg_rects

# --- draw transforms ---------------------------------------------------------
CX = PAGE_WIDTH / 2
CY = PAGE_HEIGHT / 2
SX = 1
SY = 1

# --- drawing config ----------------------------------------------------------
EXT = 1024
EXT_W = EXT
EXT_H = EXT
OFFS = np.array(
    [
        [1, 1],
        [-1, 1],
        [-1, -1],
        [1, -1],
    ]
)


def gen(scl):
    # generate quad tree
    root = quarter_space(10, 7)
    # walk the tree, each leaf should resolve in a circle (rad based on depth, position based on quad offsets)
    def walk(node, depth, pos):
        if not len(node):
            return [(*(pos*scl+[CX,CY]), pow(0.5, depth-1) * SQRT2 * scl)]
        return (
              walk(node[0], depth + 1, pos + OFFS[0] * pow(0.5, depth) * SQRT2)
            + walk(node[1], depth + 1, pos + OFFS[1] * pow(0.5, depth) * SQRT2)
            + walk(node[2], depth + 1, pos + OFFS[2] * pow(0.5, depth) * SQRT2)
            + walk(node[3], depth + 1, pos + OFFS[3] * pow(0.5, depth) * SQRT2)
        )
    return walk(root, 0, np.array([0,0]))


# --- main --------------
circles = gen(48)
svgcircles = svg_circles(*circles)
svgborder = svg_rects([CX - EXT_W, CY - EXT_H, EXT_W * 2, EXT_H * 2])
doc = svg_doc(*svgborder, *svgcircles)

svg_write(doc)
# axi_draw_svg(doc)
