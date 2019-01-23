import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def load_data():
    return pd.read_hdf("./raw_data/data.hdf", "master")


def correlation(master):
    preprocess = master.fillna(method='ffill')
    preprocess = preprocess[preprocess["PM25"] <= 500]
    preprocess = preprocess.groupby(preprocess.index).mean()

    corr = preprocess.corr(method='spearman')
    fig = plt.figure()
    ax = fig.add_subplot(111)

    cax = ax.matshow(corr, cmap='coolwarm', vmin=-1, vmax=1)
    fig.colorbar(cax)
    ticks = np.arange(0, len(corr.index), 1)

    ax.set_xticks(ticks)
    plt.xticks(rotation=90)

    ax.set_yticks(ticks)
    ax.set_xticklabels(corr.columns)
    ax.set_yticklabels(corr.index)
    plt.show()
    plt.show()


if __name__ == '__main__':
    master = load_data()
    correlation(master)