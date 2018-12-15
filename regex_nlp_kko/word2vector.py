from gensim.models.word2vec import Word2Vec
import ast
import pandas as pd

import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


def create_model(filename, skip_gram=False):
    tokens = pd.read_csv(filename)
    tokens = tokens[tokens["contents"].apply(lambda x: 'http' not in x)]

    sentence = tokens["token"].apply(lambda x: ast.literal_eval(x)).tolist()

    if skip_gram:
        model = Word2Vec(sentence, min_count=10, iter=20, size=300, sg=1)
    else:
        model = Word2Vec(sentence, min_count=10, iter=20, size=300, sg=0)

    model.init_sims(replace=True)
    model.save("./result/embedding.model")


def most_similar():
    model = Word2Vec.load("./result/embedding.model")
    print("용돈과 관련된 키워드 : ", model.most_similar("용돈"))
    print("졍이와 관련된 키워드 : ", model.most_similar("졍이"))
    print("쭈니와 관련된 키워드 : ", model.most_similar("쭈니"))


if __name__ == '__main__':
    # create_model("./result/all_token_1.csv")
    most_similar()
