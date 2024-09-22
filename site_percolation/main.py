import numpy as np
import union_find as onion
import nearest_neighbors as nn
import math
import matplotlib.pyplot as plt
import time

#set up our lattice
numb = 32 ** 2

uf = onion.UnionFind(numb)
Perc = 0

#define entire lists of all possible nearest neighbor vectors outside loop
nnx = np.array([-1,1,0,0])
nny = np.array([0,0,-1,1])

#defining the updater function to be repeatedly called
def update(numb,point):
    #find neighbors of point
    neighbors = nn.nearest2(numb,point)


    #find unnocupied neighbors
    inverted_mask = np.isin(neighbors,np.array(uf.unselected))
    mask = [not j for j in inverted_mask]
    occupied_neighbors = neighbors[mask]

    #must compare sizes of neighbors and join them all to the largest, for one or more neighbors
    if np.size(occupied_neighbors) != 0:

        #find the sizes of the occupied neighbors
        size_array = []
        for i in range(len(occupied_neighbors)):
            node = occupied_neighbors[i]
            size_array.append(uf.size[uf.find(node)])

        #find largest cluster, and remove it from the occupied neighbors list
        biggest_argument = np.argmax(size_array)
        biggest_cluster = occupied_neighbors[biggest_argument]
        np.delete(occupied_neighbors,biggest_argument)

        #finding the nearest neighbor vectors of the occupied neighbor sites
        neighbor_positions = np.nonzero(mask)[0]
        neighbor_vectorx = nnx[neighbor_positions]
        neighbor_vectory = nny[neighbor_positions]

        #call union on the largest cluster, point and rest of occupied clusters
        uf.union(biggest_cluster,point)

        r1x = neighbor_vectorx[biggest_argument] + uf.displacementx[biggest_cluster]
        uf.displacementx[point] = r1x
        r1y = neighbor_vectory[biggest_argument] + uf.displacementy[biggest_cluster]
        uf.displacementy[point] = r1y
    
        #define objects required to check for percolation
        occupied_roots = []
        for i in occupied_neighbors:
            occupied_roots.append(uf.find(i))

        biggest_parent = uf.find(biggest_cluster)

        #check for percoaltion and update the other clusters
        for k in range(len(occupied_neighbors)):
            nni = occupied_neighbors[k]

            #percolation checking condition
            if occupied_roots[k] == biggest_parent:
                dx = abs(uf.displacementx[point] - uf.displacementx[nni])
                dy = abs(uf.displacementy[point] - uf.displacementy[nni])

                if dx + dy != 1:
        

                    global Perc
                    Perc = Perc + 1
        
            #updating the pointers in a cluster
            rx = neighbor_vectorx[k] + uf.displacementx[nni]
            ry = neighbor_vectory[k] + uf.displacementy[nni]
            cluster_points = np.where(uf.roots == uf.find(nni))[0]
            deltarx = r1x - rx
            deltary = r1y - ry

            for l in cluster_points:
                uf.displacementx[l] = uf.displacementx[l] + deltarx
                uf.displacementy[l] = uf.displacementy[l] + deltary

            uf.union(biggest_cluster,nni)
        
#define a function to produce a percolation run and find when percolation has occured
def RUN(numb):
    counter = 0

    global Perc
    while Perc == 0:
    
        node1 = np.random.choice(uf.unselected)
    
        argument = np.argwhere(uf.unselected == node1)[0][0]
        uf.unselected = np.delete(np.array(uf.unselected),argument)
    
        update(numb,node1)
        counter += 1

    return counter

#defining a reset function to reset the percolation algorithm
def reset(numb):
    global Perc
    Perc = 0

    uf.size = [1]*numb
    uf.count = numb
    uf.parent = uf.makeSet(numb)
    uf.unselected = uf.parent     
    uf.roots = np.array(uf.parent)
  
    uf.displacementx = [0] * numb
    uf.displacementy = [0] * numb

#define a probability distribution
epsilon = 0.00001
p = np.linspace(epsilon,1 - epsilon,1000)

#define a function to convolve things with a binomial distribution
def convolver(Qn):
    start_time_2 = time.time()
    N = len(Qn)
    lnp = np.log(p)
    ln1_p = np.log(1-p)
    lnQn = np.log(Qn)

    Qpn = np.zeros(len(p) * N)
    Qpn = np.resize(Qpn,(len(p),N))

    for i in range(N):
        #the nCr values are calculted in log form then exponentiated as they are too big
        lnQ = (lnp * i) + (ln1_p * (N - i)) + lnQn[i]  + (nn.lchoose(N,i))
        Qpn[:,i] =np.exp(lnQ)

    ones = np.ones(N)
   
    Qp = np.matmul(Qpn,ones)
    finish_time_2 = time.time()

    print(f"{finish_time_2 - start_time_2} convolver time")
    return Qp


#defining a function to visualise the lattice of points as it percolates
def showing():
    a = []
    for i in range(numb):
        a.append(int(uf.size[uf.find(i)]))
        
    w = int(math.pow(numb,1/2))
    a = np.resize(a,(w,w))
    return a

        