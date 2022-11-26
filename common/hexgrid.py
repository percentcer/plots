from typing import Union
from .types import CPoint, HexPointCubic, HexPointAxial
import math

RADIUS_OUTER = 1
RADIUS_INNER = math.sqrt(3) / 2 * RADIUS_OUTER

def hex_to_cart_flat(hp: Union[HexPointCubic, HexPointAxial]) -> CPoint:
    x = 3 / 2 * hp.q
    y = math.sqrt(3)/2 * hp.q + math.sqrt(3) * hp.r
    return x,y

def hex_axial_to_cube(hpa: HexPointAxial) -> HexPointCubic:
    return hpa.q, hpa.r, -(hpa.q+hpa.r)

def hex_cube_to_axial(hpc: HexPointCubic) -> HexPointAxial:
    return hpc.q, hpc.r
