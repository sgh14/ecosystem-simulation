import numpy as np
from numpy import random as rd
from tqdm import tqdm


class Ecosystem:
    def __init__(self, network, H, model=0):
        self.time = 0
        self.H = H
        self.model = model
        self.network = network
        self.num_species = H.shape[0]

    
    def random_init(self):
        self.network.nodes = rd.randint(
            low=1, 
            high=self.num_species + 1,
            size=self.network.num_nodes
        )

    
    def _get_neighbours(self, node_index):
        linked_nodes = np.argwhere(self.network.links[node_index] != 0)
        alive_nodes = self.network.nodes[linked_nodes] != 0
        neighbours = linked_nodes[alive_nodes]

        return neighbours
    
    
    def _competition(self, node_i, node_j):
        competing_nodes = np.array([node_i, node_j])
        competing_nodes_classes = self.network.nodes[competing_nodes]
        p = self.H[tuple(competing_nodes_classes - 1)]
        winner_node = rd.choice(competing_nodes, p=np.array([p, 1 - p]))

        return winner_node

    
    def _death(self, node):
        self.network.nodes[node] = 0

    
    def _reproduction(self, node):
        try:
            neighbours = self._get_neighbours(node)
            competing_nodes = rd.choice(neighbours, 2)
            winner_node = self._competition(*competing_nodes)
            self.network.nodes[node] = self.network.nodes[winner_node]
        except:
            pass



    def time_step_A(self):
        self.time += 1
        node = rd.randint(0, self.network.num_nodes)
        if node != 0:
            self._death(node)
        else:
            self._reproduction(node)


    def time_step_B(self):
        self.time += 1
        node = rd.randint(0, self.network.num_nodes)
        self._death(node)
        self._reproduction(node)


    def evolve(self, t):
        shape = (t + 1,) + self.network.nodes.shape
        nodes_history = np.empty(shape)
        nodes_history[0] = self.network.nodes
        time_step = self.time_step_A if self.model == 0 else self.time_step_B
        for i in tqdm(range(t)):
            time_step()
            nodes_history[i+1] = self.network.nodes

        return nodes_history