import re
import pandas as pd

from konlpy.tag import Kkma


def get_noun(msg_txt):
    kkma = Kkma()
    nouns = list()
    pattern = re.compile("[ㄱ-ㅎㅏ-ㅣ]+")
    msg_txt = re.sub(pattern, "", msg_txt).strip()

    if len(msg_txt) > 0:
        pos = kkma.pos(msg_txt)
        for keyword, type in pos:
            # 고유명사 또는 보통명사
            if type == "NNG" or type == "NNP":
                nouns.append(keyword)
        print(msg_txt, "->", nouns)

    return nouns


def get_all_token(msg_txt):
    kkma = Kkma()
    nouns = list()
    pattern = re.compile("[ㄱ-ㅎㅏ-ㅣ]+")
    msg_txt = re.sub(pattern, "", msg_txt).strip()

    if len(msg_txt) > 0:
        pos = kkma.pos(msg_txt)
        for keyword, type in pos:
            nouns.append(keyword)
        print(msg_txt, "->", nouns)

    return nouns


if __name__ == '__main__':
    raw_data = pd.read_csv("./result/kko_regex.csv")
    print(raw_data.head())
    raw_data = raw_data.dropna()

    raw_data["token"] = raw_data["contents"].apply(lambda x: get_noun(x))
    raw_data.to_csv("./result/noun_token.csv", index=False)

    raw_data["token"] = raw_data["contents"].apply(lambda x: get_all_token(x))
    raw_data.to_csv("./result/all_token.csv", index=False)

