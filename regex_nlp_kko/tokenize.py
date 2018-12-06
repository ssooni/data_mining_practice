import re
import pandas as pd
import datetime as dt

from konlpy.tag import Kkma

# parse_result = list()
# konlpy_result = list()
#
# cur_date = ""
# cur_month = 0
#
# kkma = Kkma()
#
# for msg in msg_list:
#     if len(kko_date_pattern.findall(msg)) > 0:
#         cur_date = kko_date_pattern.findall(msg)[0]
#
#         month = dt.datetime.strptime(cur_date, "%Y년 %m월 %d일").month
#         print(cur_date, month)
#
#         if cur_month != month:
#             print(cur_month, month)
#             if len(konlpy_result) > 0:
#                 pd.DataFrame(konlpy_result).to_csv("result_%s.csv" % cur_month, index=False)
#                 konlpy_result = list()
#                 kkma = Kkma()
#
#         cur_month = month
#
#     else:
#         extract_reuslt = kko_pattern.findall(msg)
#         parse_result.extend(extract_reuslt)
#
#         if len(extract_reuslt) > 0:
#             msg_txt = extract_reuslt[0][-1]
#             msg_txt = re.sub(emoji_pattern, "", msg_txt)
#
#             if "ㅇㄷ" not in msg_txt and msg_txt != "이모티콘":
#                 nouns = list()
#                 pos = kkma.pos(msg_txt)
#                 for keyword, type in pos:
#                     # 고유명사 또는 보통명사
#                     if type == "NNG" or type == "NNP":
#                         nouns.append(keyword)
#                 print(msg_txt, "->", nouns)
#                 if len(nouns) > 0:
#                     row = [cur_date] + list(extract_reuslt[0]) + nouns
#                     konlpy_result.append(row)
#


if __name__ == '__main__':
    pass