from typing import NamedTuple

CPoint = NamedTuple("CPoint", fields=[
    ("x", float),
    ("y", float)
])

HexPointCubic = NamedTuple("HexPointCubic", fields=[
    ("q", int),
    ("r", int),
    ("s", int),
])

HexPointAxial = NamedTuple("HexPointAxial", fields=[
    ("q", int),
    ("r", int),
])
