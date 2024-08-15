from flask import Flask, render_template, jsonify, request
import os
import re
import logging
import textstat
import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer
from nltk.tokenize import sent_tokenize, word_tokenize

from textblob import TextBlob

app = Flask(__name__)

# Path to the folder containing text files
BASE_PATH = 'C:/Users/juliu/Desktop/DesinformationTermPaper/static/Converted sessions/'

# Load the fake news detection model and tokenizer
model_name = "mrm8488/bert-tiny-finetuned-fake-news-detection"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)

def calculate_average_sentence_length(text):
    """Calculate the average number of words per sentence in the text."""
    sentences = sent_tokenize(text)
    word_counts = [len(word_tokenize(sentence)) for sentence in sentences]
    average_length = sum(word_counts) / len(word_counts) if word_counts else 0
    return average_length

def split_text(text, max_length=512):
    """Split text into chunks of a maximum token length."""
    words = text.split()
    chunks = []
    current_chunk = []

    token_count = 0
    for word in words:
        token_count += len(tokenizer.tokenize(word))
        if token_count > max_length:
            chunks.append(' '.join(current_chunk))
            current_chunk = [word]
            token_count = len(tokenizer.tokenize(word))
        else:
            current_chunk.append(word)

    if current_chunk:
        chunks.append(' '.join(current_chunk))

    return chunks

def get_fake_news_likelihood(text):
    """Estimate the likelihood of fake news in the text using the pre-trained model."""
    chunks = split_text(text)
    probabilities = []

    for chunk in chunks:
        inputs = tokenizer(chunk, return_tensors="pt", truncation=True, padding=True, max_length=512)
        with torch.no_grad():
            outputs = model(**inputs)
        logits = outputs.logits
        chunk_probabilities = torch.nn.functional.softmax(logits, dim=-1)
        probabilities.append(chunk_probabilities[0][0].item())  # Probability for the 'fake' class

    # Combine probabilities (e.g., by averaging)
    average_probability = sum(probabilities) / len(probabilities) if probabilities else 0
    return average_probability


def get_sentiment(text):
    """Perform sentiment analysis using TextBlob."""
    blob = TextBlob(text)
    return blob.sentiment.polarity  # Returns sentiment polarity: -1 (negative) to 1 (positive)

def get_subjectivity(text):
    """Measure the subjectivity of a text using TextBlob."""
    blob = TextBlob(text)
    return blob.sentiment.subjectivity  # Returns subjectivity: 0 (objective) to 1 (subjective)

def get_readability(text):
    """Measure the readability of a text using Fleschs Reading Ease"""
    readability = textstat.flesch_reading_ease(text)
    return readability


def get_lexical_diversity(text, window_size=100):
    """Calculate the Moving Average Type-Token Ratio (MATTR) for lexical diversity."""
    words = text.split()
    if len(words) < window_size:
        window_size = len(words)

    ttr_list = []
    for i in range(len(words) - window_size + 1):
        window = words[i:i + window_size]
        ttr = len(set(window)) / len(window)
        ttr_list.append(ttr)

    lexical_diversity = sum(ttr_list) / len(ttr_list)
    return lexical_diversity

# Configure logging
logging.basicConfig(level=logging.DEBUG)

@app.route("/")
def hello_world():
    return render_template("index.html")
@app.route("/graph_04")
def graph_04():
    return render_template("graph_04.html")

@app.route("/graph_05")
def graph_05():
    return render_template("graph_05.html")

@app.route("/graph_06")
def graph_06():
    return render_template("graph_06.html")

@app.route("/graph_07")
def graph_07():
    return render_template("graph_07.html")

@app.route("/graph_08")
def graph_08():
    return render_template("graph_08.html")

@app.route("/graph_09")
def graph_09():
    return render_template("graph_09.html")

@app.route("/graph_10")
def graph_10():
    return render_template("graph_10.html")



@app.route("/data")
def get_data():
    year = request.args.get('year', default='1946', type=str)
    session_number = str(int(year) - 1945).zfill(2)
    folder_path = os.path.join(BASE_PATH, f"Session {session_number} - {year}")

    if not os.path.exists(folder_path):
        return jsonify({"error": "Folder not found"}), 404

    sentiment_scores = {}
    for filename in os.listdir(folder_path):
        if filename.endswith('.txt'):
            country_code = filename[:3]  # Extract the country code
            file_path = os.path.join(folder_path, filename)
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    text = file.read()
                    sentiment_score = get_sentiment(text)
                    sentiment_scores[country_code] = sentiment_score
            except Exception as e:
                print(f"Error processing file {filename}: {e}")
                sentiment_scores[country_code] = None

    return jsonify(sentiment_scores)


