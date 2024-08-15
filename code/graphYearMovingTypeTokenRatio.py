import os
import glob
import re
import nltk
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter

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


def calculate_moving_ttr(text, window_size=500):
    """Calculate the average moving type-token ratio (TTR) for the given text."""
    words = nltk.word_tokenize(text.lower())
    if len(words) < window_size:
        return 0

    ttr_values = []

    for i in range(len(words) - window_size + 1):
        window = words[i:i + window_size]
        unique_types = len(set(window))
        ttr = unique_types / len(window)
        ttr_values.append(ttr)

    return np.mean(ttr_values) if ttr_values else 0


def process_folder_by_session(folder_path):
    """Process each session folder, calculate average moving TTR per year."""
    average_ttr_values = []
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

            year_ttr_values = []
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

                    # Calculate the moving TTR for the text
                    moving_ttr = calculate_moving_ttr(preprocessed_content)
                    year_ttr_values.append(moving_ttr)

            # Calculate the average moving TTR for the year
            if year_ttr_values:
                avg_ttr = sum(year_ttr_values) / len(year_ttr_values)
                average_ttr_values.append(avg_ttr)
                years.append(year)
            else:
                print(f"No valid text files found for year: {year}")

    if not years:
        print("No data found. Please check the folder path and structure.")
    return years, average_ttr_values


def plot_ttr_timeline(years, average_ttr_values, output_path):
    if not years or not average_ttr_values:
        print("No data to plot.")
        return

    fig, ax = plt.subplots(figsize=(10, 3))
    ax.plot(years, average_ttr_values, marker='o', label='Average Moving TTR')

    # Polynomial regression (e.g., a degree 5 polynomial)
    polynomial_degree = 5
    coefficients = np.polyfit(years, average_ttr_values, polynomial_degree)
    polynomial = np.poly1d(coefficients)

    # Generate x values for plotting the polynomial regression curve
    x_values = np.linspace(min(years), max(years), 500)
    y_values = polynomial(x_values)

    # Plot the polynomial regression curve
    ax.plot(x_values, y_values, color='red')

    # Set title with padding
    ax.set_title('S2 - Lexical Diversity (MATTR) from 1946 to 2022', pad=20)

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
output_path = r'C:\Users\juliu\Desktop\DesinformationTermPaper\static\SVGs\window_size_500_s2_average_moving_ttr_1946_2022.svg'  # Path to save the SVG file
years, average_ttr_values = process_folder_by_session(folder_path)
plot_ttr_timeline(years, average_ttr_values, output_path)
