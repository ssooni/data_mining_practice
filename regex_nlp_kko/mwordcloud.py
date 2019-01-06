import pandas as pd
import ast
import numpy as np
import matplotlib.pyplot as plt

from PIL import Image
from wordcloud import WordCloud


def get_except_keyword(filename):
    keyword_list = list()
    with open(filename, encoding='utf-8') as f:
        for keyword in f.readlines():
            keyword_list.append(keyword.strip())
    print(keyword_list)
    return keyword_list


def draw_wordcloud(kkma_result):
    # List로 되어있는 열을 Row 단위로 분리
    tokens = pd.DataFrame(kkma_result["token"].apply(lambda x: ast.literal_eval(x)).tolist())

    tokens["Date"] = kkma_result["Date"]
    tokens["Speaker"] = kkma_result["Speaker"]
    tokens["timetype"] = kkma_result["timetype"]
    tokens["time"] = kkma_result["time"]
    tokens["contents"] = kkma_result["contents"]

    tokens = tokens.set_index(["Date", "Speaker", "timetype", "time", "contents"])
    tokens = tokens.T.unstack().dropna().reset_index()

    tokens.columns = ["Date", "Person", "time_type", "time", "sntc", "index", "token"]
    print(tokens.head())

    # 빈도수 집계
    summary = tokens.groupby(["token"])["index"].count().reset_index()
    summary = summary.sort_values(["index"], ascending=[False]).reset_index(drop=True)

    # 특정 단어 필터링
    except_keyword = get_except_keyword("./raw_data/except_word.txt")
    summary = summary[summary["token"].apply(lambda x: x not in except_keyword)]
    summary = summary[summary["token"].apply(lambda x: len(x) > 1)]

    # 이미지 Mask 생성
    denne_mask = np.array(Image.open("./font/denne.png"))

    # 워드클라우드 생성
    wc = WordCloud(font_path='./font/NanumBrush.ttf', background_color='white', mask=denne_mask, width=800, height=600).generate(" ".join(summary["token"]))
    plt.imshow(wc)
    plt.axis("off")
    plt.show()


if __name__ == '__main__':
    kkma_result = pd.read_csv("./result/noun_token.csv")
    draw_wordcloud(kkma_result)

