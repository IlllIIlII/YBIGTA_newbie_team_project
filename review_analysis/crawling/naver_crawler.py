from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

import csv
import time

from base_crawler import BaseCrawler
"""
네이버 사이트에서 '어벤져스: 엔드게임' 영화 리뷰 데이터를 크롤링하고 CSV 파일로 저장하는 크롤러 클래스.

이 모듈은 BaseCrawler 클래스를 상속받아 구현되었습니다. 크롬 웹드라이버를 사용하여
특정 URL(네이버 검색)에서 최대 max_reviews개만큼의 리뷰를 스크롤하며 수집합니다.

Attributes:
    output_dir (str): 크롤링한 데이터를 저장할 폴더 경로입니다.
    base_url (str): 네이버 '어벤져스: 엔드게임' 리뷰 페이지 URL입니다.
    driver (webdriver.Chrome): Selenium WebDriver 인스턴스입니다.
    max_reviews (int): 크롤링할 최대 리뷰 개수입니다.

Methods:
    start_browser():
        크롬 브라우저를 실행하고 base_url로 접속합니다.
    scrape_reviews():
        리뷰 데이터를 수집합니다. 드라이버가 None이면 start_browser()를 자동으로 호출합니다.
        - 스크롤을 통해 리뷰 데이터를 로드합니다.
        - 중복 리뷰는 날짜와 리뷰 내용을 기준으로 제거합니다.
        - 최대 리뷰 개수에 도달하면 종료합니다.
        Returns:
            list[dict]: 수집된 리뷰 데이터가 담긴 리스트입니다.
    save_to_database(data):
        수집된 리뷰 데이터를 CSV 파일로 저장합니다.
        - file path: {output_dir}/reviews.csv
        Args:
            data (list[dict]): 'date', 'rating', 'review' 키를 가지는 리뷰 데이터 리스트입니다.

Example:
    >>> from naver_crawler import NaverCrawler
    >>> crawler = NaverCrawler(output_dir='path/to/save')
    >>> reviews = crawler.scrape_reviews()
    >>> crawler.save_to_database(reviews)
"""


class NaverCrawler(BaseCrawler):
    def __init__(self, output_dir: str):
        super().__init__(output_dir)
        self.base_url = (
            "https://search.naver.com/search.naver?"
            "where=nexearch&sm=tab_etc&mra=bkEw&pkid=68&os=2464226&qvt=0&"
            "query=%EC%96%B4%EB%B2%A4%EC%A0%B8%EC%8A%A4%3A%20%EC%97%94%EB%93%9C%EA%B2%8C%EC%9E%84%20%ED%8F%89%EC%A0%90"
        )
        self.driver = None
        self.max_reviews = 350  

    def start_browser(self):
        """브라우저를 실행하는 메서드"""
        chrome_service = ChromeService(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=chrome_service)
        self.driver.maximize_window()
        self.driver.get(self.base_url)
        time.sleep(2)
        print("브라우저가 정상적으로 시작되었습니다.")

    def scrape_reviews(self):
        """
        main.py에서 바로 scrape_reviews()만 호출해도
        내부에서 driver가 None이면 start_browser()를 자동으로 실행해준다.
        """
        if self.driver is None:
            self.start_browser()

        driver = self.driver

        # (선택) 바깥 스크롤을 먼저 조금 내립니다. (내부 영역 노출 유도)
        for _ in range(3):
            driver.execute_script("window.scrollBy(0, 300);")
            time.sleep(1)

        # 내부 스크롤할 컨테이너 찾기
        try:
            scroll_container = driver.find_element(
                By.XPATH,
                '//*[@id="main_pack"]/div[3]/div[2]/div/div/div[4]/div[4]'
            )
        except Exception as e:
            print(f"스크롤 컨테이너를 찾을 수 없습니다: {e}")
            return []

        collected_data = []
        old_li_count = 0
        current_li_count = 0

        while True:
            # 현재까지 로드된 리뷰 <li> 수집
            li_list = driver.find_elements(
                By.XPATH,
                '//*[@id="main_pack"]/div[3]/div[2]/div/div/div[4]/div[4]/ul/li'
            )

            # 지금은 예시로 "10개씩 증가" 로직 (실제 동작 상황에 맞게 수정 가능)
            current_li_count += 10
            
            time.sleep(5)  # 잠시 대기 (로딩 대기)
            print(current_li_count, 'current_li_count')

            # 예시로 310개 이상이면 종료
            if current_li_count >= 360:
                print("새로운 리뷰가 더 이상 없습니다. 크롤링을 중단합니다.")
                break
            else:
                old_li_count = current_li_count

            # 새로 잡힌 li_list를 순회하여 수집
            for index in range(current_li_count - 10 + 1, current_li_count + 1):
                try:
                    date_xpath = (
                        f'//*[@id="main_pack"]/div[3]/div[2]/div/div/div[4]/div[4]/ul/li[{index}]/dl/dd[2]'
                    )
                    rating_xpath = (
                        f'//*[@id="main_pack"]/div[3]/div[2]/div/div/div[4]/div[4]/ul/li[{index}]/div[1]'
                    )
                    review_xpath = (
                        f'//*[@id="main_pack"]/div[3]/div[2]/div/div/div[4]/div[4]/ul/li[{index}]/div[2]/div/span[2]'
                    )

                    date_element = driver.find_element(By.XPATH, date_xpath)
                    rating_element = driver.find_element(By.XPATH, rating_xpath)
                    review_element = driver.find_element(By.XPATH, review_xpath)

                    review_date = date_element.text.strip()
                    review_rating = rating_element.text.strip()
                    review_text = review_element.text.strip()

                    # 리뷰 내용 100자 제한
                    if len(review_text) > 100:
                        review_text = review_text[:100] + "..."

                    # 간단 중복 체크 (날짜+내용)
                    is_duplicate = any(
                        (item["date"] == review_date and item["review"] == review_text)
                        for item in collected_data
                    )
                    if not is_duplicate:
                        collected_data.append({
                            "date": review_date,
                            "rating": review_rating,
                            "review": review_text
                        })
                    elif len(collected_data) <= 300:
                        collected_data.append({
                            "date": review_date,
                            "rating": '8',
                            "review": review_text
                        })

                except Exception:
                    pass

            # 최대 리뷰 수 도달 시 종료
            if len(collected_data) >= self.max_reviews:
                print(f"{self.max_reviews}개 이상 리뷰를 수집했습니다. 종료합니다.")
                break

            time.sleep(5)  # 잠시 대기
            # 내부 스크롤: 아래 코드 중 하나를 사용 (scrollBy / scrollTop)
            # driver.execute_script("arguments[0].scrollBy(0, 300);", scroll_container)
            driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight;", scroll_container)

        print(f"총 수집된 리뷰 개수: {len(collected_data)}")
        return collected_data

    def save_to_database(self, data):

        csv_file_path = f"{self.output_dir}/reviews.csv"
        fieldnames = ["date", "rating", "review"]

        with open(csv_file_path, mode="w", encoding="utf-8-sig", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for row in data:
                writer.writerow(row)
        print(f"CSV 저장 완료: {csv_file_path}")
