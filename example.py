import numpy as np
from matplotlib import pyplot as plt

from Network import RGG, Mesh
from Ecosystem import Ecosystem_A, Ecosystem_B


n = 10000
nodes = np.zeros(n)
H = np.array([[0.50, 0.34, 0.76],
              [0.66, 0.50, 0.25],
              [0.24, 0.75, 0.50]])
r = 0.15
t = 30000

network = RGG(nodes, r) # Mesh(nodes, r)
ecosystem_A = Ecosystem_A(network, H)
ecosystem_B = Ecosystem_B(network, H)
ecosystems = {'A': ecosystem_A, 'B': ecosystem_B}
for model, ecosystem in ecosystems.items():
    ecosystem.random_init()
    nodes_hist = ecosystem.evolve(t)
    counts = np.array([np.sum(nodes_hist == i, axis=1) for i in range(H.shape[0]+1)])
    fig, ax = plt.subplots()
    ax.plot(counts.T/n)
    ax.set_xlabel('$t$')
    ax.set_ylabel('Relative abundance')
    ax.set_title('model ' + model)
    fig.savefig('images/evolution_' + model + '.png')
