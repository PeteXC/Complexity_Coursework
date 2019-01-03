from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
import numpy as np
import random
import copy


GENE_SIZE = 20
POP_SIZE = 400
DEME_SIZE = int(POP_SIZE/20)
MUTATION_RATE = 0.2

m = ['FPTP', 'POP']
mode = m[0]

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
                list[x] = copy.copy(pop[x].fit)
        return list.index(max(list))
        # return [i for i, j in enumerate(list) if j == max(list)]

def mutate(par, R):
        child = copy.deepcopy(par)
        for i in range(len(par.G)):
                if (random.uniform(0,1) < (MUTATION_RATE)):
                        child.G[i] = random.randint(0,1)
        child.recalc(R)
        return child

def have_Sex(par1, par2, R):
        child = copy.deepcopy(par1)
        point = random.randint(0, GENE_SIZE-1)

        # Left side of point from parent 1
        child.G[:point] = par1.G[:point]

        # Right side of point from parent 2
        child.G[point:] = par2.G[point:]

        child.recalc(R)
        return child

def make_Deme(ran):
        return [Individual(ran) for q in range(DEME_SIZE)]

def plot_Surface(ax, arr):

        ax.view_init(azim=-130)
        ax.plot_surface(arr[0], arr[1], arr[2], cmap='copper', alpha=0.7)

def plot_Pop(ax, pop, text):
        ax.set_aspect('equal')

        X = [Individual.i for Individual in pop]
        Y = [Individual.j for Individual in pop]
        Z = [Individual.fit for Individual in pop]

        # f_Z0 = np.multiply(copy.deepcopy(z0), copy.deepcopy(R0))

        # ax.view_init(azim=-130)
        # ax.plot_surface(arr[0], arr[1], arr[2], cmap='copper', alpha=0.7)
        ax.title.set_text(text)

        ax.scatter(X, Y, Z, marker='*')

        return 0

def plot_Fittest(ax, pop, arr):

        ax.set_aspect('equal')

        ax.title.set_text("Fittest Tracker")

        for i in range(len(pop)):
                ax.scatter(arr[0][i], arr[1][i], arr[2][i], marker='*')

        return 0


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

landscape_arr = [X0, Y0, Z0]

###############################################################################
###     Individuals Part        ###

# population_0 = [Individual(copy.deepcopy(R0)) for q in range(POP_SIZE)]
# population_1 = copy.deepcopy(population_0)

# w, h = int(POP_SIZE/DEME_SIZE), DEME_SIZE
# demes_0 = [[0 for x in range(w)] for y in range(h)]

# for ii in range(len(demes_0)):
#         for jj in range(len(demes_0[ii])):
#                 demes_0[ii][jj] = copy.deepcopy(population_0[ii*DEME_SIZE+jj])

# deme = [Individual(copy.deepcopy(R0)) for q in range(DEME_SIZE)]

population_0 = [make_Deme(copy.deepcopy(R0)) for i in range(int(POP_SIZE/DEME_SIZE))]
population_1 = copy.deepcopy(population_0)

print(vars(population_0[0][0]))

### Use this for printing out what the inviduals array is
# print([Individual.G for Individual in population])

###############################################################################
###     Hillclimber - Population Plot (Pre)      ###
# fig2 = plt.figure()
# fig2.suptitle("Hillclimber")

# f2_ax0 = fig2.add_subplot(131,projection='3d')
# f2_ax0.set_aspect('equal')

# pre_pop0_X = [Individual.i for Individual in population_0]
# pre_pop0_Y = [Individual.j for Individual in population_0]
# pre_pop0_Z = [Individual.fit for Individual in population_0]

# f2_Z0 = np.multiply(copy.deepcopy(z0), copy.deepcopy(R0))

# f2_ax0.view_init(azim=-130)
# f2_ax0.plot_surface(X0, Y0, f2_Z0, cmap='copper', alpha=0.7)
# f2_ax0.title.set_text("Population (Pre)")

# f2_ax0.scatter(pre_pop0_X, pre_pop0_Y, pre_pop0_Z, marker='*')


###     Crossover - Population Plot (Pre)      ###
# fig3 = plt.figure()
# fig3.suptitle("Crossover")

# f3_ax0 = fig3.add_subplot(131,projection='3d')
# f3_ax0.set_aspect('equal')

