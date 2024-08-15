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


def extract_numbers(text):
    """Extract meaningful numbers from the text using regular expressions."""
    # Define regex patterns for numbers written as words and as digits
    number_words = r'\b(one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety|hundred|thousand|million|billion|trillion)\b'
    digit_numbers = r'\b\d+(?:[\.,]\d+)?\b'

    # Combine patterns
    combined_pattern = f'{number_words}|{digit_numbers}'

    # Find all matches
    matches = re.findall(combined_pattern, text, re.IGNORECASE)

    # Filter out numbers that might be paragraph or page numbers (e.g., isolated numbers at the start of lines)
    # This is a simple heuristic and may need to be adjusted based on actual data
    meaningful_numbers = [match for match in matches if not re.match(r'^\d{1,2}$', match)]

    return meaningful_numbers


def process_folder_by_session(folder_path):
    """Process each session folder, calculate average number density per year."""
    number_densities = []
    years = []

    session_folders = glob.glob(os.path.join(folder_path, "Session*"))

    for session_folder in session_folders:
        # Extract year from folder name
        match = re.search(r'Session\s\d{2}\s-\s(\d{4})$', session_folder)
        if match:
            year = int(match.group(1))
            '''
            # Skip years 1948 and 1949
            if year in [1948, 1949]:
                continue  # Skip years 1948 and 1949
            '''
            year_number_counts = []
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

                    # Extract numbers from the preprocessed content
                    numbers = extract_numbers(preprocessed_content)
                    # Avoid division by zero
                    total_words = len(nltk.word_tokenize(preprocessed_content))
                    if total_words == 0:
                        continue

                    number_density = len(numbers) / total_words
                    year_number_counts.append(number_density)

            # Calculate the average number density for the year
            if year_number_counts:
                avg_number_density = sum(year_number_counts) / len(year_number_counts)
                number_densities.append(avg_number_density)
                years.append(year)
            else:
                print(f"No valid text files found for year: {year}")

    if not years:
        print("No data found. Please check the folder path and structure.")
    return years, number_densities


def plot_number_density_timeline(years, number_densities, output_path):
    if not years or not number_densities:
        print("No data to plot.")
        return

    fig, ax = plt.subplots(figsize=(10, 3))
    ax.plot(years, number_densities, marker='o', label='Number Density')

    # Polynomial regression (e.g., a degree 5 polynomial)
    polynomial_degree = 5
    coefficients = np.polyfit(years, number_densities, polynomial_degree)
    polynomial = np.poly1d(coefficients)

    # Generate x values for plotting the polynomial regression curve
    x_values = np.linspace(min(years), max(years), 500)
    y_values = polynomial(x_values)

    # Plot the polynomial regression curve
    ax.plot(x_values, y_values, color='red')

    # Set title with padding
    ax.set_title('T3 - Number Rate from 1946 to 2022', pad=20)

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
output_path = r'C:\Users\juliu\Desktop\DesinformationTermPaper\static\SVGs\t3_number_density_1946_2022.svg'  # Path to save the SVG file
years, number_densities = process_folder_by_session(folder_path)
plot_number_density_timeline(years, number_densities, output_path)
