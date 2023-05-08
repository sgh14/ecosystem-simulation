import numpy as np
from os import path

from Network import RGG, Mesh
from Ecosystem import Ecosystem_A, Ecosystem_B
from plot_results import plot_abundances, create_gif


n = 1000
nodes = np.zeros(n)
H = np.array([[0.50, 0.34, 0.76],
              [0.66, 0.50, 0.25],
              [0.24, 0.75, 0.50]])
r_vals = {'short': 0.03, 'long': 0.15}
t = 10000

for distance, r in r_vals.items():
    network = RGG(nodes, r) # Mesh(nodes, r)
    ecosystem_A = Ecosystem_A(network, H)
    ecosystem_B = Ecosystem_B(network, H)
    ecosystems = {'A': ecosystem_A, 'B': ecosystem_B}
    for model, ecosystem in ecosystems.items():
        ecosystem.random_init()
        nodes_hist = ecosystem.evolve(t)
        title = 'model ' + model + ' - ' + distance + f' range ($r={r}$)'
        output_path = path.join('images', 'evolution_' + model + '_' + distance)
        create_gif(ecosystem, nodes_hist, output_path + '.gif', step=500)
        plot_abundances(ecosystem, nodes_hist, title, output_path + '.png')
