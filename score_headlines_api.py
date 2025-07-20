"""API service to score news headlines as Optimistic, Neutral, or Pessimistic using a pre-trained sentiment classifier."""

import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
import joblib

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Load the pre-trained model and transformer
clf = joblib.load('svm.joblib')
model = SentenceTransformer("all-MiniLM-L6-v2")

@app.get("/status")
def get_status():
    """
    Health check endpoint to verify that the API is running.
    Returns:
        dict: A dictionary indicating the status of the API.
    """
    logger.info("Status check endpoint called")
    return {"status": "ok"}

class HeadlinesRequest(BaseModel):
    """
    Request schema for /score_headlines endpoint.

    Attributes:
        headlines (list[str]): A list of headline strings to be scored.
    """
    headlines: list[str]

@app.post("/score_headlines")
def score_headlines(request: HeadlinesRequest):
    """
    Scores a list of headlines using the sentiment classifier.

    Args:
        request (HeadlinesRequest): A request body containing a list of headlines.

    Returns:
        dict: A dictionary with sentiment labels corresponding to each headline.
    """
    try:
        logger.info("Received request to score headlines")
        embeddings = model.encode(request.headlines)
        predictions = clf.predict(embeddings)
        return {"labels": predictions.tolist()}
    except Exception as e:
        logger.error("Error processing request: %s", e)
        raise HTTPException(status_code=500, detail="Internal Server Error") from e