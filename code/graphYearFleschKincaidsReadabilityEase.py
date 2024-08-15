import os
import glob
import re
import nltk
import matplotlib.pyplot as plt
import numpy as np
from nltk.corpus import cmudict
from nltk.tokenize import sent_tokenize, word_tokenize

# Ensure you have NLTK's punkt tokenizer data and CMU Pronouncing Dictionary
nltk.download('punkt')
nltk.download('cmudict')

# Load the CMU Pronouncing Dictionary
d = cmudict.dict()


def syllable_count(word):
    """Return the number of syllables in a word using CMU Pronouncing Dictionary."""
    word = word.lower()
    if word in d:
        return max([len(list(y for y in x if y[-1].isdigit())) for x in d[word]])
    else:
        # Estimate syllables for words not in the dictionary
        return len(re.findall(r'[aeiouy]+', word))


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


def calculate_flesch_kincaid(text):
    """Calculate the Flesch-Kincaid Readability Ease (FKRE) for the given text."""
    sentences = sent_tokenize(text)
    words = word_tokenize(text)

    num_sentences = len(sentences)
    num_words = len(words)
    num_syllables = sum(syllable_count(word) for word in words)

    if num_sentences == 0 or num_words == 0:
        return 0

    # Calculate Flesch-Kincaid Readability Ease
    fk_re = 206.835 - 1.015 * (num_words / num_sentences) - 84.6 * (num_syllables / num_words)
    return fk_re


def process_folder_by_session(folder_path):
    """Process each session folder, calculate average Flesch-Kincaid Readability Ease per year."""
    fk_re_values = []
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
            year_fk_re_values = []
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

                    # Calculate the Flesch-Kincaid Readability Ease for the text
                    fk_re = calculate_flesch_kincaid(preprocessed_content)
                    year_fk_re_values.append(fk_re)

            # Calculate the average FKRE for the year
            if year_fk_re_values:
                avg_fk_re = sum(year_fk_re_values) / len(year_fk_re_values)
                fk_re_values.append(avg_fk_re)
                years.append(year)
            else:
                print(f"No valid text files found for year: {year}")

    if not years:
        print("No data found. Please check the folder path and structure.")
    return years, fk_re_values


def plot_fk_re_timeline(years, fk_re_values, output_path):
    if not years or not fk_re_values:
        print("No data to plot.")
        return

    fig, ax = plt.subplots(figsize=(10, 3))
    ax.plot(years, fk_re_values, marker='o', label='Flesch-Kincaid Readability Ease')

    # Polynomial regression (e.g., a degree 5 polynomial)
    polynomial_degree = 5
    coefficients = np.polyfit(years, fk_re_values, polynomial_degree)
    polynomial = np.poly1d(coefficients)

    # Generate x values for plotting the polynomial regression curve
    x_values = np.linspace(min(years), max(years), 500)
    y_values = polynomial(x_values)

    # Plot the polynomial regression curve
    ax.plot(x_values, y_values, color='red')

    # Set title with padding
    ax.set_title('S3 - Flesch-Kincaid Readability Ease from 1946 to 2022', pad=20)

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
output_path = r'C:\Users\juliu\Desktop\DesinformationTermPaper\static\SVGs\s3_flesch_kincaid_readability_1946_2022.svg'  # Path to save the SVG file
years, fk_re_values = process_folder_by_session(folder_path)
plot_fk_re_timeline(years, fk_re_values, output_path)
