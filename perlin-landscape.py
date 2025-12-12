#!/usr/bin/env python
# -*- encoding: utf-8 -#-

# https://axidraw.com/doc/py_api/
# https://github.com/evil-mad/axidraw
# http://axidraw.com/docs


from common.axidraw import axi_draw_svg, axi_draw_paths
from common.noise import Perlin
from common.page import PAGE_WIDTH, PAGE_HEIGHT
from common.svg import svg_polylines, svg_doc, svg_write, svg_rects
import numpy as np

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

    traces = []
    for ti in range(ylines):
        traces.append(list())

    while xsamp < 1.0:
        for ti in range(ylines):
            ysamp = ystep * ti
            s = p.sample(np.array([xsamp, ysamp]))
            traces[ti].append([(CX - WORKW*0.5) + xsamp * WORKW, (CY - WORKH*0.5) + ysamp * WORKH + s * offset_factor])
        xsamp += xstep

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
lines = gen(0.01, 200, 15)
svglines = svg_polylines(*lines)
doc = svg_doc(*svglines)

svg_write(doc)
# axi_draw_svg(doc)
