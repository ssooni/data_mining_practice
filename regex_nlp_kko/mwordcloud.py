import pandas as pd
import datetime as dt
import ast
from wordcloud import WordCloud

import matplotlib.pyplot as plt


def draw_wordcloud(tokens):
    pass


if __name__ == '__main__':
    kkma_result = pd.read_csv("./result/noun_token_1.csv")
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

    summary = tokens.groupby(["token"])["index"].count().reset_index()
    summary = summary.sort_values(["index"], ascending=[False]).reset_index(drop=True)
    summary = summary[summary["token"] != '이모티콘']

    summary = summary[summary["token"] != '사진']
    summary = summary[summary["token"] != '동영상']
    summary = summary[summary["token"] != '오늘']
    summary = summary[summary["token"] != '내일']

    summary = summary[summary["token"].apply(lambda x: len(x) > 1)]

    summary = summary.head(100)
    # freq_80 = summary["index"].quantile(0.95)
    # summary = summary[summary["index"] < freq_80]

    # summary.plot.line()
    # plt.show()
    print(summary.describe())

    print(" ".join(summary["token"]))
    wc = WordCloud(font_path='./font/NanumBrush.ttf', background_color='white', width=800, height=600).generate(" ".join(summary["token"]))
    plt.imshow(wc)
    plt.axis("off")
    plt.show()