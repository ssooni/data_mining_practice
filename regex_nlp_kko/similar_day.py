import pandas as pd
import ast
import re

from sklearn.metrics.pairwise import linear_kernel
from sklearn.feature_extraction.text import TfidfVectorizer


def preprocess(x):
    result = list()
    except_word = open("./raw_data/except_similar.txt", mode="r", encoding="utf-8").readlines()
    han = re.compile(r"[가-힣]{2,}")

    for i in x:
        # 두글자 이상 한글이 포함되는 경우만 사용
        if len(han.findall(i)) == 0:
            continue
        # 이모티콘 / 사진 / 동영상을 보낸 채팅내역 제거
        if len(x) == 1 and i in ["사진", "이모티콘", "동영상"]:
            continue
        # 제거 대상 키워드리스트에 포함되는 경우제거
        if i in except_word:
            continue

        result.append(i)
    return result


def generate_daily_bow(tokens):
    tokens["token"] = tokens["token"].apply(lambda x: preprocess(x))

    date_list = sorted(list(set(tokens["Date"].tolist())))
    print("Date : ", len(date_list), " days")

    document_list = list()
    for date in sorted(date_list):
        daily_tokens = tokens[tokens["Date"] == date]
        document = ""
        for t in daily_tokens["token"].tolist():
            if len(" ".join(t)) > 0:
                document += " "
                document += " ".join(t)

        print(date, document[0:100])
        document_list.append(document)

    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(document_list)

    similar_result = list()
    for index, date in enumerate(sorted(date_list)):
        for i, score in find_similar(X, index):
            similar_result.append([date, date_list[i], score])

    df = pd.DataFrame(similar_result, columns=["Date", "Smlr_Date", "Similarity"])
    df = df.sort_values(["Similarity"], ascending=False)
    print(df)


def find_similar(tfidf_matrix, index, top_n=5):
    cosine_similarities = linear_kernel(tfidf_matrix[index:index+1], tfidf_matrix).flatten()
    related_docs_indices = [i for i in cosine_similarities.argsort()[::-1] if i != index]
    return [(index, cosine_similarities[index]) for index in related_docs_indices][0:top_n]


if __name__ == '__main__':
    tokens = pd.read_csv("./result/noun_token_1.csv")
    tokens["token"] = tokens["token"].apply(lambda x: ast.literal_eval(x))
    print(tokens.head())

    generate_daily_bow(tokens)
