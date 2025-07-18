from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
import joblib
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Load the pre-trained model
clf = joblib.load('svm.joblib')
model = SentenceTransformer("all-MiniLM-L6-v2")

# HTTP type GET /status will return a JSON object {'status': 'ok'}
@app.get("/status")
def get_status():
    logger.info("Status check endpoint called")
    return {"status": "ok"}

# HTTP type POST will accept a list of headlines and return their labels {'labels': ['Optimistic', 'Optimistic', 'Neutral', 'Pessimistic', ...]}
class HeadlinesRequest(BaseModel):
    headlines: list[str]

@app.post("/score_headlines")
def score_headlines(request: HeadlinesRequest):
    try:
        logger.info("Received request to score headlines")
        embeddings = model.encode(request.headlines)
        predictions = clf.predict(embeddings)
        return {"labels": predictions.tolist()}
    except Exception as e:
        logger.error(f"Error processing request: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")