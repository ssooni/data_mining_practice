import requests
import pandas as pd
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
        sleep(1)


def call_weather_api(start_date, end_date):
    # API 키는 공개하기 힘든 점 양해 바랍니다.
    api_key = open("./raw_data/weather_api").readlines()[0].strip()
    url_format = 'https://data.kma.go.kr/apiData/getData?type=json&dataCd=ASOS&dateCd=HR&startDt={date}&startHh=00&endDt={date}&endHh=23&stnIds={snt_id}&schListCnt=100&pageIndex=1&apiKey={api_key}'

    headers = {'content-type': 'application/json;charset=utf-8'}
    for date in pd.date_range(start_date, end_date).strftime("%Y%m%d"):
        print("%s Weather" % date)
        url = url_format.format(api_key=api_key, date=date, snt_id="108")
        response = requests.get(url, headers=headers, verify=False)
        print(response.json()[-1]["info"])
        result = pd.DataFrame(response.json()[-1]["info"])
        print(result.head())
        result.to_csv("./raw_data/weather/weather_%s.csv" % date, index=False, encoding="utf-8")
        sleep(1)


if __name__ == '__main__':
    call_api("TimeAverageAirQuality", "2009-01-01", "2019-01-01", "dust")
    call_weather_api("2009-01-01", "2019-01-01")