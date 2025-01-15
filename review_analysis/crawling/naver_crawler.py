from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

import csv
import time

from base_crawler import BaseCrawler


class NaverCrawler(BaseCrawler):
    def __init__(self, output_dir: str):
        super().__init__(output_dir)
        self.base_url = (
            "https://search.naver.com/search.naver?"
            "where=nexearch&sm=tab_etc&mra=bkEw&pkid=68&os=2464226&qvt=0&"
            "query=%EC%96%B4%EB%B2%A4%EC%A0%B8%EC%8A%A4%3A%20%EC%97%94%EB%93%9C%EA%B2%8C%EC%9E%84%20%ED%8F%89%EC%A0%90"
        )
        self.driver = None
        self.max_reviews = 1000  # 내부에서 최대 몇 개의 리뷰를 수집할 것인지

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
            if current_li_count >= 310:
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
