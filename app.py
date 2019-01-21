from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
import numpy as np
import random
import copy


GENE_SIZE = 40
POP_SIZE = 400
DEME_SIZE = int(POP_SIZE/20)

MUTATION_RATE = 1/GENE_SIZE

MIGRATION_RATE = 1/50
MIGRATION_INTERVAL = 30

STOP_GEN_NUM = 1000
TEST_GEN_NUM = 400

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

def mutate(par, R, mut_r):
        child = copy.deepcopy(par)
        for i in range(len(par.G)):
                if (random.random() <= (mut_r)):
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

def pipe(par1, par2, R, gene_size):
        child = copy.deepcopy(par1)
        point = random.randint(0, gene_size-1)

        # Create randomised genetic map
        random.shuffle(child.G)

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

def make_Deme(ran, gene_size, deme_size):
        return [Individual(ran, gene_size) for q in range(deme_size)]

def make_Pop(ran, gene_size, pop_size, deme_size):
        return [make_Deme(copy.deepcopy(ran), gene_size, deme_size) for i in range(int(pop_size/deme_size))]

def make_R(gene_size):
        x0 = np.arange(0, (gene_size/2)+1, 1)
        y0 = np.arange(0, (gene_size/2)+1, 1)
        Y0, X0 = np.meshgrid(x0, y0)

        R0 = np.random.rand(len(X0),len(X0))
        for n in range(len(X0)):
                for m in range(len(X0)):
                        R0[m,n] = (R0[m,n]+1)/2
        return R0

def migrate(target_deme, migrant_indexes, population, n, mig_interval):

        if (int(n)%mig_interval == 0):
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

                # Migrate the migrants to their new demes
                for r in range(len(population)):
                        population[target_deme[r]][migrant_indexes[target_deme[r]]] = copy.deepcopy(migrant_Arr[r])

def adaptive_migrate(target_deme, migrant_indexes, population, n, fittestZ, MI):
        if (int(n/10) % MI == 0):
                print("MIGRATION, INTERVAL: ", MI)
                n=0

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

                # Migrate the migrants to their new demes
                for r in range(len(population)):
                        population[target_deme[r]][migrant_indexes[target_deme[r]]] = copy.deepcopy(migrant_Arr[r])


def plot_Surface(ax, arr):

        ax.view_init(azim=-130)
        ax.plot_surface(arr[0], arr[1], arr[2], cmap='copper', alpha=0.7)

def plot_Pop(ax, pop, text):
        ax.set_aspect('equal')

        X = [Individual.i for Individual in pop]
        Y = [Individual.j for Individual in pop]
        Z = [Individual.fit for Individual in pop]

        ax.title.set_text(text)

        ax.scatter(X, Y, Z, marker='*')

        return 0

def plot_Fittest(ax, pop, arr, deme_num):

        ax.set_aspect('equal')

        ax.title.set_text("Fittest Tracker")

        ax.scatter(arr[0][deme_num], arr[1][deme_num], arr[2][deme_num], marker='*')

        return 0

def plot_Gen():

        global MIGRATION_INTERVAL

        gen_fig = plt.figure()
        gen_fig.suptitle("GA Performance")

        ax0 = gen_fig.add_subplot(121)
        ax1 = gen_fig.add_subplot(122)

        ax0.title.set_text("Uniform Crossover")
        ax1.title.set_text("Logarithmic One Point Crossover")

        ax0.set_ylabel('Generations to Peak')
        ax0.set_xlabel('n')

        ax1.set_ylabel('Logarithmic Generations to Peak')
        ax1.set_xlabel('n')

        hillclimber_gen = []
        crossover_gen = []

        hillclimber_av = []
        crossover_av = []

        hillclimber_log = []
        crossover_log = []

        n_array = []
        std_dev_hillclimber = []
        std_dev_crossover = []

        std_dev_hillclimber_log = []
        std_dev_crossover_log = []

        for gene_s in range(20, 40, 10):

                hillclimber_gen = []
                crossover_gen = []

                print("Doing Gene Size of ", gene_s)
                for iteration in range(10):

                        print("         Doing iteration ", iteration)

                        R1 = make_R(gene_s)

                        pop = make_Pop(copy.deepcopy(R1), gene_s, POP_SIZE, DEME_SIZE)

                        # Record all of the GA generation results

                        new_hill_gen = hillclimber_GA(copy.deepcopy(pop), copy.deepcopy(R1), gene_s, 1/gene_s, MIGRATION_INTERVAL)[3]
                        if (new_hill_gen <= gene_s*15):
                                hillclimber_gen.append(new_hill_gen)
                        else:
                                print("         THROWAWAY", "\n")

                        new_cross_gen = crossover_GA(copy.deepcopy(pop), copy.deepcopy(R1), gene_s, 1/gene_s, MIGRATION_INTERVAL)[3]
                        if (new_cross_gen <= gene_s*15):
                                crossover_gen.append(new_cross_gen)
                        else:
                                print("         THROWAWAY", "\n")


                # Get the averages of the GA generation results
                hillclimber_av.append(np.average(hillclimber_gen))
                crossover_av.append(np.average(crossover_gen))

                # n_array.append(gene_s/2)
                std_dev_hillclimber.append(np.std(hillclimber_gen))
                std_dev_crossover.append(np.std(crossover_gen))

        # # Logarithms
        # hillclimber_log = np.log(hillclimber_av)
        # crossover_log = np.log(crossover_av)

        # std_dev_hillclimber_log = np.log(std_dev_hillclimber)
        # std_dev_crossover_log = np.log(std_dev_crossover_log)
        n_array = np.arange(20, 20+len(hillclimber_av)*5, 5)

        ax0.errorbar(n_array, hillclimber_av, yerr=std_dev_hillclimber, fmt='-o', capsize=5)
        ax0.errorbar(n_array, crossover_av, yerr=std_dev_crossover, fmt='-x', capsize=5)

        # ax1.errorbar(n_array, hillclimber_log, yerr=std_dev_hillclimber_log, fmt='-o', capsize=5)
        # ax1.errorbar(n_array, crossover_log, yerr=std_dev_crossover_log, fmt='-x', capsize=5)

        plt.show()

