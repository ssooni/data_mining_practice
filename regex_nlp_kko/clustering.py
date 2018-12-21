from sklearn.cluster import DBSCAN
from gensim.models import Word2Vec

import pandas as pd
import re

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm


def cluster():
    model = Word2Vec.load("./result/embedding.model")
    word_vector = model.wv.vectors
    match_index = model.wv.index2word
    print(len(match_index))
    model.init_sims(replace=True)

    # 두 글자이상 한글인 경우만 사용
    han = re.compile(r"[가-힣]{2,}")

    for min_sample in range(3, 9):
        dbscan = DBSCAN(eps=0.675, min_samples=min_sample)

        clusters = dbscan.fit_predict(word_vector)
        c = pd.DataFrame(clusters, columns=["cluster"], index=match_index)

        c = pd.DataFrame(c.reset_index())
        print(c.T.unstack())

        c = c[c["index"].apply(lambda x: len(han.findall(x)) > 0)]
        c = c[c["cluster"] != -1]
        print(c.groupby(["cluster"]).count())

        c.to_excel(pd.ExcelWriter("./result/cluster_eps_%s.xlsx" % min_sample), index=False)


def plot():
    clstr = pd.read_excel(pd.ExcelFile("./result/DBSCAN_eps0.75/cluster_eps_4.xlsx"))
    min_cluster = clstr["cluster"].min()
    max_cluster = clstr["cluster"].max()

    print(min_cluster, max_cluster)
    for clstr_num in range(min_cluster, max_cluster + 1):
        clstr_index = clstr[clstr["cluster"] == clstr_num].index
        clstr.loc[clstr_index, "value"] = list(range(0, len(clstr_index) * 3, 3))

    print(clstr)
    font = fm.FontProperties(fname="./font/NanumBrush.ttf", size=15)

    fig, ax = plt.subplots()
    clstr.plot.scatter(x="cluster", y="value", ax=ax)
    clstr[["cluster", "value", "index"]].apply(lambda x: ax.text(*x, fontproperties=font), axis=1)
    plt.show()


if __name__ == '__main__':
    plot()