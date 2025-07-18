# Headlines to Sentiment

This project deploys a sentiment model that classifies news headlines into three categories:  
*Optimistic*  
*Neutral*  
*Pessimistic*

The sentiment scores will be used to track daily news sentiment, providing valuable signals to clients such as hedge funds and government agencies.

## Project Structure

- `score_headlines.py`: Scores headlines from a text file using the trained sentiment model.
- `headline_scraper.py`: Scrapes headlines from the Chicago Tribune, New York Times, or LA Times.
- `score_headlines_api.py`: Serves the sentiment model as a real-time FastAPI web service.
- `svm.joblib`: The pre-trained sentiment classifier.
- `requirements.txt`: List of required Python packages.
- `Assignment1_HiraStanley.ipynb`: Cleaned notebook where I tested code.

## Main Setup

1. Clone the repository:
```bash
git clone https://github.com/HiraStanley/headline-sentiment-scorer.git
cd headline-sentiment-scorer
```
2. (Optional) Create and activate a virtual environment:
```bash
python -m venv pmle
pmle\Scripts\activate
```
3. Install required packages:
```bash
pip install -r requirements.txt
```

## Batch Scoring (Offline)
1. Run the headline scraper. You will be prompted to enter the source (chicagotribune, nyt): nyt. LA Times denies access requests.:
```bash
python headline_scraper.py
```
2. Run the sentiment scorer:
```bash
python score_headlines.py <input_file> <source>
```
Example:
```bash
python score_headlines.py sample_headlines.txt chicagotribune
```

## Real-Time Scoring via FastAPI
1. Run the API server:
```bash
uvicorn score_headlines_api:app --host 0.0.0.0 --port {}
```
2. Check server status:
```bash
curl http://localhost:{}/status
```
Expected output:
{"status": "ok"}
insert
```
3. Send headlines for real-time scoring:
```bash
curl -X POST http://localhost:{}/score_headlines -H "Content-Type: application/json" -d "{\"headlines\": [\"Stocks come crashing\", \"1000 Murdered\"]}"
```
Expected output:
```bash
{"labels": ["Pessimistic", "Pessimistic"]}
```