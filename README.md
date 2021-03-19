# Data Mining Practice
일상 생활 속의 데이터를 이용해서 데이터 마이닝 기법을 적용하고자 하였습니다.

> 블로그 : http://ssoonidev.tistory.com

## regex_nlp_kko
카카오톡 대화 내용을 NLP에 적용해 보았습니다.
> 실제 대화내용을 기반으로 작성되어 DataSet 공개가 어렵습니다.

1. 한글 형태소 분석기 **Kkma**로 Tokenize 적용
2. Token 들의 빈도를 기준으로 **WordCloud** 생성
3. **Word2Vec**로 Word Embedding 적용
4. Word Vector로 **DBSCAN** 클러스터링 적용
5. Cosine Similarity으로 유사도 측정

## dust_weather
T시의 서울시 강남구의 미세먼지 농도를 T-20 ~ T-1 구간의 기상과 미세먼지 농도를 이용해서 모델링

> 데이터 출처 : 서울시 열린데이터광장 (http://data.seoul.go.kr)
> 공공데이터포털 : (https://www.data.go.kr/)

1. API Call을 하여 Raw Data 구성하기
2. **GRU** 모델 적용

![예측결과](https://user-images.githubusercontent.com/22573245/111718506-5c9d7c80-889d-11eb-9859-cc5f7fa3d33b.png)

## kaggle 문제
