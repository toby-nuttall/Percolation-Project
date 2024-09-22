import numpy as np
import math
#reflect the geometry with a nearest neighbors function

#define position function, converting between a vector (i,j) and a node n
def position(size,node):
    M = np.arange(size)
    w = int(math.pow(size,1/2))
    M = np.resize(M,(w,w))
    
    i = node%w
    j = int(np.trunc(node/w))
    a = np.array([j,i])
    return a

#return 4 matrices of nearest neighbors to each point
def nearest(size):
    M = np.arange(size)
    w = int(math.pow(size,1/2))
    M = np.resize(M,(w,w))

    roll_up = np.roll(M,w)
    roll_down = np.roll(M,-w)

    roll_right = np.roll(M,-1)
    roll_right[0:w,w-1] = np.roll(roll_right,w)[0:w,(w-1)]

    roll_left = np.roll(M,1)
    roll_left[0:w,0] = np.roll(roll_left,-w)[0:w,0]

    return [roll_left,roll_right,roll_up,roll_down]

#a second nearest function defined for convenience
def nearest2(size,point):
    M = np.arange(size)
    w = int(math.pow(size,1/2))
    M = np.resize(M,(w,w))

    X = position(size,point)

    roll_up = np.roll(M,w)
    roll_down = np.roll(M,-w)

    roll_right = np.roll(M,-1)
    roll_right[0:w,w-1] = np.roll(roll_right,w)[0:w,(w-1)]

    roll_left = np.roll(M,1)
    roll_left[0:w,0] = np.roll(roll_left,-w)[0:w,0]

    return np.array([roll_left[X[0],X[1]],roll_right[X[0],X[1]],roll_up[X[0],X[1]],roll_down[X[0],X[1]]])

#function returning the neareest neighbor vector from a point to its occupied neighbor
def neighbor(R):
    if R == 0:
        return np.array([1,0])
    
    elif R == 1:
        return np.array([-1,0])
    
    elif R == 2:
        return np.array([0,1])
    
    else:
        return np.array([0,-1])

def lchoose(N,n):
    #defining a N choose n function which logs the result (similar to that in rust)

    return math.lgamma(N + 1)- math.lgamma(n + 1) - math.lgamma((N - n) + 1)


