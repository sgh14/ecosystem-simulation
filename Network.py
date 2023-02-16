import numpy as np


class Network:
    def __init__(self, nodes, coords, links):
        self.nodes = np.zeros(nodes) if type(nodes)==int else nodes
        self.coords = coords
        self.links = links