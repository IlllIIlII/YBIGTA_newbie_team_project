# 팀 소개

저희 팀은  4조 이경민, 이서현, 김형진입니다. 
함께 협력하며 최고의 결과물을 만들어내기 위해 노력하고 있습니다.

## 팀원 소개

### 팀원 1 - 이경민
안녕하세요~ 인공지능학과 23학번 이경민입니다.
모두 잘 해봅시다 화이팅~

### 팀원 2 - 이서현 
안녕하세요! 컴퓨터과학과 23학번 이서현입니다.  
신입 교육 세션 다들 화이팅~!

### 팀원 3 - 김형진
ex ) 안녕하세요! 응용통계학과 20학번 김형진입니다.  
26기 모두들 화이팅!

### 팀 사진
저희 팀 사진입니다.
![branch_protection](github/branch_protection.png)
![push_rejected](github/push_rejected.png)
![merged_{MaDoKaLiF}](github/merged_{MaDoKaLiF}.png)
![merged_lshthegod](github/merged_lshthegod.png)
![merged_IlllIIlII](github/merged_IlllIIlII.jpg)


## 어벤져스: 엔드게임 리뷰 크롤러 (Naver 등)
본 프로젝트에서는 **어벤져스: 엔드게임** 리뷰 데이터를 네이버, IMDb,로튼토마토에서 크롤링하여 수집하였습니다.  
---

### 프로젝트 개요

