import numpy as np
import union_find2 as UF
import nearest_neighbors as nn
import math
import matplotlib.pyplot as plt
import time

#set up our lattice
numb = 100
steps = 100

X = nn.nearest_bonds(numb)
uf = UF.UnionFind(numb,X)

start_time = time.time()

#function to be called to run each percolation simulation
def RUN(numb):
    clusters = []

    while  len(uf.unselectedpairs) >= 1:

        #select a bond to be filled
        [node1,node2] = uf.unselectedpairs[np.random.randint(len(uf.unselectedpairs))]
        uf.unselectedpairs.remove([node1,node2])

        #call the union algorithm
        uf.union(node1,node2)

        #cluster size finding function
        clusters.append(uf.size[uf.find(node1)])


    #produce an array of largest cluster size 
    largest_cluster = []
    current_largest = 0

    for i in range(len(clusters)):
            
        if clusters[i] > current_largest:
            current_largest = clusters[i]
            
        else:
            pass

        largest_cluster.append(current_largest)


    return largest_cluster

#reset function to resset the lattice after each simulation
def reset(numb):
    X = nn.nearest_bonds(numb)
    uf.unselectedpairs = X
    uf.size = [1]*numb
    uf.count = numb
    uf.parent = uf.makeSet(numb)
  

#defining a function to visualise the lattice of points as it percolates, this was used only in testing and writing
def showing():
    a = []
    for i in range(numb):
        a.append(int(uf.size[uf.find(i)]))
        
    w = int(math.pow(numb,1/2))
    a = np.resize(a,(w,w))
    return a

#defining the occupation probability linspace
p = np.linspace(0,1,1000)

#define the convolver function to convert between the microcanoncal and canonical ensemble 
def convolver(Qn):
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
    return Qp

