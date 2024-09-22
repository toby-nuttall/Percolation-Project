import percolation_clustersize as pc
import numpy as np
import time
import matplotlib.pyplot as plt

#defining p again for readability of code, p = probability linspace
p = np.linspace(0,1,1000)


#function to be called once for each lattice size, to collect and convolute data 
def data_collection(L):

#prepare the lattice 
    pc.reset(L ** 2)

# collecting the data in microcanonicle ensemble
    data = np.zeros(2 * 100 * L**2)
    data = np.resize(data, (2 * L**2,100))


#BIG loop, this is the slow step
    for j in range(100):
        a = pc.RUN(L ** 2)
        print(j)
        data[:,j] = a
        pc.reset(L ** 2)

    #defining objects for the matrix multiplication 
    ones = np.ones(100)
    DATA = np.matmul(data,ones) * 0.01 * 1/(L**2)

    return pc.convolver(DATA)

start_time = time.time()

#define the line to compare to
d1 = np.ones(100) * 0.5927
height = np.linspace(0,1,100)

#call the data to be collected 
Q32 = data_collection(32)
Q64 = data_collection(64)
Q128 = data_collection(128)
Q256 = data_collection(256)

end_time = time.time()
print(f"total time ={end_time - start_time}")

plt.plot(p,Q32, label = "L = 32")
plt.plot(p,Q64, label = "L = 64")
plt.plot(p,Q128, label = "L = 128")
plt.plot(p,Q256, label = "L = 256")
plt.plot(d1,height,linestyle = 'dashed',color = "grey")

plt.ylabel("scaled largest cluster size (n/N)")
plt.xlabel("Occupation Probability p")
plt.legend()

plt.savefig("Bond_percolation_clustersize3.png")
plt.show()
