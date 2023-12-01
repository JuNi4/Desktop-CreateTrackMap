from math import *
from numba import jit

@jit(nopython=True)
def rotation_matrix(a, v,size):
    # convert degrees to radians
    a = radians(a)
    # get sin and cosin
    c = cos(a)
    s = sin(a)
    # construct matrix
    #m = [
    #    [ c, -s ],
    #    [ s,  c ]
    #]

    # unfold vector
    vx, vy = v
    # multiply by size
    vx = vx*size
    vy = vy*size

    # calculate position vector
    x = c*vx - -s*vy
    y = s*vx - c*vy

    return x,y