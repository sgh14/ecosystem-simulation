import numpy as np
from numpy import random as rd


class Ecosystem:
    def __init__(self, H, delay, network):
        self.time = 0
        self.H = H
        self.delay = delay
        self.network = network
        self.num_species = H.shape[0]

    
    def random_init(self):
        self.network.nodes = rd.randint(
            low=1, 
            high=self.num_species + 1,
            size=self.network.num_nodes
        )


    def evolve(self):
        dead_node = rd.randint(0, self.network.num_nodes)
        connected_nodes = np.argwhere(self.network.links[dead_node]).squeeze()
        competing_nodes = rd.choice(connected_nodes, 2)
        competing_nodes_classes = self.network.nodes[competing_nodes]
        p = self.H[tuple(competing_nodes_classes - 1)]
        winner_node = rd.choice(competing_nodes, p=np.array([p, 1 - p]))
        self.network.nodes[dead_node] = self.network.nodes[winner_node]
        self.time += 1
            