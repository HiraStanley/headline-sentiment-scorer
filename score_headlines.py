# Imports

import numpy as np
import joblib
from sentence_transformers import SentenceTransformer
from datetime import date

# Load Pre-Trained Model
clf = joblib.load('svm.joblib')
model = SentenceTransformer("all-MiniLM-L6-v2")

# Load heading data
with open('headlines_chicagotribune_2024-12-01.txt', 'r') as file:
    headlines = file.readlines()

# Convert headlines to embeddings
embeddings = model.encode(headlines[0])

# Load the original headlines (needed to print alongside predictions)
with open('headlines_chicagotribune_2024-12-01.txt', 'r') as file:
    headlines = [line.strip() for line in file.readlines()]

# Run predictions
predictions = clf.predict(embeddings)

# Build output filename
TODAY = date.today().strftime('%Y-%m-%d')
output_filename = f"headline_scores_chicagotribune_{TODAY}.txt"

# Write results to file
with open(output_filename, 'w', encoding='utf-8') as file:
    for pred, headline in zip(predictions, headlines):
        file.write(f"{pred}, {headline}\n")

print(f"Results written to {output_filename}")