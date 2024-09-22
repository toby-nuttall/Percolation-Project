import main as m
import numpy as np
import matplotlib.pyplot as plt
import time

#defining p again for readability of code lol
p = np.linspace(0,1,1000)

def data_collection(L):

#prepare the lattice 
    m.reset(L ** 2)

# collecting the data in microcanonicle ensemble
    data = []
    for j in range(100):
        a = m.RUN(L ** 2)
        data.append(a)
        print(j)
        m.reset(L ** 2)

    data = np.array(data)
    

    Rn = []

    for k in range(L ** 2):
        a = np.where(data < k)[0]
        b = np.size(a)
    
        Rn.append(b * 0.01)
    #convolving to the Canonical ensemble
    return m.convolver(Rn)

#time how long the data takes to collect
start_time = time.time()

#call the data to be collected 
Q32 = data_collection(32)
Q64 = data_collection(64)
Q128 = data_collection(128)
Q256 = data_collection(256)

end_time = time.time()
print(f"total time ={end_time - start_time}")

#make some dotted lines for comparing to theory
d1 = np.ones(100) * 0.5927
height = np.linspace(0,1,100)

d2 = np.ones(100) * 0.69047
width = np.linspace(0,1,100)


#define the matlpotlib objects...
plt.plot(p,Q32, label = "L = 32")
plt.plot(p,Q64, label = "L = 64")
plt.plot(p,Q128, label = "L = 128")
plt.plot(p,Q256, label = "L = 256")
plt.plot(d1,height,linestyle = 'dashed',color = "grey")
plt.plot(width,d2,linestyle = 'dashed',color = "grey")

plt.xlim(0.55,0.65)

plt.ylabel("Wrapping Probability R(p)")
plt.xlabel("Occupation Probability p")
plt.legend()

plt.savefig("Site_Percolation_Plot2.png")
plt.show()


