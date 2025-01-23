from base_crawler import BaseCrawler
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import pandas as pd
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

class ImdbCrawler(BaseCrawler):
    """
    A web crawler to scrape user reviews from IMDb for a specific movie.

    Attributes:
        output_dir (str): Directory path to save the scraped reviews as a CSV file.
        base_url (str): URL of the IMDb reviews page for the specific movie.
        driver (webdriver.Chrome): Chrome WebDriver instance for browsing the web page.
        values (list): List of scraped reviews with details like date, rate, and contents.
    """
    def __init__(self, output_dir: str):
        """
        Initializes the ImdbCrawler instance with the output directory and base URL.

        Args:
            output_dir (str): Directory path where the scraped reviews will be saved.
        """
        super().__init__(output_dir)
        self.base_url = 'https://www.imdb.com/title/tt4154796/reviews/?ref_=tt_ov_ururv'
        self.driver = None
        
    def start_browser(self):
        """
        Starts a Chrome browser session using Selenium WebDriver, navigates to the IMDb reviews page,
        and prepares the browser for scraping by maximizing the window.
        """
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
        """
        Scrapes user reviews from the IMDb reviews page. The function scrolls through the page to load
        all reviews, then extracts the date, rating, and contents of each review using BeautifulSoup.

        Reviews are stored in the `self.values` attribute as a list of lists.

        Returns:
            list: A list of reviews where each review is represented as a list containing:
                - date (str): The date of the review.
                - rate (str): The rating given by the user.
                - contents (str): The review text.

        Raises:
            Exception: If elements are not found.
        """
        if self.driver is None:
            self.start_browser()
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
                blank.append(date)
            else:
                continue
            # rating
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
        return self.values

    def save_to_database(self, data):
        """
        Saves scraped review data to a CSV file.

        Args:
            data (list): A list of lists where each inner list represents a single review

        Returns:
            None: This method saves the data to a CSV file and does not return any value.
        """
        li = []
        columns = ['date','rating','review']
        df = pd.DataFrame(data, columns = columns)
        li.append(df)
        df_ = pd.concat(li).reset_index(drop=True)
        df_.to_csv(f'{self.output_dir}/reviews_imdb.csv', encoding = 'utf-8-sig')
