from sklearn.cluster import DBSCAN
from gensim.models import Word2Vec

import pandas as pd
import re

model = Word2Vec.load("./result/embedding.model")
word_vector = model.wv.vectors
match_index = model.wv.index2word
print(len(match_index))
model.init_sims(replace=True)

han = re.compile(r"[가-힣]{2,}")

for eps in range(3, 9):
    dbscan = DBSCAN(eps=0.75, min_samples=eps)

    clusters = dbscan.fit_predict(word_vector)
    c = pd.DataFrame(clusters, columns=["cluster"], index=match_index)
    c = pd.DataFrame(c.reset_index())

    print(c.groupby(["cluster"]).count())

    c = c[c["index"].apply(lambda x: len(han.findall(x)) > 0)]
    c = c[c["cluster"] != -1]

    c.to_excel(pd.ExcelWriter("./result/cluster_eps_%s.xlsx" % eps), index=False)