from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
import numpy as np
import random


GENE_SIZE = 20

population = []

xy_lim = 10


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

###############################################################################
###     Individuals Part        ###

# population = [Individual() for q in range(300)]

### Use this for printing out what the inviduals array is
# print([Individual.G for Individual in population])

###############################################################################
###     SET UP FITNESS LANDSCAPE        ###

#   Set up graphing
fig = plt.figure()
fig.suptitle("Fitness Landscape")

#   Create the X and Y axes based on i and j values of the population
# x0 = [Individual.i for Individual in population]
# y0 = [Individual.j for Individual in population]
x0 = np.arange(0,GENE_SIZE,1)
y0 = np.arange(0,GENE_SIZE,1)
X0, Y0 = np.meshgrid(x0, y0)

#   Set up Z axis based on fitness values of the population
z0 = (2**X0 + 2**Y0)
# r0 = [random.uniform(0.5,1) for i in Y0]
r0 = np.random.rand(len(X0),len(X0))
for n in range(len(X0)):
        for m in range(len(X0)):
                r0[m,n] = (r0[m,n]+1)/2
Z0 = np.multiply(z0,r0)

# print (z0)
# print ((X0))
# print ((Y0))
# print ((Z0))

###############################################################################
###     Plots       ###
###############################################################################

###     FITNESS       ###
ax = fig.add_subplot(133,projection='3d')
ax.set_aspect('equal')

ax.plot_surface(X0, Y0, Z0, cmap='afmhot')
ax.title.set_text("Fitness")

###############################################################################
###     2^i + 2^j      ###

ax1 = fig.add_subplot(131,projection='3d')
ax1.set_aspect('equal')

Z1 = np.multiply(z0,[1 for i in Y0])

ax1.plot_surface(X0, Y0, Z1, cmap='afmhot')
ax1.title.set_text("2^i + 2^j")

###############################################################################
###     R(i,j)      ###

ax2 = fig.add_subplot(132,projection='3d')
ax2.set_aspect('equal')

Z2 = np.multiply(z0,r0)
Z2 = np.divide(Z2,z0)

ax2.plot_surface(X0, Y0, Z2, cmap='afmhot')
ax2.title.set_text("R(i,j)")

plt.show()
