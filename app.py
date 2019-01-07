from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
import numpy as np
import random
import copy


GENE_SIZE = 20
POP_SIZE = 400
DEME_SIZE = int(POP_SIZE/20)

MUTATION_RATE = 1/GENE_SIZE

MIGRATION_RATE = 1/50

STOP_GEN_NUM = 1000
TEST_GEN_NUM = 400

# np.random.seed(0)

m = ['FPTP', 'POP']
mode = m[0]

P = ['FIRST', 'ALL']
Pmode = P[1]

xy_lim = 10


###############################################################################
###     CLASSES     ###

class Individual():

        G = []
        i = 0
        j = 0
        R = 0
        fit = 0

###   Init constructor to initialise attributes
        def __init__(self, ran, g_size):
                self.G = self.calc_genes(g_size)
                self.i = self.calc_i()
                self.j = self.calc_j()
                self.R = self.calc_R(ran)
                self.fit = self.calc_fit()

###   Calculate the i value from the genes
        def calc_i(self):
                ones = 0
                arr = self.G[:int(len(self.G)/2)]
                for c in range(len(arr)):
                        if (arr[c] == 1):
                                ones += 1
                return ones

###   Calculate the j value from the genes
        def calc_j(self):
                ones = 0
                arr = self.G[int(len(self.G)/2):]
                for v in range(len(arr)):
                        if (arr[v] == 1):
                                ones += 1
                return ones

###   Generate the Genes for this individual
        def calc_genes(self, g_size):
                return np.random.randint(2, size=g_size)

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

def mutate(par, R, mut_r):
        child = copy.deepcopy(par)
        for i in range(len(par.G)):
                if (random.random() <= (mut_r)):
                        # child.G[i] = random.randint(0,1)
                        if (child.G[i] == 1):
                                child.G[i] = 0
                        else:
                                child.G[i] = 1
        child.recalc(R)
        return child

def have_Sex(par1, par2, R, gene_size):
        child = copy.deepcopy(par1)
        point = random.randint(0, gene_size-1)

        # Left side of point from parent 1
        child.G[:point] = par1.G[:point]

        # Right side of point from parent 2
        child.G[point:] = par2.G[point:]

        child.recalc(R)
        return child

def bang(par1, par2, R):
        child = copy.deepcopy(par1)

        # Uniform crossover the child
        for i in range(len(child.G)):
                if (random.uniform(0,1) >= 50):
                        child.G[i] = par1.G[i]
                else:
                        child.G[i] = par2.G[i]

        child.recalc(R)
        return child

def make_Deme(ran, gene_size):
        return [Individual(ran, gene_size) for q in range(DEME_SIZE)]

def make_Pop(ran, gene_size):
        return [make_Deme(copy.deepcopy(ran), gene_size) for i in range(int(POP_SIZE/DEME_SIZE))]

def make_R(gene_size):
        # R0 = np.random.rand(int((gene_size/2)+1), int((gene_size/2)+1))
        # for n in range(len(R0)):
        #         for m in range(len(R0)):
        #                 R0[m,n] = (R0[m,n]+1)/2
        # print(len(R0), len(R0[0]))
        x0 = np.arange(0, (gene_size/2)+1, 1)
        y0 = np.arange(0, (gene_size/2)+1, 1)
        Y0, X0 = np.meshgrid(x0, y0)

        # r0 = [random.uniform(0.5,1) for i in Y0]
        R0 = np.random.rand(len(X0),len(X0))
        for n in range(len(X0)):
                for m in range(len(X0)):
                        R0[m,n] = (R0[m,n]+1)/2
        return R0

