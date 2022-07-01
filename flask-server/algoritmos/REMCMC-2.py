import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

# calculate


def distribute(x, mu, std):
    return (1/(np.sqrt(2*np.pi*std**2)))*np.exp(-(x-mu)**2/(2*std**2))

# Tptal process


node_indices = 0.2  # media partition
phi = 0.1  # phi de cada algoritmo -> sigma
time = 0.5  # tiempo de cada algoritmo -> delta
n = 3000
x = np.zeros(n)
accept = 0

for i in range(0, n-1):
    y = x[i]+np.random.uniform(-time, time)
    if np.random.rand() < min(1, distribute(y, node_indices, phi)/distribute(x[i], node_indices, phi)):
        x[i+1] = y
        accept += 1
    else:
        x[i+1] = x[i]

print("The acceptance was: ", accept/n*100, "%")

plt.hist(x, density=True, bins=30)
xs = np.linspace(-1, 1, 100)
plt.plot(xs, distribute(xs, node_indices, phi))
plt.plot(x[:1000])
