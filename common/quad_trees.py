import numpy as np
from random import randint
from typing import NamedTuple

from .types import CPoint

def find_quad(point: CPoint, depth: int):
    quad = -1
    #          |
    #    1     |     0
    #          |
    # ---------+---------
    #          |
    #    2     |     3
    #          |
    # assume point is normalized [0,1]
    MD = 0.5
    DIRS = np.array(
        [
            [MD, MD],
            [0, MD],
            [0, 0],
            [MD, 0],
        ]
    )
    tmp = np.array(point)
    for _ in range(depth + 1):
        # check quad, offset in the quad direction, scale up
        if tmp[1] > MD:
            quad = 1 if tmp[0] < MD else 0
        else:
            quad = 2 if tmp[0] < MD else 3
        tmp -= DIRS[quad]
        tmp *= 2.0
    return (quad, tmp)


def quad_tree(points):
    Leaf = NamedTuple(typename="Leaf", fields=[
        ("point", CPoint),
        ("point_rel", CPoint),
        ("quad", int)
    ])

    def dfs(test, node, depth):
        quad, p_rel = find_quad(test, depth)

        if not len(node):
            node.extend([[] for _ in range(4)])
        if not len(node[quad]):
            node[quad] = Leaf(test, p_rel, quad)
            return
        
        if type(node[quad]) == Leaf:
            # can't have two leaves
            l = node[quad]
            l_q, l_pr = find_quad(l.point_rel, 0)
            node[quad] = [[]] * 4
            node[quad][l_q] = Leaf(l.point, l_pr, l_q)
        
        dfs(test, node[quad], depth+1)
    
    root = []
    for p in points:
        dfs(p, root, 0)
    return root
    
def quarter_space(branches: int, depth: int) -> list:
    # recursion helper
    def splitter(node, depth):
        if depth == 0:
            return
        if not len(node):
            node.extend([[] for _ in range(4)])
        splitter(node[randint(0,3)], depth-1)
    # walk for each branch
    root = []
    for _ in range(branches):
        splitter(root, depth)
    return root