def migrate(target_deme, migrant_indexes, population):
        if (random.random() < MIGRATION_RATE):
                print("MIGRATION")

                # Do a same deme check
                same_Deme = True
                while (same_Deme):

                        # Shuffle the target demes
                        random.shuffle(target_deme)

                        # Check if any migrant will migrate to the same deme as it's already in, if so then reshuffle
                        for h in range(len(population)):
                                if (target_deme[h] == h):
                                        same_Deme = True
                                        break
                                else:
                                        same_Deme = False

                # Make new array of migrants
                migrant_Arr = []
                for ip in range(len(population)):
                        migrant_Arr.append(copy.deepcopy(population[ip][migrant_indexes[ip]]))
                        # print(migrant_Arr[ip].fit)
                        # print(population[ip][migrant_indexes[ip]].fit, "\n")

                # print(migrant_Arr[0].fit)
                # print(population[0][migrant_indexes[0]].fit, "\n")

                # Migrate the migrants to their new demes
                for r in range(len(population)):
                        # population[target_deme[r]][migrant_indexes[target_deme[r]]] = copy.deepcopy(population[r][migrant_indexes[r]])
                        population[target_deme[r]][migrant_indexes[target_deme[r]]] = copy.deepcopy(migrant_Arr[r])

def adaptive_migrate(target_deme, migrant_indexes, population, fittestZ):
        if (random.random() < MIGRATION_RATE):
                # print("MIGRATION")

                # Do a same deme check
                same_Deme = True
                while (same_Deme):

                        # Shuffle the target demes
                        random.shuffle(target_deme)

                        # Check if any migrant will migrate to the same deme as it's already in, if so then reshuffle
                        for h in range(len(population)):
                                if (target_deme[h] == h):
                                        same_Deme = True
                                        break
                                else:
                                        same_Deme = False

                # Make new array of migrants
                migrant_Arr = []
                for ip in range(len(population)):
                        migrant_Arr.append(copy.deepcopy(population[ip][migrant_indexes[ip]]))
                        # print(migrant_Arr[ip].fit)
                        # print(population[ip][migrant_indexes[ip]].fit, "\n")

                # print(migrant_Arr[0].fit)
                # print(population[0][migrant_indexes[0]].fit, "\n")

                # Migrate the migrants to their new demes
                for r in range(len(population)):
                        # population[target_deme[r]][migrant_indexes[target_deme[r]]] = copy.deepcopy(population[r][migrant_indexes[r]])
                        population[target_deme[r]][migrant_indexes[target_deme[r]]] = copy.deepcopy(migrant_Arr[r])


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

def plot_Fittest(ax, pop, arr, deme_num):

        ax.set_aspect('equal')

        ax.title.set_text("Fittest Tracker")

        # for i in range(len(pop)):
        ax.scatter(arr[0][deme_num], arr[1][deme_num], arr[2][deme_num], marker='*')

        return 0

def plot_Gen():
        gen_fig = plt.figure()
        gen_fig.suptitle("GA Performance")

        ax0 = gen_fig.add_subplot(121)
        ax1 = gen_fig.add_subplot(122)

        hillclimber_gen = []
        crossover_gen = []

        hillclimber_av = []
        crossover_av = []

        n_array = []
        std_dev_hillclimber = []
        std_dev_crossover = []

        for gene_s in range(10, 40, 10):

                print("Doing Gene Size of ", gene_s)
                for iteration in range(5):

                        print("         Doing iteration ", iteration)

                        R1 = make_R(gene_s)

                        # Record all of the GA generation results
                        hillclimber_gen.append(hillclimber_GA(make_Pop(copy.deepcopy(R1), gene_s), copy.deepcopy(R1), gene_s, 1/gene_s)[3])
                        crossover_gen.append(crossover_GA(make_Pop(copy.deepcopy(R1), gene_s), copy.deepcopy(R1), gene_s, 1/gene_s)[3])

                # Get the averages of the GA generation results
                hillclimber_av.append(np.average(hillclimber_gen))
                crossover_av.append(np.average(crossover_gen))

                n_array.append(gene_s/2)
                std_dev_hillclimber.append(np.std(hillclimber_gen))
                std_dev_crossover.append(np.std(crossover_gen))


        ax0.errorbar(n_array, hillclimber_av, yerr=std_dev_hillclimber, fmt='-o', capsize=5)
        ax0.errorbar(n_array, crossover_av, yerr=std_dev_crossover, fmt='-x', capsize=5)

        plt.show()