def plot_Gen_migration(gene_s):
        gen_fig = plt.figure()
        gen_fig.suptitle("GA Performance Varying Migration Intervals")

        ax0 = gen_fig.add_subplot(121)
        ax1 = gen_fig.add_subplot(122)

        ax0.title.set_text("One Point Crossover")
        ax1.title.set_text("Logarithmic One Point Crossover")

        ax0.set_ylabel('Generations to Peak')
        ax0.set_xlabel('Migration Interval')

        ax1.set_ylabel('Logarithmic Generations to Peak')
        ax1.set_xlabel('Migration Interval')

        hillclimber_gen = []
        crossover_gen = []

        hillclimber_av = []
        crossover_av = []

        hillclimber_log = []
        crossover_log = []

        n_array = []
        std_dev_hillclimber = []
        std_dev_crossover = []

        std_dev_hillclimber_log = []
        std_dev_crossover_log = []

        for mig_s in range(10, 70, 10):

                hillclimber_gen = []
                crossover_gen = []

                print("Doing migration interval of ", mig_s)
                for iteration in range(20):

                        print("         Doing iteration ", iteration)

                        R1 = make_R(gene_s)

                        pop = make_Pop(copy.deepcopy(R1), gene_s, POP_SIZE, DEME_SIZE)

                        # Record all of the GA generation results

                        new_hill_gen = hillclimber_GA(copy.deepcopy(pop), copy.deepcopy(R1), gene_s, 1/gene_s, mig_s)[3]
                        if (new_hill_gen <= gene_s*15):
                                hillclimber_gen.append(new_hill_gen)
                        else:
                                print("         THROWAWAY", "\n")

                        new_cross_gen = crossover_GA(copy.deepcopy(pop), copy.deepcopy(R1), gene_s, 1/gene_s, mig_s)[3]
                        if (new_cross_gen <= gene_s*15):
                                crossover_gen.append(new_cross_gen)
                        else:
                                print("         THROWAWAY", "\n")


                # Get the averages of the GA generation results
                hillclimber_av.append(np.average(hillclimber_gen))
                crossover_av.append(np.average(crossover_gen))

                # n_array.append(gene_s/2)
                std_dev_hillclimber.append(np.std(hillclimber_gen))
                std_dev_crossover.append(np.std(crossover_gen))

        # # Logarithms
        # hillclimber_log = np.log(hillclimber_av)
        # crossover_log = np.log(crossover_av)

        # std_dev_hillclimber_log = np.log(std_dev_hillclimber)
        # std_dev_crossover_log = np.log(std_dev_crossover_log)
        n_array = np.arange(10, 10+len(hillclimber_av)*10, 10)

        ax0.errorbar(n_array, hillclimber_av, yerr=std_dev_hillclimber, fmt='-o', capsize=5)
        ax0.errorbar(n_array, crossover_av, yerr=std_dev_crossover, fmt='-x', capsize=5)

        # ax1.errorbar(n_array, hillclimber_log, yerr=std_dev_hillclimber_log, fmt='-o', capsize=5)
        # ax1.errorbar(n_array, crossover_log, yerr=std_dev_crossover_log, fmt='-x', capsize=5)

        plt.show()

