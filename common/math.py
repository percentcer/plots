import math

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
