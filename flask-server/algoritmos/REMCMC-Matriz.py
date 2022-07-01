import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

node_indices = (0, 1, 2)  # media partition
phi = 0.1  # phi de cada algoritmo -> sigma
time = 0.5  # tiempo de cada algoritmo -> delta
x = np.array([
    [0, 0, 0],
    [0, 0, 0],
    [1, 0, 1],
    [0, 0, 1],
    [0, 0, 1],
    [1, 1, 1],
    [1, 0, 0],
    [0, 1, 0]
])


def distribute(node_indices, x, phi, time):
    hoña = []
    hoña2 = []
    for i in range(0, len(x)):
        xc = np.random.normal(x[i], 0.5)
        print("Current value = ", x[i], " proposed value = ", xc)
        hoña.append([xc[0],xc[1],xc[2]])
        var = (norm.pdf(xc, node_indices, time) /
              norm.pdf(x[i], node_indices, phi))
        print("Reason =", var)
        hoña2.append([var[0],var[1],var[2]])
    print("Hoña = ", hoña)
    print("Hoña2 = ", hoña2)


distribute(node_indices, x, phi, time)
