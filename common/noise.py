from .math import TAU, smoothstep
from .types import CPoint
from math import cos, sin
import random
import numpy as np

class Perlin:
    gradient_vectors = []
    dimensions: np.ndarray = np.array([-1, -1])
    def __init__(self, x, y):
        self.dimensions = np.array([x,y])
        for _ in range( (x+1) * (y+1) ):
            # todo: make the extreme values match the 0 values for looping
            v = np.array([1,0])
            a = random.random() * TAU
            r = np.array([[cos(a), sin(a)], [-sin(a), cos(a)]]) # np is row major
            self.gradient_vectors.append(v @ r)

    def sample(self, p: np.ndarray):
        # mod sample position if it's outside of the [0..1] range
        p = np.modf(p)[0]
        if p[0] < 0:
            p[0] = 1 + p[0]
        if p[1] < 0:
            p[1] = 1 + p[1]


        # determine which cell we're in
        expp = p * self.dimensions
        uv_cell = np.modf(expp)


        # compute offset vectors to uv from each of the four corners
        #     00              10
        #       ┌────────────┐ 
        #       │            │ 
        #       │   uv       │ 
        #       │            │ 
        #       │            │ 
        #       └────────────┘ 
        #     01              11
        u = uv_cell[0][0]
        v = uv_cell[0][1]
        off_00 = np.array([u,         v])
        off_10 = np.array([u - 1,     v])
        off_01 = np.array([u,     v - 1])
        off_11 = np.array([u - 1, v - 1])

        # print("=========================")
        # print(p)
        # print(u,v)
        # print(ne,nw,sw,se)

        # gather the four corner values themselves
        stride = self.dimensions[1] + 1
        cellx = int(uv_cell[1][0])
        celly = int(uv_cell[1][1])
        # print(cellx, celly)
        grid_00 = self.gradient_vectors[ celly * stride + cellx ]
        grid_10 = self.gradient_vectors[ celly * stride + cellx + 1]
        grid_01 = self.gradient_vectors[ (celly + 1) * stride + cellx ]
        grid_11 = self.gradient_vectors[ (celly + 1) * stride + cellx + 1 ]
        # print(grid_ne,grid_nw,grid_sw,grid_se)

        # compute dot product with each
        dot_00 = np.dot(grid_00, off_00)
        dot_10 = np.dot(grid_10, off_10)
        dot_01 = np.dot(grid_01, off_01)
        dot_11 = np.dot(grid_11, off_11)

        # bilinear blend
        dot_mat = np.array([
                [dot_00, dot_10],
                [dot_01, dot_11]
            ])
        
        lerp_u = np.array([smoothstep(1.0 - u), smoothstep(u)])
        lerp_v = np.array([smoothstep(1.0 - v), smoothstep(v)])

        blend = lerp_u @ (dot_mat.T @ lerp_v)

        return blend
