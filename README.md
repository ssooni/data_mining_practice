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
서울시 미세먼지와 날씨와 상관 관계를 분석

> 데이터 출처 : 서울시 열린데이터광장 (http://data.seoul.go.kr)

1. API Call을 하여 Raw Data 구성하기
2. Granger Causality 적용
3. **GRU** 모델 적용

## kaggle 문제
