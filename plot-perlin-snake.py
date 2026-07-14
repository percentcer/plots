#!/usr/bin/env python
# -*- encoding: utf-8 -#-

# https://axidraw.com/doc/py_api/
# https://github.com/evil-mad/axidraw
# http://axidraw.com/docs


from common.axidraw import axi_draw_svg, axi_draw_paths
from common.math import smoothstep, dist, TAU, rot
from common.noise import Perlin
from common.page import PAGE_WIDTH, PAGE_HEIGHT
from common.svg import svg_polylines, svg_circles, svg_doc, svg_write, svg_frame

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
    idir = []
    rwsize = []
    rwdir = []

    for snakeidx in range(num_snakes):
        pos.append(np.array([CX,CY]))
        idir.append(np.array([1,0]) @ rot(random.random() * TAU))
        rwsize.append(random.random())
        rwdir.append(random.random())

    traces = []

    for snakeidx in range(num_snakes):
        xsamp = 0
        while xsamp < 1.0:
            sz = (p.sample(np.array([xsamp, rwsize[snakeidx]])) * 0.5 + 0.5) * size_factor
            dr = (p.sample(np.array([xsamp, rwdir[snakeidx]])) * 0.5 + 0.5) * TAU
            pos[snakeidx] += idir[snakeidx] @ rot(dr)
            traces.append([pos[snakeidx][0], pos[snakeidx][1], sz])
            xsamp += xstep

    return traces

def gen_anim(xstep, fx, fy, size_factor):
    gridw = 10
    gridh = 10
    p = Perlin(gridw,gridh)

    pos = []
    idir = []
    rwsize = []
    rwdir = []

    cxstep = PAGE_WIDTH / fx
    cystep = PAGE_HEIGHT / fy
    idir_ = np.array([1,0]) @ rot(random.random() * TAU)
    rwsize_ = random.random()
    rwdir_ = random.random()

    for snakeidx in range(fx * fy):
        x_ = snakeidx % fx
        y_ = snakeidx // fx
        cellCX = (0.5 + x_) * cxstep
        cellCY = (0.5 + y_) * cystep
        # print(snakeidx, fx, snakeidx % fx, cellCX, cellCY)
        pos.append(np.array([cellCX, cellCY]))
        idir.append(idir_)
        rwsize.append(rwsize_)
        rwdir.append(rwdir_ + snakeidx * 0.01)

    traces = []

    for snakeidx in range(fx * fy):
        xsamp = 0
        while xsamp < .3:
            sz = (p.sample(np.array([xsamp, rwsize[snakeidx]])) * 0.5 + 0.5) * size_factor
            dr = (p.sample(np.array([xsamp, rwdir[snakeidx]])) * 0.5 + 0.5) * TAU
            pos[snakeidx] += idir[snakeidx] @ rot(dr)
            traces.append([pos[snakeidx][0], pos[snakeidx][1], sz])
            xsamp += xstep

    return traces


# --- main --------------
# result = gen(0.007, 1, 7)
result = gen_anim(0.008, 10, 8, 3)
circles = svg_circles(*result, fill='white')
doc = svg_doc(*circles, *svg_frame(0.05))

svg_write(doc)
# axi_draw_svg(doc)
