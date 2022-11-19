#!/usr/bin/env python
# -*- encoding: utf-8 -#-

# https://axidraw.com/doc/py_api/
# https://github.com/evil-mad/axidraw
# http://axidraw.com/docs

from common.page import PAGE_WIDTH, PAGE_HEIGHT, gen_border
from common.svg import svg_preview

# --- draw transforms ---------------------------------------------------------
MAG = 3
CX = PAGE_WIDTH / 2
CY = PAGE_HEIGHT / 2
SX = (PAGE_WIDTH / PAGE_HEIGHT) * MAG
SY = 1 * MAG

# --- drawing config ----------------------------------------------------------
EXT_WIDTH = (PAGE_WIDTH // 2) * 0.8
EXT_HEIGHT = (PAGE_HEIGHT // 2) * 0.8

# lorenz from https://github.com/ubilabs/axidraw/blob/master/src/draw-lorenz.js
A = 99
B = 11
C = 1


def gen(p_x, p_y, p_z):
    COORDS = []
    for _ in range(5000):
        p_x += (p_y - p_x) / B
        p_y += p_x - (p_x * p_z - p_y) / A
        p_z += p_x * p_y / p_z - C
        COORDS.append([p_x, p_y])
    return COORDS

# --- main --------------
PATH = gen(9, 1, 1)
BORDER = gen_border(CX, CY, EXT_WIDTH, EXT_HEIGHT)

# axi_draw_paths(BORDER, PATH)
svg_preview(BORDER, PATH)
