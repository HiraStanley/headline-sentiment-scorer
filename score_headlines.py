"""
score_headlines.py

Usage:
    python score_headlines.py <input_file> <source>

Example:
    python score_headlines.py sample_headlines.txt chicagotribune

Arguments:
    <input_file>  A text file with one headline per line.
    <source>      The news source name (e.g., nyt, chicagotribune).

If the required arguments are not provided, the program will display a helpful error message.
"""

# Imports

import sys
import numpy as np
import joblib
from sentence_transformers import SentenceTransformer
from datetime import date

def main():
    """
    Main function to score headlines using a pre-trained SVM model and SentenceTransformer.
    It reads headlines from a file, converts them to embeddings, and predicts their scores.
    """
    # User input: filename and source
    if len(sys.argv) != 3:
        print("\nOops! You must provide two arguments: the input file and the source name.")
        print("Correct usage:")
        print("    python score_headlines.py <input_file> <source>")
        print("\nExample:")
        print("    python score_headlines.py sample_headlines.txt chicagotribune\n")
        sys.exit(1)

    # Read command line arguments
    filename = sys.argv[1]
    source = sys.argv[2]

    # Load Pre-Trained Model
    clf = joblib.load('svm.joblib')
    model = SentenceTransformer("all-MiniLM-L6-v2")

    # Load and clean headlines data. Exception handling for file not found.
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            headlines = [line.strip() for line in file.readlines()]
    except FileNotFoundError:
        print(f"\nError: The file '{filename}' was not found. Please check the file name and try again.\n")
        sys.exit(1)

    # Convert headlines to embeddings
    embeddings = model.encode(headlines)

    # Run predictions
    predictions = clf.predict(embeddings)

    # Build output filename
    TODAY = date.today().strftime('%Y_%m_%d')
    #output_filename = f"headline_scores_{source}_{TODAY}.txt"
    output_filename = f"/app/data/headline_scores_hirastanley_{source}_{TODAY}.txt"

    # Write results to file
    with open(output_filename, 'w', encoding='utf-8') as file:
        for pred, headline in zip(predictions, headlines):
            file.write(f"{pred}, {headline}\n")

    print(f"Results written to {output_filename}")
    print("\n")

if __name__ == "__main__":
    main()