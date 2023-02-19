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

    
    def _get_neighbours(self, node_index):
        linked_nodes = np.argwhere(self.network.links[node_index] != 0)
        alive_nodes = self.network.nodes[linked_nodes] != 0
        neighbours = self.network.nodes[linked_nodes[alive_nodes]]

        return neighbours
    
    
    def _competition(self, node_i, node_j):
        competing_nodes = np.array([node_i, node_j])
        competing_nodes_classes = self.network.nodes[competing_nodes]
        p = self.H[tuple(competing_nodes_classes - 1)]
        winner_node = rd.choice(competing_nodes, p=np.array([p, 1 - p]))

        return winner_node

    
    def _death(self):
        node_i = rd.randint(0, self.network.num_nodes)
        neighbours = self._get_neighbours(node_i)
        node_j = rd.choice(neighbours)
        winner_node = self._competition(node_i, node_j)
        new_dead_node = node_i if node_j == winner_node else node_j
        self.network.nodes[new_dead_node] = 0
        self._dead_nodes.append(new_dead_node)

    
    def _reproduction(self):
        old_dead_node = self._dead_nodes.pop(0)
        neighbours = self._get_neighbours(old_dead_node)
        competing_nodes = rd.choice(neighbours, 2)
        winner_node = self._competition(*competing_nodes)
        self.network.nodes[old_dead_node] = self.network.nodes[winner_node]


    def evolve(self):
        self.time += 1
        self._death()
        if self.time % (self.delay + 1) == 0:
            self._reproduction()
            