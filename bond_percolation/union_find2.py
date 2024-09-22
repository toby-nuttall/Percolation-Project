import nearest_neighbors as nn
import numpy as np


class UnionFind:

    
    def __init__(self, numOfElements,X):
        self.parent = self.makeSet(numOfElements)
        self.size = [1]*numOfElements
        self.count = numOfElements

        self.displacement = [0,0]*numOfElements
        self.percolation_point = [False]*numOfElements

        self.unselectedpairs = X
    
    def makeSet(self, numOfElements):
        return [x for x in range(numOfElements)]

    # Time: O(logn) | Space: O(1)
    def find(self, node):
        while node != self.parent[node]:
            # path compression
            self.parent[node] = self.parent[self.parent[node]]
            node = self.parent[node]
        return node
    
    #find all the points in a given cluster
    def family(self,node,numb):
        root = self.find(node)

        a = []
        for i in range(numb):
            a.append(self.find(i))

        b = []
        for i in range(len(a)):
            if a[i] == root:
                b.append(1)
            else:
                b.append(0)
            
        b = np.array(b)
        c = b.nonzero()
   
        return c[0]
    
    # Time: O(1) | Space: O(1)
    def union(self, node1, node2):
        root1 = self.find(node1)
        root2 = self.find(node2)

        # already in the same set
        if root1 == root2:
            return

        if self.size[root1] > self.size[root2]:

            #updateing the parents
            self.parent[root2] = root1
            self.size[root1] += self.size[root2]
            self.size[root2] = 0

        else:
        
            #updateing the parents
            self.parent[root1] = root2
            self.size[root2] += self.size[root1]
            self.size[root1] = 0

        
        self.count -= 1
    






