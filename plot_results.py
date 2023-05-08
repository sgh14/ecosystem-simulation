from matplotlib import pyplot as plt
from matplotlib import collections as mc
import numpy as np
import os
import imageio


def create_gif(ecosystem, nodes_hist, output_path, step=100, plot_links=False):
    coords = ecosystem.network.coords
    links = ecosystem.network.links
    output_root, output_extension = os.path.splitext(output_path)
    filenames = []
    num_nodes, tmax = nodes_hist.shape
    for t in range(0, tmax, step):
        alive_nodes_ids = np.argwhere(nodes_hist[t]).squeeze()
        alive_coords = coords[alive_nodes_ids]
        alive_nodes = nodes_hist[t][alive_nodes_ids]
        fig, ax = plt.subplots()
        ax.scatter(alive_coords[:, 0], alive_coords[:, 1], c=alive_nodes, s=10)
        if plot_links:
            lines = []
            for i in range(num_nodes):
                for j in range(i):
                    if (i in alive_nodes) and (j in alive_nodes):
                        lines.append([coords[i], coords[j]])

            lc = mc.LineCollection(lines) #, colors=c, linewidths=2)
            ax.add_collection(lc)
            
        filename = output_root + f'_{t}_' + '.png'
        filenames.append(filename)
        fig.savefig(filename)

    with imageio.get_writer(output_path, mode='I') as writer:
        for filename in filenames:
            image = imageio.imread(filename)
            writer.append_data(image)

    for filename in set(filenames):
        os.remove(filename)


def plot_abundances(ecosystem, nodes_hist, title, output_path):
    n = ecosystem.network.num_nodes
    counts = np.array(
        [np.sum(nodes_hist == i, axis=1) for i in range(ecosystem.num_species+1)]
    )
    fig, ax = plt.subplots()
    ax.plot(counts.T/n)
    ax.set_xlabel('$t$')
    ax.set_ylabel('Relative abundance')
    ax.set_title(title)
    fig.savefig(output_path)