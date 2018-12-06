import pandas as pd
import datetime as dt
from wordcloud import WordCloud

import matplotlib.pyplot as plt

nlp_result = pd.read_csv("./result/result_2.csv")

nlp_result = nlp_result.set_index(["0", "1", "2", "3", "4"])
nlp_result = nlp_result.T.unstack().dropna().reset_index()
nlp_result.columns = ["Date", "Person", "time_type", "time", "sntc", "index", "token"]

# print(r)

nlp_result["Date"] = nlp_result["Date"].apply(lambda x: dt.datetime.strptime(x, "%Y년 %m월 %d일").strftime("%Y-%m-%d"))
nlp_result["Date"] = pd.to_datetime(nlp_result["Date"])

summary = nlp_result.groupby(["token"])["index"].count().reset_index()
print(summary)
summary = summary.sort_values(["index"], ascending=[False]).reset_index(drop=True)
#
#
summary = summary[summary["token"] != '사진']
summary = summary[summary["token"].apply(lambda x: len(x) > 1)]
#
# print(summary)

freq_80 = summary["index"].quantile(0.90)
print(freq_80)
summary = summary[summary["index"] < freq_80]
summary = summary.head(100)
# print(summary)

print(" ".join(summary["token"]))
wc = WordCloud(font_path='./font/NanumBrush.ttf', background_color='white', width=800, height=600).generate(" ".join(summary["token"]))
plt.imshow(wc)
plt.axis("off")
plt.show()