import numpy as np
from numba import njit


class Network:
    def __init__(self, nodes, coords, links):
        self.nodes = nodes
        self.coords = coords
        self.links = links
        self.num_nodes = nodes.shape[0]


class Mesh(Network):
    def __init__(self, nodes, coords):
        n = nodes.shape[0]
        links = np.ones((n, n))
        np.fill_diagonal(links, 0)
        super().__init__(nodes, coords, links)


class RGG(Network):
    def __init__(self, nodes, coords, r):
        distances = self._get_distances(coords)
        links = distances < r
        np.fill_diagonal(links, False)
        super().__init__(nodes, coords, links)
        self.r = r


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
    