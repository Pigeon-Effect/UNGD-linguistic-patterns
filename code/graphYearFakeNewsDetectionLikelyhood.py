import os
import glob
import re
import matplotlib.pyplot as plt
import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer
from nltk.tokenize import sent_tokenize
import nltk
import numpy as np

# Ensure you have NLTK's punkt tokenizer data
nltk.download('punkt')


def remove_numbered_labels(text):
    """Remove numbered labels from the text."""
    return re.sub(r'\b\d+\.\s+', '', text)


# Load the fake news detection model and tokenizer
model_name = "mrm8488/bert-tiny-finetuned-fake-news-detection"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)


def calculate_fake_news_likelihood(text):
    """Estimate the likelihood of fake news in the text using the pre-trained model."""
    sentences = sent_tokenize(text)
    probabilities = []

    for sentence in sentences:
        inputs = tokenizer(sentence, return_tensors="pt", truncation=True, padding=True, max_length=512)
        with torch.no_grad():
            outputs = model(**inputs)
        logits = outputs.logits
        sentence_probabilities = torch.nn.functional.softmax(logits, dim=-1)
        fake_prob = sentence_probabilities[0][0].item()  # Probability for the 'fake' class
        probabilities.append(fake_prob)

    # Combine probabilities (e.g., by averaging)
    average_probability = sum(probabilities) / len(probabilities) if probabilities else 0
    return average_probability


def process_folder_by_session(folder_path):
    """Process each session folder, calculate average fake news likelihood per year."""
    yearly_probabilities = {}
    years = []

    session_folders = glob.glob(os.path.join(folder_path, "Session*"))

    for session_folder in session_folders:
        # Extract year from folder name
        match = re.search(r'Session\s\d{2}\s-\s(\d{4})$', session_folder)
        if match:
            year = int(match.group(1))

            # Skip years 1948 and 1949
            if year in [1948, 1949]:
                continue  # Skip years 1948 and 1949
            year_probabilities = []
            print(f"Processing year: {year}")

            # Process each txt file in the session folder
            txt_files = glob.glob(os.path.join(session_folder, "*.txt"))
            for txt_file in txt_files:
                with open(txt_file, 'r', encoding='utf-8') as file:
                    content = file.read()
                    # Preprocess the text to remove page/paragraph numbers
                    preprocessed_content = remove_numbered_labels(content)

                    if not preprocessed_content.strip():
                        continue  # Skip empty content after preprocessing

                    # Calculate the fake news likelihood for the text
                    fake_news_likelihood = calculate_fake_news_likelihood(preprocessed_content)
                    year_probabilities.append(fake_news_likelihood)

            # Calculate the average fake news likelihood for the year
            if year_probabilities:
                avg_fake_news_likelihood = sum(year_probabilities) / len(year_probabilities)
                yearly_probabilities[year] = avg_fake_news_likelihood
                years.append(year)

    if not years:
        print("No data found. Please check the folder path and structure.")
    return years, [yearly_probabilities[year] for year in years]


def plot_fake_news_likelihood_timeline(years, average_probabilities, output_path):
    if not years or not average_probabilities:
        print("No data to plot.")
        return

    fig, ax = plt.subplots(figsize=(10, 3))
    ax.plot(years, average_probabilities, marker='o', label='Fake News Likelihood')

    # Polynomial regression (e.g., a degree 5 polynomial)
    polynomial_degree = 5
    coefficients = np.polyfit(years, average_probabilities, polynomial_degree)
    polynomial = np.poly1d(coefficients)

    # Generate x values for plotting the polynomial regression curve
    x_values = np.linspace(min(years), max(years), 500)
    y_values = polynomial(x_values)

    # Plot the polynomial regression curve
    ax.plot(x_values, y_values, color='red')

    # Set title with padding
    ax.set_title('C1 - Fake News Likelihood from 1946 to 2022', pad=20)

    ax.grid(True)

    # Set ticks for every fifth year
    tick_positions = list(range(1950, max(years) + 1, 5))
    plt.xticks(tick_positions, rotation=45)

    # Adding grid lines for every fifth year
    plt.gca().set_xticks(tick_positions, minor=True)
    plt.grid(which='both')
    plt.grid(which='major', linestyle='-', linewidth='0.5', color='black')
    plt.grid(which='minor', linestyle=':', linewidth='0.5', color='gray')

    # Ensure the y-axis does not use scientific notation
    plt.gca().get_yaxis().get_major_formatter().set_scientific(False)

    plt.tight_layout()
    plt.savefig(output_path, format='svg')
    plt.show()


# Example usage:
folder_path = r'C:\Users\juliu\Desktop\DesinformationTermPaper\static\Converted sessions'  # Path to your session folders
output_path = r'C:\Users\juliu\Desktop\DesinformationTermPaper\static\SVGs\c1_fake_news_likelihood_1946_2022.svg'  # Path to save the SVG file
years, average_probabilities = process_folder_by_session(folder_path)
plot_fake_news_likelihood_timeline(years, average_probabilities, output_path)
