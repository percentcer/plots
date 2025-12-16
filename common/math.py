import math
from math import sin, cos
import numpy as np

# --- math --------------------------------------------------------------------
TAU = 6.28
SQRT2 = math.sqrt(2)

def clamp(val, minval, maxval):
    return max(min(val, maxval),minval)

def sign(val):
    # considering zero positive
    return -1 if val < 0 else 1

def zsign(val):
    return 0 if val == 0 else sign(val)

def smoothstep(t):
    return t * t * (3-2*t)

def dist(p):
    return math.sqrt(p[0]*p[0] + p[1]*p[1])

def rot(a):
    return np.array([
        [cos(a), -sin(a)],
        [sin(a), cos(a)]
    ])
