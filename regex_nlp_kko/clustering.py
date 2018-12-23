from sklearn.cluster import DBSCAN
from gensim.models import Word2Vec

import pandas as pd
import re

import matplotlib.pyplot as plt
import matplotlib.font_manager as fm


def cluster(eps, min_sample):
    # Word Vector를 Load 합니다.
    model = Word2Vec.load("./result/embedding.model")

    word_vector = model.wv.vectors
    match_index = model.wv.index2word
    model.init_sims(replace=True)

    # 두 글자이상 한글인 경우만 사용
    han = re.compile(r"[가-힣]{2,}")

    # DBSCAN 알고리즘 적용
    dbscan = DBSCAN(eps=eps, min_samples=min_sample)
    clusters = dbscan.fit_predict(word_vector)

    df = pd.DataFrame(clusters, columns=["cluster"], index=match_index).reset_index()
    df.columns = ["word", "cluster"]
    print(df.head())

    # 한글만 필터링 처리
    df = df[df["word"].apply(lambda x: len(han.findall(x)) > 0)]

    # 노이즈 포인트 제거
    df = df[df["cluster"] != -1]

    print(df.groupby(["cluster"]).count())

    df.to_excel(pd.ExcelWriter("./result/cluster.xlsx"), index=False)


def plot():
    clstr = pd.read_excel(pd.ExcelFile("./result/cluster.xlsx"))
    min_cluster = clstr["cluster"].min()
    max_cluster = clstr["cluster"].max()

    print(min_cluster, max_cluster)
    for clstr_num in range(min_cluster, max_cluster + 1):
        clstr_index = clstr[clstr["cluster"] == clstr_num].index
        clstr.loc[clstr_index, "value"] = list(range(0, len(clstr_index) * 3, 3))

    font = fm.FontProperties(fname="./font/NanumGothic.ttf", size=12)

    fig, ax = plt.subplots()
    clstr.plot.scatter(x="cluster", y="value", ax=ax)
    clstr[["cluster", "value", "word"]].apply(lambda x: ax.text(*x, fontproperties=font), axis=1)
    plt.show()


if __name__ == '__main__':
    cluster(eps=0.75, min_sample=6)
    plot()