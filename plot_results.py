from matplotlib import pyplot as plt
import numpy as np
import os
import imageio
import h5py


def create_gif(ecosystem, hist_output_path, output_path, step=1000):
    coords = ecosystem.network.coords
    output_root, output_extension = os.path.splitext(output_path)
    filenames = []
    with h5py.File(hist_output_path, 'r') as f:
        dataset = f['nodes_hist']
        for t in range(0, dataset.shape[0], step):
            nodes = np.array(dataset[t, :], dtype=np.int32)
            alive_nodes = np.argwhere(nodes).squeeze()
            alive_coords = coords[alive_nodes]
            colors = plt.cm.Set1(nodes[alive_nodes])
            fig, ax = plt.subplots()
            ax.set_title(f'$t={t}$')
            ax.set_aspect('equal')
            ax.set_ylim((0, 1))
            ax.set_xlim((0, 1))            
            ax.scatter(alive_coords[:, 0], alive_coords[:, 1], c=colors, s=10)
            ax.set_xlabel('$x$')
            ax.set_ylabel('$y$')
            filename = output_root + f'_{t}_' + '.png'
            filenames.append(filename)
            fig.savefig(filename)
            plt.close()      

    with imageio.get_writer(output_path, mode='I', duration=250) as writer:
        for filename in filenames:
            image = imageio.imread(filename)
            writer.append_data(image)

    for filename in set(filenames):
        os.remove(filename)


def plot_abundances(ecosystem, hist_output_path, title, output_path):
    n = ecosystem.network.num_nodes
    g = ecosystem.num_species
    with h5py.File(hist_output_path, 'r') as f:
        dataset = f['nodes_hist']
        tmax = dataset.shape[0]
        abundances = np.empty((g+1, tmax))
        for t in range(tmax):
            for i in range(g + 1):
                abundances[i, t] = np.sum(np.array(dataset[t]) == i)/n

        fig, ax = plt.subplots()
        for i in range(g + 1):
            color = plt.cm.Set1(i)
            label = 'dead' if i == 0 else f'species {i}'
            ax.plot(abundances[i], c=color, label=label)
    
    fig.legend(loc='outside upper center', ncols=4)
    ax.set_ylim((0, 1))
    ax.set_xlabel('$t$')
    ax.set_ylabel('Relative abundance')
    ax.set_title(title)
    fig.savefig(output_path)
    plt.close()
