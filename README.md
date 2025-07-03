# Headlines to Sentiment

This project deploys a sentiment model that classifies news headlines into three categories:  
*Optimistic*  
*Neutral*  
*Pessimistic*

The sentiment scores will be used to track daily news sentiment, providing valuable signals to clients such as hedge funds and government agencies.

## Project Structure

- `score_headlines.py`: Scores headlines from a text file using the trained sentiment model.
- `headline_scraper.py`: Scrapes headlines from the Chicago Tribune, New York Times, or LA Times.
- `svm.joblib`: The pre-trained sentiment classifier.
- `requirements.txt`: List of required Python packages.
- `Assignment1_HiraStanley.ipynb`: Cleaned notebook where I tested code.

## Usage

1. Clone the repository:
git clone https://github.com/HiraStanley/headline-sentiment-scorer.git
cd headline-sentiment-scorer

2. Install required packages:
pip install -r requirements.txt

3. Run the headline scraper:
python headline_scraper.py

You will be prompted to enter the source (chicagotribune, nyt): nyt. LA Times denies access requests.

4. Run the sentiment scorer:
python score_headlines.py <input_file> <source>

Example:
python score_headlines.py sample_headlines.txt chicagotribune

