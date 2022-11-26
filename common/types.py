from typing import NamedTuple

CPoint = NamedTuple(typename="CPoint", fields=[
    ("x", float),
    ("y", float)
])

HexPointCubic = NamedTuple(typename="HexPointCubic", fields=[
    ("q", int),
    ("r", int),
    ("s", int),
])

HexPointAxial = NamedTuple(typename="HexPointAxial", fields=[
    ("q", int),
    ("r", int),
])
