#!/usr/bin/env python
# -*- encoding: utf-8 -#-

# https://axidraw.com/doc/py_api/
# https://github.com/evil-mad/axidraw
# http://axidraw.com/docs


from common.axidraw import axi_draw_svg, axi_draw_paths
from common.math import smoothstep, dist, TAU, rot
from common.noise import Perlin
from common.page import PAGE_WIDTH, PAGE_HEIGHT
from common.svg import svg_polylines, svg_circles, svg_doc, svg_write

import numpy as np
import scipy as sp

import random
import sys

# --- draw transforms ---------------------------------------------------------
WORKW = PAGE_WIDTH * 0.9
WORKH = PAGE_HEIGHT * 0.9
CX = PAGE_WIDTH / 2  # (mm)
CY = PAGE_HEIGHT / 2  # (mm)
SX = 1
SY = 1

def gen(xstep, num_snakes, size_factor):
    gridw = 10
    gridh = 10
    p = Perlin(gridw,gridh)

    pos = []
    sizerow = []
    dirrow = []
    for snakeidx in range(num_snakes):
        pos.append(np.array([CX,CY]))
        sizerow.append(random.random())
        dirrow.append(random.random())

    traces = []

    for snakeidx in range(num_snakes):
        xsamp = 0
        while xsamp < 1.0:
            sz = (p.sample(np.array([xsamp, sizerow[snakeidx]])) * 0.5 + 0.5) * size_factor
            dr = (p.sample(np.array([xsamp, dirrow[snakeidx]]))) * TAU
            # print(dirrow[snakeidx], dr, p.sample(np.array([xsamp, dirrow[snakeidx]])))
            pos[snakeidx] += np.array([1,0]) @ rot(dr)
            traces.append([pos[snakeidx][0], pos[snakeidx][1], sz])
            xsamp += xstep

    return traces


# --- main --------------
result = gen(0.005, 1, 7)
circles = svg_circles(*result, fill='white')
doc = svg_doc(*circles)

svg_write(doc)
# axi_draw_svg(doc)
