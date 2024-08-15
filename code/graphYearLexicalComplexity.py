import os
import glob
import re
import matplotlib.pyplot as plt


def remove_numbered_labels(text):
    """Remove numbered labels from the text."""
    return re.sub(r'\b\d+\.\s+', '', text)


def clean_text(text):
    """Remove numbered labels and replace newlines with spaces."""
    text = remove_numbered_labels(text)
    return text.replace('\n', ' ')


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


def process_folder(folder_path):
    lexical_diversities = []
    years = []

    txt_files = glob.glob(os.path.join(folder_path, "*.txt"))

    for txt_file in txt_files:
        # Extract year from filename
        match = re.search(r'(\d{4})\.txt$', txt_file)
        if match:
            year = int(match.group(1))
            with open(txt_file, 'r', encoding='utf-8') as file:
                content = file.read()
                cleaned_content = clean_text(content)
                lexical_diversity = get_lexical_diversity(cleaned_content)
                lexical_diversities.append(lexical_diversity)
                years.append(year)

    return years, lexical_diversities


def plot_lexical_diversity_timeline(years, lexical_diversities, output_path):
    fig, ax = plt.subplots(figsize=(10, 3))
    ax.plot(years, lexical_diversities, marker='o')

    # Set title with padding
    ax.set_title('Lexical Diversity (MATTR) from 1946 to 2022', pad=20)

    ax.grid(True)

    # Set ticks for every fifth year
    tick_positions = list(range(1950, max(years) + 1, 5))
    ax.set_xticks(tick_positions)
    ax.set_xticklabels(tick_positions, rotation=45)

    # Adding grid lines for every fifth year
    ax.set_xticks(tick_positions, minor=True)
    ax.grid(which='both')
    ax.grid(which='major', linestyle='-', linewidth='0.5', color='black')
    ax.grid(which='minor', linestyle=':', linewidth='0.5', color='gray')

    plt.tight_layout()
    plt.savefig(output_path, format='svg')
    plt.show()


# Example usage:
folder_path = r'C:\Users\juliu\Desktop\DesinformationTermPaper\static\mergedTxtByYears'  # Path to your folder
output_path = r'C:\Users\juliu\Desktop\DesinformationTermPaper\static\SVGs\lexical_diversity_1946_2022.svg'  # Path to save the SVG file
years, lexical_diversities = process_folder(folder_path)
plot_lexical_diversity_timeline(years, lexical_diversities, output_path)
