from typing import Dict, Type
from fastapi import APIRouter, HTTPException
from database.mongodb_connection import mongo_db
from review_analysis.preprocessing.base_processor import BaseDataProcessor
from review_analysis.preprocessing.imdb_processor import ImdbProcessor
from review_analysis.preprocessing.rottentomatoes_processor import RottenTomatoesProcessor
from review_analysis.preprocessing.naver_processor import NaverProcessor

router = APIRouter()

PREPROCESS_CLASSES: Dict[str, Type[BaseDataProcessor]] = {
    "imdb": ImdbProcessor,
    "rottentomatoes": RottenTomatoesProcessor,
    "naver": NaverProcessor,
}

@router.post("/review/preprocess/{site_name}")
def preprocess_reviews(site_name: str):
    try:
        collection = mongo_db[site_name]
    except:
        raise HTTPException(status_code=400, detail="site not exist")
    
    processor_class = PREPROCESS_CLASSES.get(site_name)
    
    if not processor_class:
        raise HTTPException(status_code=400, detail=f"Processor for {site_name} not found")
    
    processor = processor_class(collection)
    
    try:
        processed_data = processor.preprocess()
        collection.insert_many(processed_data)
        
        return {"message": "Reviews preprocessed successfully"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred during preprocessing: {str(e)}")