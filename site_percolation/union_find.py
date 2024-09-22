import nearest_neighbors as nn
import numpy as np


class UnionFind:

    
    def __init__(self, numOfElements):
        self.parent = self.makeSet(numOfElements)
        self.size = [1]*numOfElements
        self.count = numOfElements
        self.unselected = self.parent 
        self.roots = np.array(self.parent)

        #keep track of displacements
        self.displacementx = [0] * numOfElements
        self.displacementy = [0] * numOfElements
    
    def makeSet(self, numOfElements):
        return [x for x in range(numOfElements)]

    # Time: O(logn) | Space: O(1)
    def find(self, node):
        while node != self.parent[node]:
            # path compression
            self.parent[node] = self.parent[self.parent[node]]
            node = self.parent[node]
        return node
    
    
    # Time: O(1) | Space: O(1)
    def union(self, node1, node2):
        root1 = self.find(node1)
        root2 = self.find(node2)

        # already in the same set
        if root1 == root2:
            return

        if self.size[root1] >= self.size[root2]:

            #updateing the parents
            self.parent[root2] = root1
            self.size[root1] += self.size[root2]
            self.size[root2] = 0

            #keep track of the roots efficently 
            arguments = np.where(self.roots == root2)[0]
            self.roots[arguments] = root1
            

            

        else:
        
            #updateing the parents
            self.parent[root1] = root2
            self.size[root2] += self.size[root1]
            self.size[root1] = 0

            #keep track of the roots efficently 
            arguments = np.where(self.roots == root1)
            self.roots[arguments] = root2

        
        self.count -= 1

    
