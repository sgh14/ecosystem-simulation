import numpy as np
from numpy import random as rd
from numba import njit


class Ecosystem:
    def __init__(self, H, r, delay, network):
        self.time = 0
        self.H = H
        self.r = r
        self.delay = delay
        self.network = network
        self.num_species = H.shape[0]
        self.num_nodes = len(self.network.nodes)

    
    def _fill_nodes(self):
        self.network.nodes = rd.randint(
            low=1, 
            high=self.num_species + 1,
            size=self.num_nodes
        )

    
    @staticmethod
    @njit
    def _get_distances(coords):
        num_nodes = coords.shape[0]
        distances = np.zeros((num_nodes, num_nodes))
        for i in range(num_nodes):
            for j in range(i):
                d = np.sqrt(np.sum((coords[i] - coords[j])**2))
                distances[i, j] = distances[j, i] = d

        return distances


    def _create_links(self):
        distances = self._get_distances(self.network.coords)
        self.network.links = distances < self.r
    

    def random_init(self):
        self._fill_nodes()
        self._create_links()
        

    def evolve(self):
        dead_node = rd.randint(0, self.num_nodes)
        connected_nodes = np.argwhere(self.network.links[dead_node]).squeeze()
        competing_nodes = rd.choice(connected_nodes, 2)
        competing_nodes_classes = self.network.nodes[competing_nodes]
        p = self.H[tuple(competing_nodes_classes - 1)]
        winner_node = rd.choice(competing_nodes, p=np.array([p, 1 - p]))
        self.network.nodes[dead_node] = self.network.nodes[winner_node]
        self.time += 1
            