def plot_Gen_mutation(gene_s):
        gen_fig = plt.figure()
        gen_fig.suptitle("GA Performance Varying Mutation Rates")

        ax0 = gen_fig.add_subplot(121)
        ax1 = gen_fig.add_subplot(122)

        ax0.title.set_text("Mutation Rates")
        ax1.title.set_text("Logarithmic One Point Crossover")

        ax0.set_ylabel('Generations to Peak')
        ax0.set_xlabel('Migration Interval')

        ax1.set_ylabel('Logarithmic Generations to Peak')
        ax1.set_xlabel('Migration Interval')

        hillclimber_gen = []
        crossover_gen = []

        hillclimber_av = []
        crossover_av = []

        hillclimber_log = []
        crossover_log = []

        n_array = []
        std_dev_hillclimber = []
        std_dev_crossover = []

        std_dev_hillclimber_log = []
        std_dev_crossover_log = []

        for mut_r in range(1, 15+1, 1):

                mut_r = mut_r/100

                hillclimber_gen = []
                crossover_gen = []

                print("Doing mutation rate of ", mut_r)
                for iteration in range(10):

                        print("         Doing iteration ", iteration, "for ", mut_r)

                        R1 = make_R(gene_s)

                        pop = make_Pop(copy.deepcopy(R1), gene_s, POP_SIZE, DEME_SIZE)

                        # Record all of the GA generation results

                        new_hill_gen = hillclimber_GA(copy.deepcopy(pop), copy.deepcopy(R1), gene_s, mut_r, 30)[3]
                        if (new_hill_gen <= gene_s*15):
                                hillclimber_gen.append(new_hill_gen)
                        else:
                                print("         THROWAWAY", "\n")

                        new_cross_gen = crossover_GA(copy.deepcopy(pop), copy.deepcopy(R1), gene_s, mut_r, 30)[3]
                        if (new_cross_gen <= gene_s*15):
                                crossover_gen.append(new_cross_gen)
                        else:
                                print("         THROWAWAY", "\n")


                # Get the averages of the GA generation results
                hillclimber_av.append(np.average(hillclimber_gen))
                crossover_av.append(np.average(crossover_gen))

                # n_array.append(gene_s/2)
                std_dev_hillclimber.append(np.std(hillclimber_gen))
                std_dev_crossover.append(np.std(crossover_gen))

        # # Logarithms
        # hillclimber_log = np.log(hillclimber_av)
        # crossover_log = np.log(crossover_av)

        # std_dev_hillclimber_log = np.log(std_dev_hillclimber)
        # std_dev_crossover_log = np.log(std_dev_crossover_log)
        n_array = np.linspace(0.01, len(hillclimber_av)*0.01, 15)
        print(n_array)

        ax0.errorbar(n_array, hillclimber_av, yerr=std_dev_hillclimber, fmt='-o', capsize=5)
        ax0.errorbar(n_array, crossover_av, yerr=std_dev_crossover, fmt='-x', capsize=5)

        # ax1.errorbar(n_array, hillclimber_log, yerr=std_dev_hillclimber_log, fmt='-o', capsize=5)
        # ax1.errorbar(n_array, crossover_log, yerr=std_dev_crossover_log, fmt='-x', capsize=5)

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

pop_init = make_Pop(copy.deepcopy(R0), GENE_SIZE, POP_SIZE, DEME_SIZE)
population_0 = copy.deepcopy(pop_init)
population_1 = copy.deepcopy(pop_init)

### Use this for printing out what the inviduals array is
# print([Individual.G for Individual in population])

###############################################################################
###             Genetic Algorithms      ###

###############################################################################
###             Hillclimber             ###

