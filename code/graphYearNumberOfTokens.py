import os
import re
import matplotlib.pyplot as plt

def count_tokens_in_session(session_path):
    """Count the number of tokens in all .txt files in a given session folder."""
    total_tokens = 0
    for txt_file in os.listdir(session_path):
        if txt_file.endswith('.txt'):
            with open(os.path.join(session_path, txt_file), 'r', encoding='utf-8') as file:
                content = file.read()
                tokens = content.split()
                total_tokens += len(tokens)
    return total_tokens

def process_all_sessions(base_path):
    """Process all session folders to count the number of tokens for each year."""
    years = []
    token_counts = []

    for session_folder in sorted(os.listdir(base_path)):
        match = re.match(r'Session (\d{2}) - (\d{4})', session_folder)
        if match:
            session_number = int(match.group(1))
            year = int(match.group(2))
            session_path = os.path.join(base_path, session_folder)

            if os.path.isdir(session_path):
                num_tokens = count_tokens_in_session(session_path)
                years.append(year)
                token_counts.append(num_tokens)

    return years, token_counts

def plot_token_counts(years, token_counts, output_path):
    plt.figure(figsize=(10, 3))  # Adjust figsize to make the plot narrower and less high
    plt.plot(years, token_counts, marker='o')
    plt.title('Total Number of Tokens from 1946 to 2022')
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
base_path = r'C:\Users\juliu\Desktop\DesinformationTermPaper\static\Converted sessions'  # Path to the base folder containing session folders
output_path = r'C:\Users\juliu\Desktop\DesinformationTermPaper\static\SVGs\number_of_tokens_1946_2022.svg'  # Path to save the SVG file
years, token_counts = process_all_sessions(base_path)
plot_token_counts(years, token_counts, output_path)
