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
안녕하세요! 응용통계학과 20학번 김형진입니다.  
26기 모두들 화이팅!

### 팀 사진
저희 팀 사진입니다.
![branch_protection](github/branch_protection.png)
![push_rejected](github/push_rejected.png)
![merged_{MaDoKaLiF}](github/merged_{MaDoKaLiF}.png)

## 어벤져스: 엔드게임 리뷰 크롤러 (Naver 등)
본 프로젝트에서는 **어벤져스: 엔드게임** 리뷰 데이터를 네이버, GG,GG에서 크롤링하여 수집하였습니다.  
---

<!-- 
### 프로젝트 개요

- **수집 대상**: 네이버, GG,GG
- **네이버 링크**: [네이버 검색](https://search.naver.com/search.naver?where=nexearch&sm=tab_etc&mra=bkEw&pkid=68&os=2464226&qvt=0&query=%EC%96%B4%EB%B2%A4%EC%A0%B8%EC%8A%A4%3A%20%EC%97%94%EB%93%9C%EA%B2%8C%EC%9E%84%20%ED%8F%89%EC%A0%90)
- **크롤링 규모**: 네이버 총 N건, GG 총 M건, GG 총 M건의 리뷰

---

### 데이터 구조
#### 네이버
크롤링을 통해 네이버에서 수집된 데이터는 아래 3개의 컬럼으로 구성되어 있습니다.

| Column | 예시                                     | 설명                                       |
|:------:|:---------------------------------------:|:------------------------------------------:|
| `date`   | `2020.01.01. 14:32`                    | 리뷰 작성일자 및 시간                      |
| `rating` | `"별점(10점 만점 중) 8점"`              | 10점 만점 기준으로 표시된 평점             |
| `review` | `영화가 정말 재밌었습니다! 다시 보고 싶네요.` | 실제 사용자 리뷰 내용                      |

---

### 크롤링 코드 실행 방법

#### 모든 사이트 크롤링

아래 명령어를 통해 **모든 사이트**에 대해 리뷰 데이터를 일괄 수집 및 저장할 수 있습니다.

```bash
python main.py -o {output directory} --all
```
#### 네이버
```bash
python main.py -o C:\Users\PC\onedrive(yonsei)\문서\GitHub\YBIGTA_newbie_team_project\database -c naver
``` -->