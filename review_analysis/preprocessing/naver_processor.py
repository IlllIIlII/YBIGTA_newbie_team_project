from review_analysis.preprocessing.base_processor import BaseDataProcessor
from base_processor import BaseDataProcessor
from abc import ABC, abstractmethod
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import numpy as np
import re
from datetime import datetime
import os

'''
        # 결측치 처리       
        # 이상치 처리: 별점 범위 제한 (1~10)
        # 텍스트 데이터 전처리: 비정상적으로 긴 리뷰 제한, 특수문자 제거
        # 파생 변수 생성: 시간대별 리뷰 개수
        # TF-IDF 벡터화
'''
class NaverProcessor(BaseDataProcessor):
    def __init__(self, input_path: str, output_path: str):
        super().__init__(input_path, output_path)
        self.df = pd.read_csv(f'{input_path}', encoding='utf-8-sig')

    def preprocess(self):
        self.df['rating'] = self.df['rating'].str.extract(r'(\d+)').astype(float)
    
        # 결측값 처리
        self.df['rating'] = self.df['rating'].fillna(self.df['rating'].median())
        self.df['review'] = self.df['review'].fillna('')
        self.df['date'] = pd.to_datetime(self.df['date'], errors='coerce')

        # 필터링 조건
        self.df = self.df[(self.df['rating'] >= 0) & (self.df['rating'] <= 10.0)]
        print(f"After Rating Filter: {self.df.shape}")

        self.df['review_length'] = self.df['review'].apply(lambda x: len(x))
        self.df = self.df[self.df['review_length'] <= 2000]

        self.df['review'] = self.df['review'].apply(lambda x: re.sub(r'[^\w\s]', '', x))

    def feature_engineering(self):
        self.df['year'] = self.df['date'].dt.year
        self.df['month'] = self.df['date'].dt.month
        self.df['weekday'] = self.df['date'].dt.day_name()

        tfidf = TfidfVectorizer(max_features=100)
        tfidf_matrix = tfidf.fit_transform(self.df['review'])
        tfidf_df = pd.DataFrame(tfidf_matrix.toarray(), columns=tfidf.get_feature_names_out())
        self.df = pd.concat([self.df.reset_index(drop=True), tfidf_df.reset_index(drop=True)], axis=1)

    def save_to_database(self):
        os.makedirs(self.output_dir, exist_ok=True)
        output_path = os.path.join(self.output_dir, f"preprocessed_reviews_naver.csv")
        self.df.to_csv(output_path, index=False, encoding='utf-8-sig')