def fitness_Proportionate_Selection(pop):

        # Make an array of fitnesses and sum them
        arr_sum = sum([pop[x].fit for x in range(len(pop))])

        # Set value for the random value
        pick = random.uniform(0, arr_sum)
        current = 0

        # Proportionally pick the individual
        for Individual in pop:
                current += Individual.fit
                if (current > pick):
                        return Individual


###############################################################################
###     SET UP FITNESS LANDSCAPE        ###

#   Set up graphing
fig = plt.figure()
fig.suptitle("Fitness Landscape")

#   Create the X and Y axes based on i and j values of the population
x0 = np.arange(0, (GENE_SIZE/2)+1, 1)
y0 = np.arange(0, (GENE_SIZE/2)+1, 1)
Y0, X0 = np.meshgrid(x0, y0)

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

pop_init = make_Pop(copy.deepcopy(R0), GENE_SIZE)
population_0 = copy.deepcopy(pop_init)
population_1 = copy.deepcopy(pop_init)

### Use this for printing out what the inviduals array is
# print([Individual.G for Individual in population])

###############################################################################
###             Genetic Algorithms      ###

###############################################################################
###             Hillclimber             ###

def hillclimber_GA(population, ran, gene_size, mut_r):

        fittestX = [[] for aa in range(len(population))]
        fittestY = [[] for bb in range(len(population))]
        fittestZ = [[] for cc in range(len(population))]
        fittest_XYZ = [[], [], []]
        fittest_arr = [[],[],[]]
        # print(fittest_arr)

        print(mut_r)
        print(gene_size)
        fittest = [population[i][get_Fittest(population[i])] for i in range(len(population))]
        fittest_last = [population[i][0] for i in range(len(population))]

        migrant_indexes = [0 for l in range(len(population))]
        target_deme = [l for l in range(len(population))]

        done = False

        generation_0 = 0

        # MAX_FITNESS = int(max(map(max, copy.deepcopy(Z0))))
        MAX_FITNESS = int(ran[int(gene_size/2), int(gene_size/2)]*(2**(gene_size/2)+2**(gene_size/2)))

        while not(done):

                temp_population = copy.deepcopy(population)

                for p in range(len(population)):

                        for q in range(len(population[p])):

                                # Quick check to make sure that the fittest individual is not replaced
                                if (fittest[p] != population[p][q]):

                                        # Select the parent from the population using FPS
                                        parent = fitness_Proportionate_Selection(population[p])
                                        # Mutate the parent to create a child and recalculate child values
                                        child = mutate(copy.deepcopy(parent), copy.deepcopy(ran), mut_r)
                                        # if (child.G == parent.G).all():
                                        #         print("SAME")
                                        # else:
                                        #         print("DIFFERENT")
                                        # Always put the child back into the population, regardless if it's fitter or not
                                        # if (child.fit > parent.fit):
                                        temp_population[p][q] = copy.deepcopy(child)


                        # Now replace the old deme with the new deme
                        population[p] = copy.deepcopy(temp_population[p])

                        # Now find the fittest in this generation
                        fittest[p] = population[p][get_Fittest(population[p])]

                        if (fittest[p] != fittest_last[p]):
                                fittestX[p].append(fittest[p].i)
                                fittestY[p].append(fittest[p].j)
                                fittestZ[p].append(fittest[p].fit)

                        # Make sure the fittest isn't the same from last generation because plotting it isn't helpful
                        fittest_last[p] = fittest[p]

                        # Select a migrant, making sure that it's not the fittest individual of that deme
                        migrant_Chosen = False
                        while not(migrant_Chosen):

                                migrant_indexes[p] = random.randint(0,len(population[p])-1)

                                if (fittest[p] != population[p][migrant_indexes[p]]):
                                        migrant_Chosen = True
                                else:
                                        migrant_Chosen = False

                        # Check if the population has found an individual which has a high enough fitness to consider complete
                        if (mode == 'FPTP'):
                                if ((fittest[p].fit == MAX_FITNESS) or (generation_0 == gene_size*12)):
                                        done = True
                        else:
                                if (generation_0 == TEST_GEN_NUM):
                                        done = True

                migrate(target_deme, migrant_indexes, population)

                generation_0 += 1
                print(generation_0)

        fittest_arr = [fittestX, fittestY, fittestZ, generation_0]

        print("------   HILLCLIMBER    ------")
        print(fittestZ)
        print("Peak Fitness Possible: ", MAX_FITNESS)
        print("Generation: ", generation_0)
        print("------   HILLCLIMBER    ------")


        return fittest_arr

