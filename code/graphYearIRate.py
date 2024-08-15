import os
import glob
import re
import nltk
import matplotlib.pyplot as plt

# Ensure you have NLTK's punkt tokenizer data
nltk.download('punkt')

def calculate_first_person_singular_rate(text):
    """Calculate the rate of first-person singular pronouns in the text."""
    first_person_singular = {"i", "me", "my", "mine", "myself"}

    # Tokenize the text into words
    words = nltk.word_tokenize(text.lower())
    total_words = len(words)
    first_person_singular_count = sum(1 for word in words if word in first_person_singular)

    # Calculate the rate of first-person singular pronouns
    if total_words == 0:
        return 0
    return first_person_singular_count / total_words

def process_folder(folder_path):
    first_person_singular_rates = []
    years = []

    txt_files = glob.glob(os.path.join(folder_path, "*.txt"))

    for txt_file in txt_files:
        # Extract year from filename
        match = re.search(r'(\d{4})\.txt$', txt_file)
        if match:
            year = int(match.group(1))
            with open(txt_file, 'r', encoding='utf-8') as file:
                content = file.read()
                first_person_singular_rate = calculate_first_person_singular_rate(content)
                first_person_singular_rates.append(first_person_singular_rate)
                years.append(year)

    return years, first_person_singular_rates

def plot_first_person_singular_rate_timeline(years, first_person_singular_rates, output_path):
    plt.figure(figsize=(10, 5))
    plt.plot(years, first_person_singular_rates, marker='o')
    plt.title('First-Person Singular Pronoun Rate from 1946 to 2022')
    plt.grid(True)

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
folder_path = r'C:\Users\juliu\Desktop\DesinformationTermPaper\static\mergedTxtByYears'  # Path to your folder
output_path = r'C:\Users\juliu\Desktop\DesinformationTermPaper\static\mergedTxtByYears\first_person_singular_rate_1946_2022.svg'  # Path to save the SVG file
years, first_person_singular_rates = process_folder(folder_path)
plot_first_person_singular_rate_timeline(years, first_person_singular_rates, output_path)
