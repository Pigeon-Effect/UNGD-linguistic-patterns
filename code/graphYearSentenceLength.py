import os
import glob
import re
import nltk
import matplotlib.pyplot as plt
import numpy as np

# Ensure you have NLTK's punkt tokenizer data
nltk.download('punkt')


def preprocess_text(text):
    """Remove paragraph and page numbers formatted as 'number.' from the text."""
    # Define a pattern to identify page/paragraph numbers (e.g., "74." or "75.")
    pattern = r'^\d+\.\s+'

    # Remove numbers at the beginning of lines followed by a space and then preserve the rest of the line
    lines = text.split('\n')
    processed_lines = []

    for line in lines:
        if re.match(pattern, line):
            # Replace the number at the beginning of the line and preserve the rest
            line = re.sub(pattern, '', line, count=1)
        processed_lines.append(line)

    # Join the processed lines back into a single string
    return '\n'.join(processed_lines)


def process_folder_by_session(folder_path):
    """Process each session folder, calculate average sentence length per year."""
    average_sentence_lengths = []
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
            year_sentence_lengths = []
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

                    # Tokenize sentences and words
                    sentences = nltk.sent_tokenize(preprocessed_content)
                    if not sentences:
                        continue  # Skip if no sentences found

                    # Calculate sentence lengths
                    sentence_lengths = [len(nltk.word_tokenize(sentence)) for sentence in sentences]
                    average_sentence_length = sum(sentence_lengths) / len(sentence_lengths)
                    year_sentence_lengths.append(average_sentence_length)

            # Calculate the average sentence length for the year
            if year_sentence_lengths:
                avg_sentence_length = sum(year_sentence_lengths) / len(year_sentence_lengths)
                average_sentence_lengths.append(avg_sentence_length)
                years.append(year)
            else:
                print(f"No valid text files found for year: {year}")

    if not years:
        print("No data found. Please check the folder path and structure.")
    return years, average_sentence_lengths


def plot_sentence_length_timeline(years, average_sentence_lengths, output_path):
    if not years or not average_sentence_lengths:
        print("No data to plot.")
        return

    fig, ax = plt.subplots(figsize=(10, 3))
    ax.plot(years, average_sentence_lengths, marker='o', label='Average Sentence Length')

    # Polynomial regression (e.g., a degree 5 polynomial)
    polynomial_degree = 5
    coefficients = np.polyfit(years, average_sentence_lengths, polynomial_degree)
    polynomial = np.poly1d(coefficients)

    # Generate x values for plotting the polynomial regression curve
    x_values = np.linspace(min(years), max(years), 500)
    y_values = polynomial(x_values)

    # Plot the polynomial regression curve
    ax.plot(x_values, y_values, color='red')

    # Set title with padding
    ax.set_title('S1 - Average Sentence Length from 1946 to 2022', pad=20)

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
output_path = r'C:\Users\juliu\Desktop\DesinformationTermPaper\static\SVGs\s1_average_sentence_length_1946_2022.svg'  # Path to save the SVG file
years, average_sentence_lengths = process_folder_by_session(folder_path)
plot_sentence_length_timeline(years, average_sentence_lengths, output_path)
