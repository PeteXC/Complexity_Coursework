from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
import numpy as np
import random
import copy


GENE_SIZE = 20
MUTATION_RATE = 0.08

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
        return list.index(max(list))
        # return [i for i, j in enumerate(list) if j == max(list)]

def mutate(par, R):
        child = copy.deepcopy(par)
        for i in range(len(par.G)):
                if (random.uniform(0,1) < (MUTATION_RATE)):
                        child.G[i] = random.randint(0,1)
        child.recalc(R)
        return child

def have_sex(par1, par2, R):
        child = copy.deepcopy(par1)
        point = random.randint(0, GENE_SIZE-1)

        # Left side of point from parent 1
        child.G[:point] = par1.G[:point]

        # Right side of point from parent 2
        child.G[point:] = par2.G[point:]

        child.recalc(R)
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

population_0 = [Individual(copy.deepcopy(R0)) for q in range(400)]
population_1 = copy.deepcopy(population_0)

### Use this for printing out what the inviduals array is
# print([Individual.G for Individual in population])

###############################################################################
###     Hillclimber - Population Plot (Pre)      ###
fig2 = plt.figure()
fig2.suptitle("Hillclimber")

f2_ax0 = fig2.add_subplot(131,projection='3d')
f2_ax0.set_aspect('equal')

pre_pop0_X = [Individual.i for Individual in population_0]
pre_pop0_Y = [Individual.j for Individual in population_0]
pre_pop0_Z = [Individual.fit for Individual in population_0]

f2_Z0 = np.multiply(copy.deepcopy(z0), copy.deepcopy(R0))

f2_ax0.view_init(azim=-130)
f2_ax0.plot_surface(X0, Y0, f2_Z0, cmap='copper', alpha=0.7)
f2_ax0.title.set_text("Population (Pre)")

f2_ax0.scatter(pre_pop0_X, pre_pop0_Y, pre_pop0_Z, marker='*')


###     Crossover - Population Plot (Pre)      ###
fig3 = plt.figure()
fig.suptitle("Crossover")

f3_ax0 = fig3.add_subplot(131,projection='3d')
f3_ax0.set_aspect('equal')

pre_pop1_X = [Individual.i for Individual in population_1]
pre_pop1_Y = [Individual.j for Individual in population_1]
pre_pop1_Z = [Individual.fit for Individual in population_1]

f3_Z0 = np.multiply(copy.deepcopy(z0), copy.deepcopy(R0))

f3_ax0.view_init(azim=-130)
f3_ax0.plot_surface(X0, Y0, f3_Z0, cmap='copper', alpha=0.7)
f3_ax0.title.set_text("Population (Pre)")

f3_ax0.scatter(pre_pop1_X, pre_pop1_Y, pre_pop1_Z, marker='*')


###############################################################################
#############################       Main Loops       ##########################

###############################################################################
###             Hillclimber             ###

fittestX_0 = []
fittestY_0 = []
fittestZ_0 = []

fittest_last = population_0[get_Fittest(population_0)]

done = False

generation_0 = 0

MAX_FITNESS = int(max(map(max, Z0)))

while not(done):

        # Select the parent from the population
        mutated_individual_index = random.randint(0,len(population_0)-1)
        parent = population_0[mutated_individual_index]

        # Mutate the parent to create a child and recalculate child values
        child = mutate(parent, copy.deepcopy(R0))
        # print(R0[child.i, child.j])
        # child.recalc(copy.deepcopy(R0))
        # print(child.R)

        # Choose whether to put the child back into the population
        # If the child is put back into the population then this counts as a generation
        if (child.fit > parent.fit):
                population_0[mutated_individual_index] = copy.deepcopy(child)
                generation_0 += 1

        # Now find the fittest in this generation
        fittest = population_0[get_Fittest(population_0)]
        if (fittest != fittest_last):
                fittestX_0.append(fittest.i)
                fittestY_0.append(fittest.j)
                fittestZ_0.append(fittest.fit)
                print(fittest.fit)

        # Make sure the fittest isn't the same from last generation because plotting it isn't helpful
        fittest_last = fittest

        # Check if the population has found an individual which has a high enough fitness to consider complete
        if ((MAX_FITNESS * 0.95 < fittest.fit <= MAX_FITNESS) or (generation_0 == 3000)):
                done = True

print("------   HILLCLIMBER    ------")
print(fittestX_0, fittestY_0, fittestZ_0)
print("Peak Fitness Possible: ", MAX_FITNESS)
print("Generation: ", generation_0)
print("------   HILLCLIMBER    ------")

###############################################################################
###             Crossover             ###

fittestX_1 = []
fittestY_1 = []
fittestZ_1 = []

fittest_last_1 = population_1[get_Fittest(population_1)]

done = False

generation_1 = 0

MAX_FITNESS = int(max(map(max, Z0)))

