#!/usr/bin/env python
# -*- encoding: utf-8 -#-

# https://axidraw.com/doc/py_api/
# https://github.com/evil-mad/axidraw
# http://axidraw.com/docs


from common.axidraw import axi_draw_svg, axi_draw_paths
from common.math import smoothstep, dist
from common.noise import Perlin
from common.page import PAGE_WIDTH, PAGE_HEIGHT
from common.svg import svg_polylines, svg_circles, svg_doc, svg_write

import numpy as np
import scipy as sp

import sys

# --- draw transforms ---------------------------------------------------------
WORKW = PAGE_WIDTH * 0.9
WORKH = PAGE_HEIGHT * 0.9
CX = PAGE_WIDTH / 2  # (mm)
CY = PAGE_HEIGHT / 2  # (mm)
SX = 1
SY = 1

def gen(xstep, ylines, offset_factor):
    # walk through one row of the perlin noise at step size and produce a line offset by the value at each sample [-1, 1]
    ystep = 1.0 / ylines
    xsamp = 0
    ysamp = 0

    gridw = 10
    gridh = 10
    p = Perlin(gridw,gridh)

    disk = sp.stats.qmc.PoissonDisk(2, radius=0.02)
    samples = disk.fill_space()
    # offset range
    samples = [s - 0.5 for s in samples]
    # reject samples outside of the circle
    samples = [s for s in samples if dist(s) < 0.5]
    
    # print(samples)
    # sys.exit()

    traces = []

    for pos in samples:
        s = p.sample(pos)
        offsetmod = 120 + smoothstep(dist(pos)*2) * 20
        traces.append([CX + pos[0] * offsetmod, CY + pos[1] * offsetmod, (s + 1)])

    # while xsamp < 1.0:
    #     for ti in range(ylines):
    #         ysamp = ystep * ti
    #         s = p.sample(np.array([xsamp, ysamp]))
    #         traces.append([
    #             (CX - WORKW * 0.5) + xsamp * WORKW, (CY - WORKH*0.5) + ysamp * WORKH, smoothstep(s * 0.5 + 0.5) * offset_factor
    #             ])
    #     xsamp += xstep

    # # debug grid lines
    # for xi in range(gridw):
    #     traces.append([
    #         [xi * 1/gridw * PAGE_WIDTH, 0],
    #         [xi * 1/gridw * PAGE_WIDTH, PAGE_HEIGHT],
    #         ])
    # for yi in range (gridh):
    #     traces.append([
    #         [0,          yi * 1/gridh * PAGE_HEIGHT],
    #         [PAGE_WIDTH, yi * 1/gridh * PAGE_HEIGHT],
    #         ])
        
    return traces


# --- main --------------
result = gen(0.02, 20, 3)
circles = svg_circles(*result)
doc = svg_doc(*circles)

svg_write(doc)
# axi_draw_svg(doc)
