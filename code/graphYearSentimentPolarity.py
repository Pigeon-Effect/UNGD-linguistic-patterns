import os
import glob
import re
import nltk
import matplotlib.pyplot as plt
import numpy as np
from textblob import TextBlob
from nltk.tokenize import sent_tokenize, word_tokenize

# Ensure you have NLTK's punkt tokenizer data
nltk.download('punkt')


def preprocess_text(text):
    """Remove paragraph and page numbers formatted as 'number.' from the text."""
    pattern = r'^\d+\.\s+'
    lines = text.split('\n')
    processed_lines = []
    for line in lines:
        if re.match(pattern, line):
            line = re.sub(pattern, '', line, count=1)
        processed_lines.append(line)
    return '\n'.join(processed_lines)


def calculate_sentiment_polarity(text):
    """Calculate the sentiment polarity for the given text using TextBlob."""
    blob = TextBlob(text)
    return blob.sentiment.polarity


def process_folder_by_session(folder_path):
    """Process each session folder, calculate average sentiment polarity per year."""
    sentiment_polarities = []
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
            year_sentiment_polarities = []
            print(f"Processing year: {year}")

            # Process each txt file in the session folder
            txt_files = glob.glob(os.path.join(session_folder, "*.txt"))
            for txt_file in txt_files:
                with open(txt_file, 'r', encoding='utf-8') as file:
                    content = file.read()
                    # Preprocess the text to remove page/paragraph numbers
                    preprocessed_content = preprocess_text(content)

                    if not preprocessed_content.strip():
                        continue  # Skip empty content after preprocessing

                    # Calculate the sentiment polarity for the text
                    sentiment_polarity = calculate_sentiment_polarity(preprocessed_content)
                    year_sentiment_polarities.append(sentiment_polarity)

            # Calculate the average sentiment polarity for the year
            if year_sentiment_polarities:
                avg_sentiment_polarity = sum(year_sentiment_polarities) / len(year_sentiment_polarities)
                sentiment_polarities.append(avg_sentiment_polarity)
                years.append(year)
            else:
                print(f"No valid text files found for year: {year}")

    if not years:
        print("No data found. Please check the folder path and structure.")
    return years, sentiment_polarities


def plot_sentiment_polarity_timeline(years, sentiment_polarities, output_path):
    if not years or not sentiment_polarities:
        print("No data to plot.")
        return

    fig, ax = plt.subplots(figsize=(10, 3))
    ax.plot(years, sentiment_polarities, marker='o', label='Sentiment Polarity')

    # Polynomial regression (e.g., a degree 5 polynomial)
    polynomial_degree = 5
    coefficients = np.polyfit(years, sentiment_polarities, polynomial_degree)
    polynomial = np.poly1d(coefficients)

    # Generate x values for plotting the polynomial regression curve
    x_values = np.linspace(min(years), max(years), 500)
    y_values = polynomial(x_values)

    # Plot the polynomial regression curve
    ax.plot(x_values, y_values, color='red')

    # Set title with padding
    ax.set_title('S4 - Sentiment Polarity from 1946 to 2022', pad=20)

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
output_path = r'C:\Users\juliu\Desktop\DesinformationTermPaper\static\SVGs\s4_sentiment_polarity_1946_2022.svg'  # Path to save the SVG file
years, sentiment_polarities = process_folder_by_session(folder_path)
plot_sentiment_polarity_timeline(years, sentiment_polarities, output_path)