while not(done):

        select = False
        select1 = False
        select2 = False

        # Make sure not to select the same parent
        while not(select):

                # Select two individuals to fight to be the first parent from the population
                while not(select1):
                        a = population_1[random.randint(0,len(population_1)-1)]
                        b = population_1[random.randint(0,len(population_1)-1)]

                        if (a != b):
                                if (a.fit > b.fit):
                                        parent1 = copy.deepcopy(a)
                                else:
                                        parent1 = copy.deepcopy(b)
                                select1 = True

                # Select two individuals to fight to be the second parent from the population
                while not(select2):
                        a = population_1[random.randint(0,len(population_1)-1)]
                        b = population_1[random.randint(0,len(population_1)-1)]

                        if (a != b):
                                if (a.fit > b.fit):
                                        parent2 = copy.deepcopy(a)
                                else:
                                        parent2 = copy.deepcopy(b)
                                select2 = True

                if (parent1 != parent2):
                        select = True

        # Perform crossover on the two parents to generate a child
        child = have_sex(parent1, parent2, copy.deepcopy(R0))


        # Mutate the child to create a mutated child to put back into population
        mutant_child = mutate(child, copy.deepcopy(R0))

        # Choose whether to put the child back into the population
        # If the child is put back into the population then this counts as a generation

        l_select = False

        # Select two individuals to fight to see who gets replaced from the population
        while not(l_select):
                a = random.randint(0,len(population_1)-1)
                b = random.randint(0,len(population_1)-1)

                if (a != b):
                        if (population_1[a].fit > population_1[b].fit):
                                loser = a
                        else:
                                loser = b
                        l_select = True

        # Check if the loser can be replaced, and replace it
        if (mutant_child.fit > population_1[loser].fit):
                population_1[loser] = copy.deepcopy(mutant_child)
                generation_1 += 1

        # Now find the fittest in this generation
        fittest_1 = population_1[get_Fittest(population_1)]
        if (fittest_1 != fittest_last_1):
                fittestX_1.append(fittest_1.i)
                fittestY_1.append(fittest_1.j)
                fittestZ_1.append(fittest_1.fit)
                print(fittest_1.fit)

        # Make sure the fittest isn't the same from last generation because plotting it isn't helpful
        fittest_last_1 = fittest_1

        # Check if the population has found an individual which has a high enough fitness to consider complete
        if ((MAX_FITNESS * 0.95 < fittest_1.fit <= MAX_FITNESS) or (generation_1 == 3000)):
                done = True

print("------   CROSSOVER    ------")
print(fittestX_1, fittestY_1, fittestZ_1)
print("Peak Fitness Possible: ", MAX_FITNESS)
print("Generation: ", generation_1)
print("------   CROSSOVER    ------")


###############################################################################
###     Plots       ###
###############################################################################

###############################################################################

###     FITNESS       ###
ax = fig.add_subplot(133,projection='3d')
ax.set_aspect('equal')

ax.view_init(azim=-130)
ax.plot_surface(X0, Y0, Z0, cmap='copper')
ax.title.set_text("Fitness")


###############################################################################
###     2^i + 2^j      ###

ax1 = fig.add_subplot(131,projection='3d')
ax1.set_aspect('equal')

Z1 = np.multiply(copy.deepcopy(z0),[1 for i in Y0])

ax1.view_init(azim=-130)
ax1.plot_surface(X0, Y0, Z1, cmap='copper')
ax1.title.set_text("2^i + 2^j")


###############################################################################
###     R(i,j)      ###

ax2 = fig.add_subplot(132,projection='3d')
ax2.set_aspect('equal')

Z2 = np.multiply(copy.deepcopy(z0), copy.deepcopy(R0))
Z2 = np.divide(Z2, copy.deepcopy(z0))

ax2.view_init(azim=-130)
ax2.plot_surface(X0, Y0, Z2, cmap='copper')
ax2.title.set_text("R(i,j)")


###############################################################################
###     Hillclimber - Population Plot (Post)        ###

f2_ax1 = fig2.add_subplot(132,projection='3d')
f2_ax1.set_aspect('equal')

popX_0 = [Individual.i for Individual in population_0]
popY_0 = [Individual.j for Individual in population_0]
popZ_0 = [Individual.fit for Individual in population_0]

f2_Z0 = np.multiply(copy.deepcopy(z0), copy.deepcopy(R0))

f2_ax1.view_init(azim=-130)
f2_ax1.plot_surface(X0, Y0, f2_Z0, cmap='copper', alpha=0.7)
f2_ax1.title.set_text("Population (Post)")

f2_ax1.scatter(popX_0, popY_0, popZ_0, marker='*')

###     Hillclimber Plot         ###

f2_ax2 = fig2.add_subplot(133,projection='3d')
f2_ax2.set_aspect('equal')

hX = fittestX_0
hY = fittestY_0
hZ = fittestZ_0

f2_Z0 = np.multiply(copy.deepcopy(z0), copy.deepcopy(R0))

f2_ax2.view_init(azim=-130)
f2_ax2.plot_surface(X0, Y0, f2_Z0, cmap='copper', alpha=0.7)
f2_ax2.title.set_text("Fittest Tracker")

f2_ax2.scatter(hX,hY,hZ, marker='*')


###############################################################################
###     Crossover - Population Plot (Post)        ###

f3_ax1 = fig3.add_subplot(132,projection='3d')
f3_ax1.set_aspect('equal')

popX_1 = [Individual.i for Individual in population_1]
popY_1 = [Individual.j for Individual in population_1]
popZ_1 = [Individual.fit for Individual in population_1]

f3_Z0 = np.multiply(copy.deepcopy(z0), copy.deepcopy(R0))

f3_ax1.view_init(azim=-130)
f3_ax1.plot_surface(X0, Y0, f3_Z0, cmap='copper', alpha=0.7)
f3_ax1.title.set_text("Population (Post)")

f3_ax1.scatter(popX_1, popY_1, popZ_1, marker='*')

###     Crossover Plot         ###

f3_ax2 = fig3.add_subplot(133,projection='3d')
f3_ax2.set_aspect('equal')

hX_1 = fittestX_1
hY_1 = fittestY_1
hZ_1 = fittestZ_1

f3_Z0 = np.multiply(copy.deepcopy(z0), copy.deepcopy(R0))

f3_ax2.view_init(azim=-130)
f3_ax2.plot_surface(X0, Y0, f3_Z0, cmap='copper', alpha=0.7)
f3_ax2.title.set_text("Fittest Tracker")

f3_ax2.scatter(hX_1, hY_1, hZ_1, marker='*')


plt.show()