@app.route("/data2")
def get_data2():
    year = request.args.get('year', default='1946', type=str)
    session_number = str(int(year) - 1945).zfill(2)
    folder_path = os.path.join(BASE_PATH, f"Session {session_number} - {year}")

    if not os.path.exists(folder_path):
        return jsonify({"error": "Folder not found"}), 404

    subjectivity_scores = {}
    for filename in os.listdir(folder_path):
        if filename.endswith('.txt'):
            country_code = filename[:3]  # Extract the country code
            file_path = os.path.join(folder_path, filename)
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    text = file.read()
                    subjectivity_score = get_subjectivity(text)
                    subjectivity_scores[country_code] = subjectivity_score
            except Exception as e:
                print(f"Error processing file {filename}: {e}")
                subjectivity_scores[country_code] = None

    return jsonify(subjectivity_scores)

@app.route("/data3")
def get_data3():
    year = request.args.get('year', default='1946', type=str)
    session_number = str(int(year) - 1945).zfill(2)
    folder_path = os.path.join(BASE_PATH, f"Session {session_number} - {year}")

    if not os.path.exists(folder_path):
        return jsonify({"error": "Folder not found"}), 404

    readability_scores = {}
    for filename in os.listdir(folder_path):
        if filename.endswith('.txt'):
            country_code = filename[:3]  # Extract the country code
            file_path = os.path.join(folder_path, filename)
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    text = file.read()
                    readability_score = get_readability(text)
                    readability_scores[country_code] = readability_score
            except Exception as e:
                print(f"Error processing file {filename}: {e}")
                readability_scores[country_code] = None

    return jsonify(readability_scores)

@app.route("/data4")
def get_data4():
    year = request.args.get('year', default='1946', type=str)
    session_number = str(int(year) - 1945).zfill(2)
    folder_path = os.path.join(BASE_PATH, f"Session {session_number} - {year}")

    if not os.path.exists(folder_path):
        return jsonify({"error": "Folder not found"}), 404

    lexical_diversity_scores = {}
    for filename in os.listdir(folder_path):
        if filename.endswith('.txt'):
            country_code = filename[:3]  # Extract the country code
            file_path = os.path.join(folder_path, filename)
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    text = file.read()
                    lexical_diversity_score = get_lexical_diversity(text)
                    lexical_diversity_scores[country_code] = lexical_diversity_score
            except Exception as e:
                print(f"Error processing file {filename}: {e}")
                lexical_diversity_scores[country_code] = None

    return jsonify(lexical_diversity_scores)

@app.route("/data5")
def get_data5():
    year = request.args.get('year', default='1946', type=str)
    session_number = str(int(year) - 1945).zfill(2)
    folder_path = os.path.join(BASE_PATH, f"Session {session_number} - {year}")

    if not os.path.exists(folder_path):
        return jsonify({"error": "Folder not found"}), 404

    fake_news_likelihoods = {}
    for filename in os.listdir(folder_path):
        if filename.endswith('.txt'):
            country_code = filename[:3]  # Extract the country code
            file_path = os.path.join(folder_path, filename)
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    text = file.read()
                    fake_news_likelihood = get_fake_news_likelihood(text)
                    fake_news_likelihoods[country_code] = fake_news_likelihood
            except Exception as e:
                print(f"Error processing file {filename}: {e}")
                fake_news_likelihoods[country_code] = None

    return jsonify(fake_news_likelihoods)

@app.route("/data6")
def get_data6():
    year = request.args.get('year', default='1946', type=str)
    session_number = str(int(year) - 1945).zfill(2)
    folder_path = os.path.join(BASE_PATH, f"Session {session_number} - {year}")

    if not os.path.exists(folder_path):
        return jsonify({"error": "Folder not found"}), 404

    average_sentence_lengths = {}
    for filename in os.listdir(folder_path):
        if filename.endswith('.txt'):
            country_code = filename[:3]  # Extract the country code
            file_path = os.path.join(folder_path, filename)
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    text = file.read()
                    average_length = calculate_average_sentence_length(text)
                    average_sentence_lengths[country_code] = average_length
            except Exception as e:
                print(f"Error processing file {filename}: {e}")
                average_sentence_lengths[country_code] = None

    return jsonify(average_sentence_lengths)

if __name__ == "__main__":
    app.run(debug=True)