###############################################################################
###             Crossover             ###

def crossover_GA(population, ran, gene_size, mut_r):

        fittestX = [[] for aa in range(len(population))]
        fittestY = [[] for bb in range(len(population))]
        fittestZ = [[] for cc in range(len(population))]
        fittest_XYZ = [[], [], []]
        fittest_arr = [[],[],[]]
        # print(fittest_arr)

        fittest = [population[i][get_Fittest(population[i])] for i in range(len(population))]
        fittest_last = [population[i][0] for i in range(len(population))]

        # (print(fittest_last[bb].fit, fittest[bb].fit) for bb in range(len(population)))

        migrant_indexes = [0 for l in range(len(population))]
        target_deme = [l for l in range(len(population))]
        # print(target_deme)

        print(mut_r)
        print(gene_size)

        done = False

        generation_1 = 0

        # MAX_FITNESS = int(max(map(max, copy.deepcopy(Z0))))
        MAX_FITNESS = int(ran[int(gene_size/2), int(gene_size/2)]*(2**(gene_size/2)+2**(gene_size/2)))

        while not(done):

                temp_population = copy.deepcopy(population)

                # for it in range(len(population[0])):
                #         print(population[0][it].fit, end=', ')
                # print("\n")

                for p in range(len(population)):

                        for q in range(len(population[p])):

                                select = False

                                # Quick check to make sure that the fittest individual is not replaced
                                if (fittest[p] != population[p][q]):

                                        # Make sure not to select the same parent
                                        while not(select):

                                                # Use FPS to select parent 1
                                                parent1 = fitness_Proportionate_Selection(population[p])

                                                # Use FPS to select parent 2
                                                parent2 = fitness_Proportionate_Selection(population[p])

                                                # Make sure the same parent isn't chosen
                                                if (parent1 != parent2):
                                                        select = True

                                        # Perform crossover on the two parents to generate a child
                                        child = have_Sex(parent1, parent2, copy.deepcopy(ran), gene_size)


                                        # Mutate the child to create a mutated child to put back into population
                                        mutant_child = mutate(child, copy.deepcopy(ran), mut_r)

                                        # Always put the child into the population regardless of its fitness
                                        temp_population[p][q] = copy.deepcopy(copy.deepcopy(mutant_child))


                        # Now replace the old deme with the new deme
                        population[p] = copy.deepcopy(temp_population[p])

                        # Now find the fittest in this generation
                        fittest[p] = population[p][get_Fittest(population[p])]

                        if (fittest[p] != fittest_last[p]):
                                fittestX[p].append(fittest[p].i)
                                fittestY[p].append(fittest[p].j)
                                fittestZ[p].append(fittest[p].fit)


                        # Make sure the fittest isn't the same from last generation because plotting it isn't helpful
                        fittest_last[p] = fittest[p]

                        # Select a migrant, making sure that it's not the fittest individual of that deme
                        migrant_Chosen = False
                        while not(migrant_Chosen):

                                migrant_indexes[p] = random.randint(0,len(population[p])-1)

                                if (fittest[p] != population[p][migrant_indexes[p]]):
                                        migrant_Chosen = True
                                else:
                                        migrant_Chosen = False

                                # print(population[p][migrant_indexes[p]].fit)
                                # print(fittest[p].fit, "\n")

                        # Check if the population has found an individual which has a high enough fitness to consider complete
                        if (mode == 'FPTP'):
                                if ((fittest[p].fit == MAX_FITNESS) or (generation_1 == gene_size*12)):
                                        done = True
                        else:
                                if (generation_1 == TEST_GEN_NUM):
                                        done = True


                migrate(target_deme, migrant_indexes, population)

                generation_1 += 1
                print(generation_1)
                # print(population[0][get_Fittest(copy.deepcopy(population[0]))].fit)
                # print(population[0][migrant_indexes[0]].fit)
                # for it in range(len(population[0])):
                #         print(population[0][it].fit, end = ', ')
                # print("\n\n")
                # print(population[0][migrant_indexes[0]].fit)
                # print(migrant_Arr[0].fit)
                # print(population[target_deme[0]][migrant_indexes[target_deme[0]]].fit, "\n\n")

        fittest_arr = [fittestX, fittestY, fittestZ, generation_1]

        print("------   CROSSOVER    ------")
        print(fittestZ)
        print("Peak Fitness Possible: ", MAX_FITNESS)
        print("Generation: ", generation_1)
        print("------   CROSSOVER    ------")

        return fittest_arr


