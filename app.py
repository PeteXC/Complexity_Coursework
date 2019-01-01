from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
import numpy as np
import random
import copy


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
                return int(self.R*(2**self.i+2**self.j))

        def recalc(self):
                self.i = self.calc_i()
                self.j = self.calc_j()
                self.fit = self.calc_fit()
                return 0


###############################################################################
###     Functions       ###

def get_Fittest(pop):
        list = [0] * len(pop)
        for x in range(len(pop)):
                list[x] = pop[x].fit
        # return [i for i, j in enumerate(list) if j == max(list)]
        return list.index(max(list))

def mutate(par):
        child = copy.deepcopy(par)
        for i in range(len(par.G)):
                if (random.uniform(0,1) < (0.1)):
                        child.G[i] = random.randint(0,1)
        return child

###############################################################################
###     Individuals Part        ###

population = [Individual() for q in range(400)]

### Use this for printing out what the inviduals array is
# print([Individual.G for Individual in population])

###############################################################################
#############################       Main Loop       ####################################

fittestX = []
fittestY = []
fittestZ = []

fittest_last = population[get_Fittest(population)]

done = False

generation = 0

while not(done):
        # Fittest_list = get_Fittest(population)
        # print(Fittest_list)
        # for i in Fittest_list:
        #         fittest.append(population[Fittest_list[i]])
        # print(fittest)

        mutated_individual_index = random.randint(0,len(population)-1)
        # print(mutated_individual_index)
        parent = population[mutated_individual_index]
        child = mutate(parent)
        child.recalc()
        # print(parent.fit)
        # print(child.fit)

        if (child.fit > parent.fit):
                population[mutated_individual_index] = child
                generation += 1

        fittest = population[get_Fittest(population)]
        if (fittest != fittest_last):
                fittestX.append(fittest.i)
                fittestY.append(fittest.j)
                fittestZ.append(fittest.fit)
                # print(fittest.fit)

        fittest_last = fittest

        if ((2**(GENE_SIZE/2)+2**(GENE_SIZE/2))*0.9 < fittest.fit < 2**(GENE_SIZE/2)+2**(GENE_SIZE/2)):
                done = True

print(fittestX, fittestY, fittestZ)

print("Generation: ", generation)

###############################################################################
###     SET UP FITNESS LANDSCAPE        ###

#   Set up graphing
fig = plt.figure()
fig.suptitle("Fitness Landscape")

#   Create the X and Y axes based on i and j values of the population
# x0 = [Individual.i for Individual in population]
# y0 = [Individual.j for Individual in population]
x0 = np.arange(0, GENE_SIZE/2, 1)
y0 = np.arange(0, GENE_SIZE/2, 1)
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

###############################################################################

###     FITNESS       ###
ax = fig.add_subplot(133,projection='3d')
ax.set_aspect('equal')

ax.plot_surface(X0, Y0, Z0, cmap='copper')
ax.title.set_text("Fitness")


###############################################################################
###     2^i + 2^j      ###

ax1 = fig.add_subplot(131,projection='3d')
ax1.set_aspect('equal')

Z1 = np.multiply(z0,[1 for i in Y0])

ax1.plot_surface(X0, Y0, Z1, cmap='copper', alpha=0.7)
ax1.title.set_text("2^i + 2^j")

###############################################################################
###     R(i,j)      ###

ax2 = fig.add_subplot(132,projection='3d')
ax2.set_aspect('equal')

Z2 = np.multiply(z0,r0)
Z2 = np.divide(Z2,z0)

ax2.plot_surface(X0, Y0, Z2, cmap='copper')
ax2.title.set_text("R(i,j)")

###############################################################################
###     Population Plot         ###

fig2 = plt.figure()
f2_ax = fig2.add_subplot(111,projection='3d')
f2_ax.set_aspect('equal')

popX = [Individual.i for Individual in population]
popY = [Individual.j for Individual in population]
popZ = [Individual.fit for Individual in population]

f2_Z0 = np.multiply(z0,[0.5 for i in Y0])

f2_ax.plot_surface(X0, Y0, f2_Z0, cmap='copper', alpha=0.5)
f2_ax.title.set_text("Population")

f2_ax.scatter(popX,popY,popZ, marker='*')

###     Hillclimber Plot         ###

fig3 = plt.figure()
f3_ax = fig3.add_subplot(111,projection='3d')
f3_ax.set_aspect('equal')

hX = fittestX
hY = fittestY
hZ = fittestZ

f3_Z0 = np.multiply(z0,[1 for i in Y0])

f3_ax.plot_surface(X0, Y0, f2_Z0, cmap='copper', alpha=0.5)
f3_ax.title.set_text("Population")

f3_ax.scatter(hX,hY,hZ, marker='*')

plt.show()
