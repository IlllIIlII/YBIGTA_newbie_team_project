from base_crawler import BaseCrawler
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import pandas as pd
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

class ImdbCrawler(BaseCrawler):
    def __init__(self, output_dir: str):
        super().__init__(output_dir)
        self.base_url = 'https://www.imdb.com/title/tt4154796/reviews/?ref_=tt_ov_ururv'
        
    def start_browser(self):

        chrome_options = Options()
        chrome_options.add_experimental_option("detach", True)
        chrome_options.add_experimental_option("excludeSwitches",["enable-logging"])

        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.get(self.base_url)
        self.driver.implicitly_wait(2)
        try:
            self.driver.maximize_window()
        except:
            pass

    def scrape_reviews(self):
        driver = self.driver
        button = driver.find_element(By.XPATH, '//*[@id="__next"]/main/div/section/div/section/div/div[1]/section[1]/div[3]/div/span[2]/button')
        driver.execute_script("arguments[0].click();", button)

        prev_height = self.driver.execute_script("return document.body.scrollHeight")
        while True:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
            time.sleep(2)
            curr_height = self.driver.execute_script("return document.body.scrollHeight")
            if curr_height == prev_height:
                break
            prev_height = curr_height

        
        self.values = []
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        data_rows = soup.find_all('article', attrs={'class':'sc-d59f276d-1 euAsTr user-review-item'})
        print(f"found {len(data_rows)} data.")
        print("now crawling...")

        for _, row in enumerate(data_rows): 
            blank = []
            
            # date
            date = row.find('li', attrs={'class':'ipc-inline-list__item review-date'})
            if date:
                date = date.get_text().strip()
                date_parts = date.split()
                blank.append(date_parts[0])
                blank.append(date_parts[1].strip(','))
                blank.append(date_parts[2])
            else:
                continue
            # rate
            rate = row.find('span', attrs={'class':'ipc-rating-star--rating'})
            if rate:
                rate = rate.get_text().strip()
                blank.append(rate)
            else:
                continue
            # contents
            contents = row.find('div', attrs={'class':'ipc-html-content-inner-div'})
            if contents:
                contents = contents.get_text().strip()
                contents = contents.replace('\n', ' ').replace('\r', ' ').replace('<br>', ' ').strip()
                blank.append(contents)
            else:
                continue
            self.values.append(blank)
        print(f"crawled for {len(self.values)} data.")

    def save_to_database(self):
        li = []
        columns = ['month', 'day', 'year','rate','contents']
        df = pd.DataFrame(self.values, columns = columns)
        li.append(df)
        df_ = pd.concat(li).reset_index(drop=True)
        df_.to_csv(f'{self.output_dir}/reviews_imdb.csv', encoding = 'utf-8-sig')
