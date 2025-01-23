from review_analysis.preprocessing.base_processor import BaseDataProcessor
import pandas as pd

class ImdbProcessor(BaseDataProcessor):
    def __init__(self, input_path: str, output_path: str):
        super().__init__(input_path, output_path)
        self.df = pd.read_csv(f'{input_path}', encoding='utf-8-sig')
        self.output_path = output_path

    def preprocess(self):
        self.df['rating'] = pd.to_numeric(self.df['rating'], errors='coerce')
        self.df['text_length'] = self.df['review'].apply(lambda x: len(x) if isinstance(x, str) else 0)

        median_value = self.df['text_length'].median()
        median_value = int(median_value)
        self.df['text_length'] = self.df['text_length'].apply(lambda x: median_value if x >= 2000 else x)


        self.df['rating'] = self.df['rating'].fillna(self.df['rating'].median())
        self.df = self.df[(self.df['rating'] >= 1) & (self.df['rating'] <= 10)]

        self.df['date'] = pd.to_datetime(self.df['date'], errors='coerce')
        start_date = '2019-04-24'
        end_date = '2025-01-10'
        self.df = self.df[(self.df['date'] >= start_date) & (self.df['date'] <= end_date)]
            
    def feature_engineering(self):
        bins = range(0, self.df['text_length'].max() + 200, 200)
        labels = [f"{i}-{i+199}" for i in bins[:-1]]
        self.df['length_group'] = pd.cut(self.df['text_length'], bins=bins, labels=labels, right=False)

    def save_to_database(self):
        self.df = self.df.reindex(columns=['date', 'rating', 'text_length', 'length_group','review'])
        self.df.to_csv(f'{self.output_path}/preprocessed_reviews_imdb.csv', encoding='utf-8-sig', index=False)
