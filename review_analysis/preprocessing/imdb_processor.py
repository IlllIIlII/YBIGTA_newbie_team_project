from review_analysis.preprocessing.base_processor import BaseDataProcessor
import pandas as pd

class ImdbProcessor(BaseDataProcessor):
    """
    A class to preprocess and feature engineer IMDb movie reviews dataset.
    
    This class is responsible for loading a CSV file containing movie reviews,
    performing data cleaning and preprocessing tasks, and applying feature engineering
    techniques to the dataset. The processed data is then saved to a specified output path.

    Attributes:
        df (pandas.DataFrame): The DataFrame containing the movie reviews data.
        output_path (str): The path where the processed data will be saved.

    Methods:
        preprocess():
            Cleans and preprocesses the dataset by handling missing values, converting data types,
            and filtering out outliers in the data.
        
        feature_engineering():
            Creates additional features by segmenting reviews based on text length into bins.
        
        save_to_database():
            Saves the processed dataset to a CSV file in the specified output path.
    """

    def __init__(self, input_path: str, output_path: str):
        """
        Initializes the ImdbProcessor with the paths for input and output files.

        Args:
            input_path (str): The path to the input CSV file containing the movie reviews.
            output_path (str): The path where the processed dataset will be saved.
        """

        super().__init__(input_path, output_path)
        self.df = pd.read_csv(f'{input_path}', encoding='utf-8-sig')
        self.output_path = output_path

    def preprocess(self):
        """
        Cleans and preprocesses the movie reviews dataset by:

        - Converting 'rating' column to numeric, handling errors by coercing invalid values to NaN.
        - Calculating the length of each review and storing it in a new column 'text_length'.
        - Replacing extreme values in 'text_length' (values >= 2000) with the median length.
        - Filling missing values in 'rating' column with the median value.
        - Filtering the dataset to ensure 'rating' is between 1 and 10.
        - Converting 'date' column to datetime format and filtering reviews within a defined date range.

        The cleaned dataset is stored in the `self.df` attribute.
        """

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
        """
        Applies feature engineering techniques on the preprocessed dataset:

        - Bins the 'text_length' into 200-character intervals and assigns the resulting 
          bin labels to a new column 'length_group'.

        The updated dataset with the new 'length_group' column is stored in the `self.df` attribute.
        """
        bins = range(0, self.df['text_length'].max() + 200, 200)
        labels = [f"{i}-{i+199}" for i in bins[:-1]]
        self.df['length_group'] = pd.cut(self.df['text_length'], bins=bins, labels=labels, right=False)

    def save_to_database(self):
        """
        Saves the processed DataFrame to a CSV file in the specified output directory.

        The processed data includes the columns: 'date', 'rating', 'text_length', 
        'length_group', and 'review'. The file is saved with UTF-8 encoding and a 
        BOM header for compatibility with Excel.

        The output file is saved in the path provided by the `output_path` attribute.
        """
        self.df = self.df.reindex(columns=['date', 'rating', 'text_length', 'length_group','review'])
        self.df.to_csv(f'{self.output_path}/preprocessed_reviews_imdb.csv', encoding='utf-8-sig', index=False)
