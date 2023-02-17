import numpy as np
from numpy import random as rd


class Ecosystem:
    def __init__(self, network, H, delay=0):
        self.time = 0
        self.H = H
        self.delay = delay
        self.network = network
        self.num_species = H.shape[0]
        self._dead_nodes = []

    
    def random_init(self):
        self.network.nodes = rd.randint(
            low=1, 
            high=self.num_species + 1,
            size=self.network.num_nodes
        )

    
    def _death(self):
        new_dead_node = rd.randint(0, self.network.num_nodes)
        self.network.nodes[new_dead_node] = 0
        self._dead_nodes.append(new_dead_node)

    
    def _reproduction(self):
        old_dead_node = self._dead_nodes.pop(0)
        connected_nodes = np.argwhere(self.network.links[old_dead_node]).squeeze()
        competing_nodes = rd.choice(connected_nodes, 2)
        competing_nodes_classes = self.network.nodes[competing_nodes]
        p = self.H[tuple(competing_nodes_classes - 1)]
        winner_node = rd.choice(competing_nodes, p=np.array([p, 1 - p]))
        self.network.nodes[old_dead_node] = self.network.nodes[winner_node]


    def evolve(self):
        self.time += 1
        self._death()
        if self.time % (self.delay + 1) == 0:
            self._reproduction()
            