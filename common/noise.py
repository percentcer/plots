from .math import TAU
from .types import CPoint
import random
import numpy as np

class Perlin:
    gradient_vectors = []
    dimensions: np.ndarray = np.array([-1, -1])
    def __init__(self, x, y):
        self.dimensions = np.array([x,y])
        for _ in range( (x+1) * (y+1) ):
            v = np.array([1,0])
            a = random.random() * TAU
            r = np.array([np.cos(a), -np.sin(a)], [np.sin(a), np.cos(a)])
            self.gradient_vectors.append(v @ r)

    def sample(self, p: np.ndarray):
        # determine which cell we're in
        expp = p * self.dimensions
        cell = np.min(np.floor(expp), self.dimensions-1)
        uv = np.fract(expp)

        # compute offset vectors to uv from each of the four corners
        #     nw              ne
        #       ┌────────────┐ 
        #       │            │ 
        #       │   uv       │ 
        #       │            │ 
        #       │            │ 
        #       └────────────┘ 
        #     sw              se
        ne = np.array([uv[0] - 1,    -uv[1]])
        nw = np.array([uv[0],        -uv[1]])
        sw = np.array([uv[0],     1 - uv[1]])
        se = np.array([uv[0] - 1, 1 - uv[1]])

        # gather the four corner values themselves
        stride = self.dimensions[1] + 1
        grid_ne = self.gradient_vectors[ cell[0] + 1 + cell[1] * stride ]
        grid_nw = self.gradient_vectors[ cell[0] + cell[1] * stride ]
        grid_sw = self.gradient_vectors[ cell[0] + (cell[1] + 1) * stride ]
        grid_se = self.gradient_vectors[ cell[0] + 1 + (cell[1] + 1) * stride ]

        # compute dot product with each
        
        # weighted blend
        pass