# pre_pop1_X = [Individual.i for Individual in population_1]
# pre_pop1_Y = [Individual.j for Individual in population_1]
# pre_pop1_Z = [Individual.fit for Individual in population_1]

# f3_Z0 = np.multiply(copy.deepcopy(z0), copy.deepcopy(R0))

# f3_ax0.view_init(azim=-130)
# f3_ax0.plot_surface(X0, Y0, f3_Z0, cmap='copper', alpha=0.7, rstride=1, cstride=1)
# f3_ax0.title.set_text("Population (Pre)")

# f3_ax0.scatter(pre_pop1_X, pre_pop1_Y, pre_pop1_Z, marker='*')


###############################################################################
###             Genetic Algorithms      ###

###############################################################################
###             Hillclimber             ###

def hillclimber_GA(population):

        fittestX = [[] for aa in range(len(population))]
        fittestY = [[] for bb in range(len(population))]
        fittestZ = [[] for cc in range(len(population))]
        fittest_XYZ = [[], [], []]
        fittest_arr = [[],[],[]]
        # print(fittest_arr)

        fittest = [population[i][get_Fittest(population[i])] for i in range(len(population))]
        fittest_last = [population[i][0] for i in range(len(population))]

        (print(fittest_last[bb].fit, fittest[bb].fit) for bb in range(len(population)))

        done = False

        generation_0 = 0

        MAX_FITNESS = int(max(map(max, copy.deepcopy(Z0))))

        while not(done):

                for p in range(len(population)):

                        # Select the parent from the population
                        mutated_individual_index = random.randint(0,len(population[p])-1)
                        parent = population[p][mutated_individual_index]

                        # Mutate the parent to create a child and recalculate child values
                        child = mutate(copy.deepcopy(parent), copy.deepcopy(R0))
                        # print(R0[child.i, child.j])
                        # child.recalc(copy.deepcopy(R0))
                        # print(child.R)

                        # Choose whether to put the child back into the population
                        # If the child is put back into the population then this counts as a generation
                        if (child.fit > parent.fit):
                                population[p][mutated_individual_index] = copy.deepcopy(child)
                                generation_0 += 1

                        # Now find the fittest in this generation
                        fittest[p] = population[p][get_Fittest(population[p])]

                        if (fittest[p] != fittest_last[p]):
                                fittestX[p].append(fittest[p].i)
                                fittestY[p].append(fittest[p].j)
                                fittestZ[p].append(fittest[p].fit)
                                # if (p == 0):
                                #         print(fittest_arr[p][2])
                                #         print(fittest[p].fit, "\n")

                        # Make sure the fittest isn't the same from last generation because plotting it isn't helpful
                        fittest_last[p] = fittest[p]

                        # Check if the population has found an individual which has a high enough fitness to consider complete
                        if (mode == 'FPTP'):
                                if ((fittest[p].fit == MAX_FITNESS) or (generation_0 == 3000)):
                                        done = True
                        else:
                                if (generation_0 == 1900):
                                        done = True

                # for gg in range(len(population[0])):
                #         print(population[0][gg].fit, " ", end="", flush=True)

                # print("\n", fittest[0].fit, "\n")

        fittest_arr = [fittestX, fittestY, fittestZ]

        print("------   HILLCLIMBER    ------")
        # print(fittestX)
        # print(fittestY)
        print(fittestZ)
        print("Peak Fitness Possible: ", MAX_FITNESS)
        print("Generation: ", generation_0)
        print("------   HILLCLIMBER    ------")


        return fittest_arr

###############################################################################
###             Crossover             ###

def crossover_GA(population_1):

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
                child = have_Sex(parent1, parent2, copy.deepcopy(R0))


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
                        # print(generation_1)

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
                if (mode == 'FPTP'):
                        if ((MAX_FITNESS * 0.95 < fittest_1.fit <= MAX_FITNESS) or (generation_1 == 3000)):
                                done = True
                else:
                        if (generation_1 == 1900):
                                done = True

        print("------   CROSSOVER    ------")
        print(fittestX_1, fittestY_1, fittestZ_1)
        print("Peak Fitness Possible: ", MAX_FITNESS)
        print("Generation: ", generation_1)
        print("------   CROSSOVER    ------")


###############################################################################
#############################       Main Loop       ###########################

fig2 = plt.figure()
fig2.suptitle("Hillclimber")

