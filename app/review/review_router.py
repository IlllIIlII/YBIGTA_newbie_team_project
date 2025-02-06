from fastapi import APIRouter, HTTPException
from database.mongodb_connection import mongo_db
from review_analysis.preprocessing.base_processor import BaseDataProcessor

router = APIRouter()

@router.post("/review/preprocess/{site_name}")
async def preprocess_reviews(site_name: str):
    try:
        pass

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