def hillclimber_GA(population, ran, gene_size, mut_r, mig_interval):

        fittestX = [[] for aa in range(len(population))]
        fittestY = [[] for bb in range(len(population))]
        fittestZ = [[] for cc in range(len(population))]
        fittest_XYZ = [[], [], []]
        fittest_arr = [[],[],[]]

        fittest = [population[i][get_Fittest(population[i])] for i in range(len(population))]
        fittest_last = [population[i][0] for i in range(len(population))]

        migrant_indexes = [0 for l in range(len(population))]
        target_deme = [l for l in range(len(population))]

        done = False

        generation_0 = 0

        migrate_count = 0

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
                                if ((fittest[p].fit >= MAX_FITNESS) or (generation_0 == gene_size*15)):
                                        done = True
                        else:
                                if (generation_0 == TEST_GEN_NUM):
                                        done = True

                migrate(target_deme, migrant_indexes, population, generation_0, mig_interval)
                # adaptive_migrate(target_deme, migrant_indexes, population, migrate_count, fittestZ, MIGRATION_INTERVAL)
                migrate_count += 1

                # # Update Migration Interval
                # if(generation_0 > 5):

                #         for z in range(len(population)):
                #                 if (fittestZ[z][-1] > fittestZ[z][-2]):
                #                         # mut_r -= (1/gene_size)/gene_size
                #                         MIGRATION_INTERVAL += 1
                #                 else:
                #                         # mut_r += (1/gene_size)/gene_size
                #                         MIGRATION_INTERVAL -= 1

                # if (MIGRATION_INTERVAL < 100):
                #         MIGRATION_INTERVAL = 100

                # if (mut_r > 0.2):
                #         mut_r = 0.2

                generation_0 += 1
                # print(generation_0, " MIGRATION_INTERVAL: ", MIGRATION_INTERVAL, "Mutate Rate: ", mut_r)
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

def crossover_GA(population, ran, gene_size, mut_r, mig_interval):

        fittestX = [[] for aa in range(len(population))]
        fittestY = [[] for bb in range(len(population))]
        fittestZ = [[] for cc in range(len(population))]
        fittest_XYZ = [[], [], []]
        fittest_arr = [[],[],[]]
        # print(fittest_arr)

        fittest = [population[i][get_Fittest(population[i])] for i in range(len(population))]
        fittest_last = [population[i][0] for i in range(len(population))]

        migrant_indexes = [0 for l in range(len(population))]
        target_deme = [l for l in range(len(population))]

        done = False

        generation_1 = 0

        migrate_count = 0

        MAX_FITNESS = int(ran[int(gene_size/2), int(gene_size/2)]*(2**(gene_size/2)+2**(gene_size/2)))

        while not(done):

                temp_population = copy.deepcopy(population)

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
                                        child = have_Sex(parent1, parent2, copy.deepcopy(ran), gene_size)#
                                        # child = pipe(parent1, parent2, copy.deepcopy(ran), gene_size)
                                        # child = bang(parent1, parent2, copy.deepcopy(ran))


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

                        # Check if the population has found an individual which has a high enough fitness to consider complete
                        if (mode == 'FPTP'):
                                if ((fittest[p].fit >= MAX_FITNESS) or (generation_1 == gene_size*15)):
                                        done = True
                        else:
                                if (generation_1 == TEST_GEN_NUM):
                                        done = True

                migrate(target_deme, migrant_indexes, population, generation_1, mig_interval)

                # adaptive_migrate(target_deme, migrant_indexes, population, migrate_count, fittestZ, MIGRATION_INTERVAL)
                migrate_count += 1

                # # Update Migration Interval
                # if(generation_1 > 5):
                #         for z in range(len(population)):
                #                 if ((fittestZ[z][-1] > fittestZ[z][-2])):
                #                         # mut_r -= (1/gene_size)/gene_size
                #                         MIGRATION_INTERVAL += 1
                #                 else:
                #                         # mut_r += (1/gene_size)/gene_size
                #                         MIGRATION_INTERVAL -= 1

                # if (MIGRATION_INTERVAL < 100):
                #         MIGRATION_INTERVAL = 100

                # if (mut_r > 0.2):
                #         mut_r = 0.2

                generation_1 += 1
                print(generation_1)
                # print(generation_1, " MIGRATION_INTERVAL: ", MIGRATION_INTERVAL, "Mutate Rate: ", mut_r)

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
        fittest_arr_0 = hillclimber_GA(population_0, copy.deepcopy(R0), GENE_SIZE, MUTATION_RATE, MIGRATION_INTERVAL)

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
        fittest_arr_1 = crossover_GA(population_1, copy.deepcopy(R0), GENE_SIZE, MUTATION_RATE, MIGRATION_INTERVAL)

        # Plot the post-evolution population sub-figure
        plot_Surface(f3_ax1, copy.deepcopy(landscape_arr))
        for tt in range(len(population_1)):
                plot_Pop(f3_ax1, population_1[tt], "Crossover (Post)")
        # plot_Pop(f3_ax1, population_1[0], "Crossover (Post)")

        # Plot the post-evolution fittest trace
        plot_Surface(f3_ax2, copy.deepcopy(landscape_arr))
        for yy in range(len(population_1)):
                plot_Fittest(f3_ax2, population_1[yy], copy.deepcopy(fittest_arr_1), yy)

do_Hillclimber()
do_Crossover()
# plot_Gen()
# plot_Gen_migration(40)
# plot_Gen_mutation(40)

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