f2_ax0 = fig2.add_subplot(131,projection='3d')
f2_ax1 = fig2.add_subplot(132,projection='3d')
f2_ax2 = fig2.add_subplot(133,projection='3d')

# Plot the pre-evolution population sub-figure
plot_Surface(f2_ax0, copy.deepcopy(landscape_arr))
for rr in range(len(population_0)):
        plot_Pop(f2_ax0, population_0[rr], "Hillclimber (Pre)")

# Do the GA on the population
fittest_arr = hillclimber_GA(population_0)

# Plot the post-evolution population sub-figure
plot_Surface(f2_ax1, copy.deepcopy(landscape_arr))
for tt in range(len(population_0)):
        plot_Pop(f2_ax1, population_0[tt], "Hillclimber (Post)")

# Plot the post-evolution fittest trace
plot_Surface(f2_ax2, copy.deepcopy(landscape_arr))
for yy in range(len(population_0)):
        plot_Fittest(f2_ax2, population_0[yy], copy.deepcopy(fittest_arr))

###############################################################################
###     Plots       ###
###############################################################################

###############################################################################

###     FITNESS       ###
ax = fig.add_subplot(133,projection='3d')
ax.set_aspect('equal')

ax.view_init(azim=-130)
ax.plot_surface(X0, Y0, Z0, cmap='copper', rstride=1, cstride=1)
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


# ###############################################################################
# ###     Hillclimber - Population Plot (Post)        ###

# f2_ax1 = fig2.add_subplot(132,projection='3d')
# f2_ax1.set_aspect('equal')

# popX_0 = [Individual.i for Individual in population_0]
# popY_0 = [Individual.j for Individual in population_0]
# popZ_0 = [Individual.fit for Individual in population_0]

# f2_Z0 = np.multiply(copy.deepcopy(z0), copy.deepcopy(R0))

# f2_ax1.view_init(azim=-130)
# f2_ax1.plot_surface(X0, Y0, f2_Z0, cmap='copper', alpha=0.7)
# f2_ax1.title.set_text("Population (Post)")

# f2_ax1.scatter(popX_0, popY_0, popZ_0, marker='*')

# ###     Hillclimber Plot         ###

# f2_ax2 = fig2.add_subplot(133,projection='3d')
# f2_ax2.set_aspect('equal')

# hX = fittestX_0
# hY = fittestY_0
# hZ = fittestZ_0

# f2_Z0 = np.multiply(copy.deepcopy(z0), copy.deepcopy(R0))

# f2_ax2.view_init(azim=-130)
# f2_ax2.plot_surface(X0, Y0, f2_Z0, cmap='copper', alpha=0.7)
# f2_ax2.title.set_text("Fittest Tracker")

# f2_ax2.scatter(hX,hY,hZ, marker='*')


# ###############################################################################
# ###     Crossover - Population Plot (Post)        ###

# f3_ax1 = fig3.add_subplot(132,projection='3d')
# f3_ax1.set_aspect('equal')

# popX_1 = [Individual.i for Individual in population_1]
# popY_1 = [Individual.j for Individual in population_1]
# popZ_1 = [Individual.fit for Individual in population_1]

# f3_Z0 = np.multiply(copy.deepcopy(z0), copy.deepcopy(R0))

# f3_ax1.view_init(azim=-130)
# f3_ax1.plot_surface(X0, Y0, f3_Z0, cmap='copper', alpha=0.7)
# f3_ax1.title.set_text("Population (Post)")

# f3_ax1.scatter(popX_1, popY_1, popZ_1, marker='*')

# ###     Crossover Plot         ###

# f3_ax2 = fig3.add_subplot(133,projection='3d')
# f3_ax2.set_aspect('equal')

# hX_1 = fittestX_1
# hY_1 = fittestY_1
# hZ_1 = fittestZ_1

# f3_Z0 = np.multiply(copy.deepcopy(z0), copy.deepcopy(R0))

# f3_ax2.view_init(azim=-130)
# f3_ax2.plot_surface(X0, Y0, f3_Z0, cmap='copper', alpha=0.7, rstride=1, cstride=1)
# print(len(X0), len(X0[0]))
# f3_ax2.title.set_text("Fittest Tracker")

# f3_ax2.scatter(hX_1, hY_1, hZ_1, marker='*')


plt.show()
