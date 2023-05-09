from matplotlib import pyplot as plt
from matplotlib import collections as mc
import numpy as np
import os
import imageio

def create_gif(ecosystem, nodes_hist, output_path, step=5000):
    coords = ecosystem.network.coords
    output_root, output_extension = os.path.splitext(output_path)
    filenames = []
    for t in range(0, nodes_hist.shape[0], step):
        alive_nodes = np.argwhere(nodes_hist[t]).squeeze()
        alive_coords = coords[alive_nodes]
        colors = [(1, 1, 1), 'b', 'r', 'y']
        my_cmap = ListedColormap(colors)
        colors = my_cmap(nodes_hist[t][alive_nodes])
        fig, ax = plt.subplots()
        ax.set_title(f'$t={t}$')
        ax.set_aspect('equal')            
        ax.scatter(alive_coords[:, 0], alive_coords[:, 1], c=colors, s=10)
        ax.set_xlabel('$x$')
        ax.set_ylabel('$y$')
        filename = output_root + f'_{t}_' + '.png'
        filenames.append(filename)
        fig.savefig(filename)
        plt.close()

    with imageio.get_writer(output_path, mode='I', duration=50) as writer:
        for filename in filenames:
            image = imageio.imread(filename)
            writer.append_data(image)

    for filename in set(filenames):
        os.remove(filename)



def plot_abundances(ecosystem, nodes_hist, title, output_path):
    n = ecosystem.network.num_nodes
    fig, ax = plt.subplots()
    for i in range(ecosystem.num_species + 1):
        abundance = np.sum(nodes_hist == i, axis=1)/n
        color = plt.cm.Set1(i)
        ax.plot(abundance, c=color)

    ax.set_xlabel('$t$')
    ax.set_ylabel('Relative abundance')
    ax.set_title(title)
    fig.savefig(output_path)
    plt.close()
