import os
import sys
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer  # type: ignore
from base_processor import BaseDataProcessor

class RottenTomatoesProcessor(BaseDataProcessor):
    """
    Rotten Tomatoes 데이터 전처리 및 Feature Engineering 클래스.

    Attributes:
        input_path(str): 입력 파일 경로.
        output_dir (str): 출력 파일을 저장할 디렉토리 경로.
    """

    def __init__(self, input_path: str, output_dir: str):
        super().__init__(input_path, output_dir)
        self.data = None

    def preprocess(self):

        if not os.path.exists(self.input_path):
            raise FileNotFoundError(f"Input file not found: {self.input_path}")

        self.data = pd.read_csv(self.input_path)


        self.data.dropna(subset=['date', 'rating', 'review'], inplace=True)


        self.data = self.data[(self.data['rating'].astype(float) >= 0) & (self.data['rating'].astype(float) <= 5)]
        self.data['review_length'] = self.data['review'].str.len()
        self.data = self.data[(self.data['review_length'] >= 10) & (self.data['review_length'] <= 500)]


    def feature_engineering(self):
        self.data['date'] = pd.to_datetime(self.data['date'], errors='coerce')
        self.data['year'] = self.data['date'].dt.year
        self.data['month'] = self.data['date'].dt.month
        self.data['weekday'] = self.data['date'].dt.day_name()

        tfidf = TfidfVectorizer(max_features=100)
        tfidf_matrix = tfidf.fit_transform(self.data['review'])
        tfidf_df = pd.DataFrame(tfidf_matrix.toarray(), columns=tfidf.get_feature_names_out())
        self.data = pd.concat([self.data.reset_index(drop=True), tfidf_df.reset_index(drop=True)], axis=1)

    def save_to_database(self):
        os.makedirs(self.output_dir, exist_ok=True)
        output_path = os.path.join(self.output_dir, f"preprocessed_reviews_rottentomatoes.csv")
        self.data.to_csv(output_path, index=False, encoding='utf-8-sig')

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    default_input_path = os.path.join(current_dir, "..", "crawling", "database", "reviews_rottentomatoes.csv")
    default_output_dir = os.path.join(current_dir, "..", "crawling", "database")

    processor = RottenTomatoesProcessor(
        input_path=default_input_path,
        output_dir=default_output_dir
    )
    processor.preprocess()
    processor.feature_engineering()
    processor.save_to_database()