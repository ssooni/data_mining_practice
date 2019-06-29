import requests
import pandas as pd
import os
import datetime as dt
import matplotlib.pyplot as plt
import urllib3

from time import sleep


def call_api(api_name, start_date, end_date, dir_name):
    # API 키는 공개하기 힘든 점 양해 바랍니다.
    api_key = open("./raw_data/api_key").readlines()[0].strip()
    url_format = 'http://openAPI.seoul.go.kr:8088/{api_key}/json/{api_name}/1/{end_index}/{date}'
    headers = {'content-type': 'application/json;charset=utf-8'}

    for date in pd.date_range(start_date, end_date).strftime("%Y%m%d"):
        # 최초 1회 Call은 해당 일자의 데이터 수를 확인한다.
        url = url_format.format(api_name=api_name, api_key=api_key, end_index=1, date=date)
        response = requests.get(url, headers=headers)
        end_index = response.json()[api_name]["list_total_count"]
        print("Max Count(%s): %s" % (date, end_index))

        # 해당 일자의 모든 데이터를 불러온다.
        url = url_format.format(api_name=api_name, api_key=api_key, end_index=end_index, date=date)
        response = requests.get(url, headers=headers)
        result = pd.DataFrame(response.json()[api_name]["row"])
        result.to_csv("./raw_data/%s/dust_%s.csv" % (dir_name, date), index=False, encoding="utf-8")

        # API 부하 관리를 위해 0.5초 정도 쉬어 줍시다 (찡긋)
        sleep(0.5)


def call_weather_api(start_date, end_date):
    # API 키는 공개하기 힘든 점 양해 바랍니다.
    api_key = open("./raw_data/weather_api").readlines()[0].strip()
    url_format = 'https://data.kma.go.kr/apiData/getData?type=json&dataCd=ASOS&dateCd=HR&startDt={date}&startHh=00&endDt={date}&endHh=23&stnIds={snt_id}&schListCnt=100&pageIndex=1&apiKey={api_key}'

    headers = {'content-type': 'application/json;charset=utf-8'}
    urllib3.disable_warnings()

    for date in pd.date_range(start_date, end_date).strftime("%Y%m%d"):
        print("%s Weather" % date)
        url = url_format.format(api_key=api_key, date=date, snt_id="108")
        response = requests.get(url, headers=headers, verify=False)

        # 200 (정상)의 경우에만 파일 생성
        print(response.status_code)
        if response.status_code == 200:
            result = pd.DataFrame(response.json()[-1]["info"])
            print(result.head())
            result.to_csv("./raw_data/weather/weather_%s.csv" % date, index=False, encoding="utf-8")

        # API 부하 관리를 위해 0.5초 정도 쉬어 줍시다 (찡긋)
        sleep(0.5)


def concat_data():
    df_list = list()

    # ./raw_data/dust 아래의 모든 파일을 읽습니다.
    for root, dirs, files in os.walk("./raw_data/dust", topdown=False):
        for name in files:
            df_list.append(pd.read_csv(os.path.join(root, name)))

    dust = pd.DataFrame(pd.concat(df_list, sort=False))

    # Datetime 형태로 Index를 변경해줍니다.
    dust["MSRDT"] = dust["MSRDT"].apply(lambda x: dt.datetime.strptime(str(x), "%Y%m%d%H%M"))
    dust = dust.set_index("MSRDT")

    df_list.clear()

    # ./raw_data/weather 아래의 모든 파일을 읽습니다.
    for root, dirs, files in os.walk("./raw_data/weather", topdown=False):
        for name in files:
            df_list.append(pd.read_csv(os.path.join(root, name)))
    weather = pd.DataFrame(pd.concat(df_list, sort=False))

    # Datetime 형태로 Index를 변경해줍니다.
    weather["TM"] = weather["TM"].apply(lambda x: dt.datetime.strptime(x, "%Y-%m-%d %H:%M"))
    weather = weather.set_index("TM")

    # join() 함수는 같은 iㅠndex 끼리의 join을 제공합니다.
    master = weather.join(dust, how="inner")

    master.to_hdf("./raw_data/data.hdf", "master")
    dust.to_hdf("./raw_data/data.hdf", "dust")
    weather.to_hdf("./raw_data/data.hdf", "weather")


def describe_dust_data():
    master = pd.read_hdf("./raw_data/data.hdf", "master")

    msr_nm_list = set(master["MSRSTE_NM"].dropna().tolist())
    print(msr_nm_list)

    # 한글 전용 폰트 적용
    plt.rcParams["font.family"] = 'D2Coding'
    plt.rcParams["font.size"] = 10

    fig, ax = plt.subplots()
    master.boxplot(column='PM25', by='MSRSTE_NM', ax=ax)
    plt.show()


if __name__ == '__main__':
    # call_api("TimeAverageAirQuality", "2009-01-01", "2019-01-01", "dust")
    call_weather_api("2009-01-01", "2019-01-01")
    concat_data()
    describe_dust_data()