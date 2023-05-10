import numpy as np
import os
from os import path

from Network import RGG, Mesh
from Ecosystem import Ecosystem_A, Ecosystem_B
from plot_results import plot_abundances, create_gif


os.makedirs('images', exist_ok=True)
os.makedirs('results', exist_ok=True)

n = 1000
nodes = np.zeros(n)
H = np.array([[0.50, 0.34, 0.76],
              [0.66, 0.50, 0.25],
              [0.24, 0.75, 0.50]])
r_vals = {'short': 0.03, 'long': 0.15}
t = 100*n

for dist, r in r_vals.items():
    network = RGG(nodes, r) # Mesh(nodes, r)
    ecosystem_A = Ecosystem_A(network, H)
    ecosystem_B = Ecosystem_B(network, H)
    ecosystems = {'A': ecosystem_A, 'B': ecosystem_B}
    for model, ecosystem in ecosystems.items():
        ecosystem.random_init()
        hist_output_path = path.join('results', 'evolution_' + model + '_' + dist + '.h5')
        ecosystem.evolve(t, hist_output_path)
        title = 'model ' + model + ' - ' + dist + f' range ($r={r}$)'
        img_output_path = path.join('images', 'evolution_' + model + '_' + dist)
        create_gif(ecosystem, hist_output_path, img_output_path + '.gif', step=5*n)
        plot_abundances(ecosystem, hist_output_path, title, img_output_path + '.png')
