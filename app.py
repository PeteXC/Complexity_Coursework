from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
import numpy as np
import random


GENE_SIZE = 32

population = []


###############################################################################
###     CLASSES     ###

class Individual:

    G = [0] * GENE_SIZE
    i = 0
    j = 0
    R = 0
    fit = 0

###   Init constructor to initialise attributes
    def __init__(self):
        # n = 8
        self.G = self.calc_genes()
        self.i = self.calc_i()
        self.j = self.calc_j()
        self.R = self.calc_R()
        self.fit = self.calc_fit()

###   Calculate the i value from the genes
    def calc_i(self):
        ones = 0
        arr = self.G[:int(GENE_SIZE/2)]
        for c in range(len(arr)):
            if (arr[c] == 1):
                ones += 1
        return ones

###   Calculate the j value from the genes
    def calc_j(self):
        ones = 0
        arr = self.G[int(GENE_SIZE/2):]
        for v in range(len(arr)):
            if (arr[v] == 1):
                ones += 1
        return ones

###   Generate the Genes for this individual
    def calc_genes(self):
        return np.random.randint(2, size=GENE_SIZE)

###   Generate R value to calculate the fitness
    def calc_R(self):
        return random.uniform(0.5,1)

###   Calculate the fitness from the equation
    def calc_fit(self):
        return self.R*(2**self.i+2**self.j)

###############################################################################


population = [Individual() for q in range(200)]

### Use this for printing out what the inviduals array is
# print([Individual.G for Individual in population])

#   Set up graphing
fig = plt.figure()
fl = fig.add_subplot(111,projection='3d')
fl.set_aspect('equal')
#ax.set_zlim3d(-1.5, 1.5)

#   Create the X and Y axes based on i and j values of the population
x0 = [Individual.i for Individual in population]
y0 = [Individual.j for Individual in population]
X0, Y0 = np.meshgrid(x0, y0)

#   Set up Z axis based on fitness values of the population
r0 = (2**X0 + 2**Y0)
Z0 = np.multiply(r0,[Individual.R for Individual in population])

print ((X0))
print ((Y0))
print ((Z0))

fl.plot_surface(X0, Y0, Z0, cmap='gist_heat')
fl.title("Fitness Landscape")


plt.show()
