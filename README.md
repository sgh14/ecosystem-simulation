# Ecosystem simulation

Simulation of competitive ecological communities of sessile individuals based on [[1]](#1).

## Set up

```
$ conda env create -f environment.yml
```

## Example

```python
import numpy as np
from matplotlib import pyplot as plt

from Network import RGG, Mesh
from Ecosystem import Ecosystem


n = 10000
nodes = np.zeros(n)
coords = np.random.rand(n, 2)
H = np.random.rand(3, 3)
r = 0.2
t = 10000

network = RGG(nodes, coords, r)
# network = Mesh(nodes, coords)
ecosystem = Ecosystem(network, H, model=1)
ecosystem.random_init()
nodes_history = ecosystem.evolve(t)

counts = np.array([np.sum(nodes_history == i, axis=1) for i in range(H.shape[0]+1)])
plt.plot(counts.T)
plt.savefig('evolution.png')
```

## References

<a id="1">[1]</a> Calleja-Solanas, V., Khalil, N., Gómez-Gardeñes, J., Hernández-García, E., & Meloni, S. (2022). Structured interactions as a stabilizing mechanism for competitive ecological communities. Physical Review E, 106(6), 064307; ArXiv:2012.14916.