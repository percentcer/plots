#!/usr/bin/env python
# -*- encoding: utf-8 -#-
# https://axidraw.com/doc/py_api/
# https://github.com/evil-mad/axidraw
# http://axidraw.com/docs

from common.page import PAGE_WIDTH, PAGE_HEIGHT
from common.svg import svg_preview

# lorenz from https://github.com/ubilabs/axidraw/blob/master/src/draw-lorenz.js
X = 9
Y = 1
Z = 1

A = 99
B = 11
C = 1

# scale and center
CX = PAGE_WIDTH / 2
CY = PAGE_HEIGHT / 2

MAG = 2
SX = (PAGE_WIDTH / PAGE_HEIGHT) * MAG
SY = 1 * MAG

EXT_WIDTH = (PAGE_WIDTH // 2) * 0.8
EXT_HEIGHT = (PAGE_HEIGHT // 2) * 0.8

BORDER = [
    [CX-EXT_WIDTH, CY-EXT_HEIGHT],
    [CX+EXT_WIDTH, CY-EXT_HEIGHT],
    [CX+EXT_WIDTH, CY+EXT_HEIGHT],
    [CX-EXT_WIDTH, CY+EXT_HEIGHT],
    [CX-EXT_WIDTH, CY-EXT_HEIGHT]
]

def gen(start_x, start_y):
    global X, Y, Z
    COORDS = []
    for _ in range(5000):
        Y += X - (X * Z - Y) / A
        X += (Y - X) / B
        Z += X * Y / Z - C
        p = [X * SX + start_x, Y * SY + start_y]
        COORDS.append(p)
    return COORDS

svg_preview(BORDER, gen(CX, CY))