###############################################################################
#############################       Main Loop       ###########################


# plot_Gen()


# HILLCLIMBER
def do_Hillclimber():

        fig2 = plt.figure()
        fig2.suptitle("Hillclimber")

        f2_ax0 = fig2.add_subplot(131,projection='3d')
        f2_ax1 = fig2.add_subplot(132,projection='3d')
        f2_ax2 = fig2.add_subplot(133,projection='3d')

        # Plot the pre-evolution population sub-figure
        plot_Surface(f2_ax0, copy.deepcopy(landscape_arr))

        if Pmode == "ALL":
                for rr in range(len(population_0)):
                        plot_Pop(f2_ax0, population_0[rr], "Hillclimber (Pre)")
        else:
                plot_Pop(f2_ax0, population_0[0], "Hillclimber (Pre)")

        # Do the GA on the population
        fittest_arr_0 = hillclimber_GA(population_0, copy.deepcopy(R0), GENE_SIZE, MUTATION_RATE)

        # Plot the post-evolution population sub-figure
        plot_Surface(f2_ax1, copy.deepcopy(landscape_arr))
        if Pmode == "ALL":
                for tt in range(len(population_0)):
                        plot_Pop(f2_ax1, population_0[tt], "Hillclimber (Post)")
        else:
                plot_Pop(f2_ax1, population_0[0], "Hillclimber (Post)")

        # Plot the post-evolution fittest trace
        plot_Surface(f2_ax2, copy.deepcopy(landscape_arr))
        for yy in range(len(population_0)):
                plot_Fittest(f2_ax2, population_0[yy], copy.deepcopy(fittest_arr_0), yy)

#------------------------------------------------------------------------------#

# CROSSOVER
def do_Crossover():
        fig3 = plt.figure()
        fig3.suptitle("Crossover")

        f3_ax0 = fig3.add_subplot(131,projection='3d')
        f3_ax1 = fig3.add_subplot(132,projection='3d')
        f3_ax2 = fig3.add_subplot(133,projection='3d')

        # Plot the pre-evolution population sub-figure
        plot_Surface(f3_ax0, copy.deepcopy(landscape_arr))
        for rr in range(len(population_1)):
                plot_Pop(f3_ax0, population_1[rr], "Crossover (Pre)")
        # plot_Pop(f3_ax0, population_1[0], "Crossover (Pre)")

        # Do the GA on the population
        fittest_arr_1 = crossover_GA(population_1, copy.deepcopy(R0), GENE_SIZE, MUTATION_RATE)

        # Plot the post-evolution population sub-figure
        plot_Surface(f3_ax1, copy.deepcopy(landscape_arr))
        for tt in range(len(population_1)):
                plot_Pop(f3_ax1, population_1[tt], "Crossover (Post)")
        # plot_Pop(f3_ax1, population_1[0], "Crossover (Post)")

        # Plot the post-evolution fittest trace
        plot_Surface(f3_ax2, copy.deepcopy(landscape_arr))
        for yy in range(len(population_1)):
                plot_Fittest(f3_ax2, population_1[yy], copy.deepcopy(fittest_arr_1), yy)

# do_Hillclimber()
# do_Crossover()
plot_Gen()

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

plt.show()
