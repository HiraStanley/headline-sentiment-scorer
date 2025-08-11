# Use the official Python image as a base
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY score_headlines.py /app/
COPY svm.joblib /app/

# Command to run the application
ENTRYPOINT ["python", "score_headlines.py"]
# Fallback default arguments
CMD ["sample_headlines.txt", "chicagotribune"]

# Build the Docker image:
# docker build -t score-headlines .

# Run the Docker container with two required arguments (%cd% for Windows command prompt):
# docker run --rm -v "%cd%:/app" score-headlines sample_headlines.txt chicagotribune