# Ecosystem simulation

Simulation of competitive ecological communities of sessile individuals

## Set up

```
$ conda env create -f environment.yml
```

## Example

```python
import numpy as np
from tqdm import tqdm

from Network import RGG, Mesh
from Ecosystem import Ecosystem


n = 1000
nodes = np.zeros(n)
coords = np.random.rand(n, 2)
H = np.random.rand(3, 3)
r = 0.1
delay = 4
t = 100000

network = RGG(nodes, coords, r)
# network = Mesh(nodes, coords)
ecosystem = Ecosystem(network, H, delay)
ecosystem.random_init()
for _ in tqdm(range(t)):
    ecosystem.evolve()

results = ecosystem.network
nodes = results.nodes
coords = results.coords
```