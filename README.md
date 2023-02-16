# Ecosystem simulation

Simulation of competitive ecological communities of sessile individuals

## Set up

```
$ conda env create -f environment.yml
```

## Example

```python
from tqdm import tqdm


n = 1000
H = np.random.rand(3, 3)
r = 0.1
delay = 4
t = 100000

network = Network(n, np.random.rand(n, 2), np.ones((n, n)))
ecosystem = Ecosystem(H, r, delay, network)
ecosystem.random_init()
for t_i in tqdm(range(t)):
    ecosystem.evolve()

results = ecosystem.network
nodes = results.nodes
coords = results.coords
```