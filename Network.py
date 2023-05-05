import numpy as np
from numba import njit


class Network:
    def __init__(self, nodes, coords, links):
        self.nodes = nodes
        self.coords = coords
        self.links = links
        self.num_nodes = nodes.shape[0]


class Interaction_Network(Network):
    def __init__(self, nodes, coords, r):
        distances = self._get_distances(coords)
        links = self._get_links(distances, r)
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
    

    @staticmethod
    def _get_links(distances, r):
        links = distances < r
        np.fill_diagonal(links, False)

        return links


class Mesh(Interaction_Network):
    def __init__(self, nodes, r):
        n = nodes.shape[0]
        coords = self._get_coords(n)
        super().__init__(nodes, coords, r)

    
    @staticmethod
    def _get_coords(n):
        x = y = np.linspace(0, 1, np.ceil(np.sqrt(n)).astype(np.int32))
        X, Y = np.meshgrid(x, y)
        coords = np.stack([X.flat, Y.flat], axis=1)[:n]

        return coords


class RGG(Interaction_Network):
    def __init__(self, nodes, r):
        n = nodes.shape[0]
        coords = self._get_coords(n)
        super().__init__(nodes, coords, r)
    
    @staticmethod
    def _get_coords(n):
        coords = np.random.rand(n, 2)

        return coords