from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
import numpy as np

n = 8

individuals = []

class Individual:

    def __init__(self):
        # n = 8
        G = [0] * 8
        G = self.calc_genes()
        i = self.calc_i()
        j = self.calc_j()
        R = self.calc_R()
        fit = self.calc_fit()

    def calc_i(self):
        ones = 0
        for x in self.G:
            if self.G[x]:
                ones+1
        return ones

    def calc_j(self):
        ones = 0
        for x in self.G:
            if self.G[x]:
                ones+1
        return ones

    def calc_genes(self):
        return np.random.randint(2, size=8)

    def calc_R(self):
        return np.random.randint(0.5, 1, 1)

    def calc_fit(self):
        return self.R*(2**self.i+2**self.j)


# individuals = [Individual() for x in range(5)]
a = Individual()

print(a.calc_genes())

# for x in individuals:
#     attrs = vars(individuals[x])
#     print (", ".join("%s: %s" % item for item in attrs.items()))

# fig = plt.figure()
# ax = fig.add_subplot(111,projection='3d')
# ax.set_aspect('equal')
# ax.set_zlim3d(-1.5, 1.5)

# x = np.arange(-10, 10, 0.5)
# y = np.arange(-10, 10, 0.5)
# x, y = np.meshgrid(x, y)a
# r = (np.sin(x)+np.cos(y))/10
# z = np.sin(x)*r

# ax.plot_surface(x, y, z, rstride=1, cstride=1, cmap='gist_heat')

# plt.show()