- **수집 대상**: 네이버, IMDb, GG
- **네이버 링크**: [네이버 검색](https://search.naver.com/search.naver?where=nexearch&sm=tab_etc&mra=bkEw&pkid=68&os=2464226&qvt=0&query=%EC%96%B4%EB%B2%A4%EC%A0%B8%EC%8A%A4%3A%20%EC%97%94%EB%93%9C%EA%B2%8C%EC%9E%84%20%ED%8F%89%EC%A0%90)
- **IMDb 링크**: [IMDb](https://www.imdb.com/title/tt4154796/reviews/?ref_=tt_ov_ururv)
- **로튼토마토 링크** [Rottentomatoes](https://www.rottentomatoes.com/m/avengers_endgame/reviews?type=user)
- **크롤링 규모**: 네이버 총 300건, IMDb 총 2365건, 로튼토마토 총 1081건의 리뷰

---

### 데이터 구조
#### 네이버
크롤링을 통해 네이버에서 수집된 데이터는 아래 3개의 컬럼으로 구성되어 있습니다.

| Column | 예시                                     | 설명                                       |
|:------:|:---------------------------------------:|:------------------------------------------:|
| `date`   | `2020.01.01. 14:32`                    | 리뷰 작성일자 및 시간                      |
| `rating` | `"별점(10점 만점 중) 8점"`              | 10점 만점 기준으로 표시된 평점             |
| `review` | `영화가 정말 재밌었습니다! 다시 보고 싶네요.` | 실제 사용자 리뷰 내용                      |


#### IMDb
크롤링을 통해 IMDb에서 수집된 데이터는 아래 3개의 컬럼으로 구성되어 있습니다.

| Column   | 예시                    | 설명               |
|:--------:|:-----------------------:|:------------------:|
| `date`   | `Apr 24, 2019`          | 리뷰 작성일자       |
| `rating` | `9`                     | 10점 만점의 평점    |
| `review` | `This film deserves it.`| 실제 사용자 리뷰 내용|
---

#### 로튼토마토
크롤링을 통해 로튼토마토에서 수집된 데이터는 아래 3개의 컬럼으로 구성되어 있습니다.

| Column | 예시                                     | 설명                                       |
|:------:|:---------------------------------------:|:------------------------------------------:|
| `date`   | `2021-12-07`                    | 리뷰 작성일자 및 시간                      |
| `rating` | `"3.5`              | 5점 만점 기준으로 표시된 평점             |
| `review` | `This is a great vehicle for fan service and all the commercial success that comes with that, but it ...` | 실제 사용자 리뷰 내용 |

### 크롤링 코드 실행 방법

#### 모든 사이트 크롤링

아래 명령어를 통해 **모든 사이트**에 대해 리뷰 데이터를 일괄 수집 및 저장할 수 있습니다.

```bash
python main.py -o {output directory} --all
```
#### 네이버
```bash
python main.py -o C:\Users\PC\onedrive(yonsei)\문서\GitHub\YBIGTA_newbie_team_project\database -c naver
```
#### 로튼토마토
```bash
python main.py -o C:\Users\PC\onedrive(yonsei)\문서\GitHub\YBIGTA_newbie_team_project\database -c rottentomatoes
```

---
### EDA/전처리/FE 결과

#### IMDb

아래 그래프는 평점 분포를 나타낸 막대 그래프입니다. 10점에 특히 많은 평점이 몰렸습니다.
![IMDb_rating](review_analysis/plots/IMDb_rating.png)

아래 그래프는 리뷰 작성 년도 분포입니다. 영화 개봉 년도인 2019년에 가장 많은 리뷰가 달렸습니다.
![IMDb_date](review_analysis/plots/IMDb_date.png)

아래 그래프는 리뷰 텍스트의 길이입니다. 
![IMDb_distribution](review_analysis/plots/IMDb_distribution.png)


리뷰 텍스트의 길이 분석한 결과, 대부분의 리뷰는 2000자 이내에 위치하고 있으며, 일부 리뷰는 극단적으로 긴 형태(2000자 이상)로 나타났습니다. 이에 2000자 이상의 리뷰를 중앙값으로 대체하여 분석에 적합하도록 처리했습니다. 또한, 텍스트 길이를 200자 단위로 나누어 새로운 그룹 변수(length_group)를 생성했습니다.

아래 그래프는 전처리와 FE를 마친 후의 데이터를 sunburst로 나타낸 결과입니다. 평점에 따른 리뷰의 길이를 200자 단위로 나누어 표기하였습니다.
![IMDb_sunburst](review_analysis/plots/IMDb_sunburst.png)

#### RottenTomatoes

이상치 탐색 결과입니다. 데이터에 큰 예외나 오류는 없는 것으로 보입니다.
![EDA_inspection](review_analysis/plots/EDA_inspection.png)

리뷰 평점 그래프입니다. 관객들 대다수가 높은 평점을 준 것을 알 수 있습니다.
![rating_distribution](review_analysis/plots/rating_distribution.png)

리뷰 길이를 보면 100자 미만의 리뷰를 작성한 유저는 많지 않습니다.
![review_length_distribution](review_analysis/plots/review_length_distribution.png)

관련성 있는, 자주 나오는 단어의 그래프입니다.
![keyword_frequencies](review_analysis/plots/keyword_frequencies.png)

요일별, 월별 리뷰의 개수 그래프입니다. 요일별로는 큰 차이가 없으나 금요일이 가장 많습니다.
![week](review_analysis/plots/review_by_weekday.png)
![month](review_analysis/plots/monthly_review_counts.png)

#### naver

아래 그래프는 리뷰 작성 년도 분포입니다. 영화 개봉 년도인 2019년에 가장 많은 리뷰가 달렸습니다.
![number_of_reviews](review_analysis/plots/number_of_reviews.png)

아래 그래프는 키워드의 빈도입니다. 
![naver_keyword_frequency](review_analysis/plots/naver_keyword_frequency.png)

아래 그래프는 키워드의 빈도입니다. 
![naver_word_clouds](review_analysis/plots/naver_word_clouds.png)

언급된 단어의 빈도를 보아 '아이언맨', '마블', '어벤져스', '영화', '재미', '완벽한' 등의 단어가 많이 언급된 것을 확인할 수 있습니다. 

---

[Docker Hub](https://hub.docker.com/repository/docker/seohyun7/ybigta-team/general)