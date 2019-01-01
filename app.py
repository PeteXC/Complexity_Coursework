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

class Individual():

        G = [0] * GENE_SIZE
        i = 0
        j = 0
        R = 0
        fit = 0

###   Init constructor to initialise attributes
        def __init__(self,ran):
                self.G = self.calc_genes()
                self.i = self.calc_i()
                self.j = self.calc_j()
                self.R = self.calc_R(ran)
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
        def calc_R(self,ran):
                return ran[self.i, self.j]

###   Calculate the fitness from the equation
        def calc_fit(self):
                return int(self.R*(2**self.i+2**self.j))

        def recalc(self, ran):
                self.i = self.calc_i()
                self.j = self.calc_j()
                self.R = self.calc_R(ran)
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
###     SET UP FITNESS LANDSCAPE        ###

#   Set up graphing
fig = plt.figure()
fig.suptitle("Fitness Landscape")

#   Create the X and Y axes based on i and j values of the population
x0 = np.arange(0, (GENE_SIZE/2)+1, 1)
y0 = np.arange(0, (GENE_SIZE/2)+1, 1)
X0, Y0 = np.meshgrid(x0, y0)

#   Set up Z axis based on fitness values of the population
z0 = (2**X0 + 2**Y0)
# r0 = [random.uniform(0.5,1) for i in Y0]
R0 = np.random.rand(len(X0),len(X0))
for n in range(len(X0)):
        for m in range(len(X0)):
                R0[m,n] = (R0[m,n]+1)/2
Z0 = np.multiply(copy.deepcopy(z0),copy.deepcopy(R0))


###############################################################################
###     Individuals Part        ###

population = [Individual(R0) for q in range(400)]
# print(vars(population[3]))
population2 = copy.deepcopy(population)

### Use this for printing out what the inviduals array is
# print([Individual.G for Individual in population])

###############################################################################
###     Population Plot (Pre)      ###
fig2 = plt.figure()

f2_ax0 = fig2.add_subplot(131,projection='3d')
f2_ax0.set_aspect('equal')

pre_popX = [Individual.i for Individual in population]
pre_popY = [Individual.j for Individual in population]
pre_popZ = [Individual.fit for Individual in population]

f2_Z0 = np.multiply(z0, copy.deepcopy(R0))

f2_ax0.plot_surface(X0, Y0, f2_Z0, cmap='copper', alpha=0.7)
f2_ax0.title.set_text("Population (Pre)")

f2_ax0.scatter(pre_popX, pre_popY, pre_popZ, marker='*')

###############################################################################
#############################       Main Loop       ####################################

fittestX = []
fittestY = []
fittestZ = []

fittest_last = population[get_Fittest(population)]

done = False

generation = 0

MAX_FITNESS = int(max(map(max, Z0)))

while not(done):

        # Select the parent from the population
        mutated_individual_index = random.randint(0,len(population)-1)
        parent = population[mutated_individual_index]

        # Mutate the parent to create a child and recalculate child values
        child = mutate(parent)
        # print(R0[child.i, child.j])
        child.recalc(R0)
        # print(child.R)

        # Choose whether to put the child back into the population
        # If the child is put back into the population then this counts as a generation
        if (child.fit > parent.fit):
                population[mutated_individual_index] = copy.deepcopy(child)
                generation += 1

        # Now find the fittest in this generation
        fittest = population[get_Fittest(population)]
        if (fittest != fittest_last):
                fittestX.append(fittest.i)
                fittestY.append(fittest.j)
                fittestZ.append(fittest.fit)
                print(fittest.fit)

        # Make sure the fittest isn't the same from last generation because plotting it isn't helpful
        fittest_last = fittest

        # Check if the population has found an individual which has a high enough fitness to consider complete
        if ((MAX_FITNESS * 0.95 < fittest.fit <= MAX_FITNESS) or (generation == 3000)):
                done = True

print(fittestX, fittestY, fittestZ)
print("Peak Fitness Possible: ", MAX_FITNESS)
print("Generation: ", generation)


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

ax1.plot_surface(X0, Y0, Z1, cmap='copper')
ax1.title.set_text("2^i + 2^j")

###############################################################################
###     R(i,j)      ###

ax2 = fig.add_subplot(132,projection='3d')
ax2.set_aspect('equal')

Z2 = np.multiply(z0, copy.deepcopy(R0))
Z2 = np.divide(Z2, copy.copy(z0))

ax2.plot_surface(X0, Y0, Z2, cmap='copper')
ax2.title.set_text("R(i,j)")

###############################################################################
###     Population Plot (Post)        ###

f2_ax1 = fig2.add_subplot(132,projection='3d')
f2_ax1.set_aspect('equal')

popX = [Individual.i for Individual in population]
popY = [Individual.j for Individual in population]
popZ = [Individual.fit for Individual in population]

f2_Z0 = np.multiply(z0, copy.deepcopy(R0))

f2_ax1.plot_surface(X0, Y0, f2_Z0, cmap='copper', alpha=0.7)
f2_ax1.title.set_text("Population (Post)")

f2_ax1.scatter(popX,popY,popZ, marker='*')

###     Hillclimber Plot         ###

f2_ax2 = fig2.add_subplot(133,projection='3d')
f2_ax2.set_aspect('equal')

hX = fittestX
hY = fittestY
hZ = fittestZ

f3_Z0 = np.multiply(z0, copy.deepcopy(R0))

f2_ax2.plot_surface(X0, Y0, f2_Z0, cmap='copper', alpha=0.7)
f2_ax2.title.set_text("Fittest Tracker")

f2_ax2.scatter(hX,hY,hZ, marker='*')

plt.show()
