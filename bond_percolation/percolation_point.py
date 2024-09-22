import numpy as np
import union_find as onion
import nearest_neighbors as nn
import math
import matplotlib.pyplot as plt
import time

#set up our lattice
numb = 10000
steps = 10000
uf = onion.UnionFind(numb)

start_time = time.time()

#call a set of random bonds to form
for i in range(steps):
    node1 = np.random.randint(0,numb)
    n1 = nn.position(numb,node1)

    R = np.random.randint(0,4)
    node2 = nn.nearest(numb)[R]
    node2 = node2[n1[1],n1[0]]
    
    neighbor_vector = nn.neighbor(R)

    #call the perolation checking condition
    disp = math.pow((uf.displacement[node2*2] - uf.displacement[node1*2])**2 + (uf.displacement[node2*2 + 1] - uf.displacement[node1*2 + 1])**2,1/2)
    if uf.find(node1) == uf.find(node2) and round(disp) != 1:

        uf.percolation_point[node1] = True
        uf.percolation_point[node2] = True
    else:
        pass

    #call the union algorithm    
    uf.union(node1,node2,neighbor_vector,numb)


end_time = time.time()
print(f"total time ={end_time - start_time}")

#defining a function to visualise the lattice of points as it percolates
def showing():
    a = []
    for i in range(numb):

        if uf.percolation_point[i] == True:
            print(i)
            a.append(int(uf.size[uf.find(i)]))
            pass
        
        else:
            a.append(int(uf.size[uf.find(i)]))

    w = int(math.pow(numb,1/2))
    a = np.resize(a,(w,w))
    return a

plt.matshow(showing())
plt.show()
        
