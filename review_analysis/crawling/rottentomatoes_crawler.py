from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import csv
import os
import time
from base_crawler import BaseCrawler

class RottenTomatoesCrawler(BaseCrawler):
    """
    로튼토마토 사용자 리뷰를 크롤링하는 클래스.

    Attributes:
        output_dir (str): 데이터를 저장할 디렉토리 경로
        base_url (str): 로튼토마토 리뷰 페이지 URL
        driver (webdriver.Chrome): Selenium WebDriver 인스턴스
        max_reviews (int): 크롤링할 최대 리뷰 개수
    """

    def __init__(self, output_dir: str):
        super().__init__(output_dir)
        self.base_url = "https://www.rottentomatoes.com/m/avengers_endgame/reviews?type=user"
        self.driver = None
        self.max_reviews = 1000

    def start_browser(self):
        chrome_service = ChromeService(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=chrome_service)
        self.driver.maximize_window()
        self.driver.get(self.base_url)
        time.sleep(2)
        

    def scrape_reviews(self):
        """
        리뷰 데이터를 수집하여 리스트로 반환합니다.

        Returns:
            list[dict]: 수집된 리뷰 데이터 리스트
        """
        if self.driver is None:
            self.start_browser()

        driver = self.driver
        collected_data = []

        while True:
            
            reviews = driver.find_elements(By.CSS_SELECTOR, ".audience-review-row")

            for review in reviews:
                try:
                    date = review.find_element(By.CSS_SELECTOR, ".audience-reviews__duration").text.strip()
                    rating_element = review.find_element(By.CSS_SELECTOR, "rating-stars-group")
                    rating = rating_element.get_attribute("score") if rating_element else "N/A"
                    review_text = review.find_element(By.CSS_SELECTOR, ".audience-reviews__review").text.strip()

                    if len(review_text) > 100:
                        review_text = review_text[:100] + "..."

                    
                    if not any(d["review"] == review_text for d in collected_data):
                        collected_data.append({
                            "date": date,
                            "rating": rating,
                            "review": review_text
                        })

                except Exception as e:
                    print(f"error: {e}")
                    continue

            
            if len(collected_data) >= self.max_reviews:
                break

           
            try:
                next_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "rt-button[data-loadmoremanager='btnLoadMore:click']"))
                )
                next_button.click()
                time.sleep(3)
            except Exception as e:
                print(f"error: {e}")
                break

        
        return collected_data

    def save_to_database(self, data):
        """수집된 데이터를 CSV 파일로 저장합니다."""
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

        csv_file_path = f"{self.output_dir}/reviews_rottentomatoes.csv"
        fieldnames = ["date", "rating", "review"]

        with open(csv_file_path, mode="w", encoding="utf-8-sig", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for row in data:
                writer.writerow(row)

        print(f"CSV 저장 완료: {csv_file_path}")

if __name__ == "__main__":
    crawler = RottenTomatoesCrawler(output_dir="./database")
    reviews = crawler.scrape_reviews()
    crawler.save_to_database(reviews)

