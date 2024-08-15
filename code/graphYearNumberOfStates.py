import os
import re
import matplotlib.pyplot as plt


def count_txt_files_in_session(session_path):
    """Count the number of .txt files in a given session folder."""
    txt_files = [f for f in os.listdir(session_path) if f.endswith('.txt')]
    return len(txt_files)


def process_all_sessions(base_path):
    """Process all session folders to count the number of .txt files for each year."""
    years = []
    state_counts = []

    for session_folder in sorted(os.listdir(base_path)):
        match = re.match(r'Session (\d{2}) - (\d{4})', session_folder)
        if match:
            session_number = int(match.group(1))
            year = int(match.group(2))
            session_path = os.path.join(base_path, session_folder)

            if os.path.isdir(session_path):
                num_states = count_txt_files_in_session(session_path)
                years.append(year)
                state_counts.append(num_states)

    return years, state_counts


def plot_state_counts(years, state_counts, output_path):
    plt.figure(figsize=(10, 3))  # Adjust figsize to make the plot narrower and less high
    plt.plot(years, state_counts, marker='o')
    plt.title('Number of Speeches from 1946 to 2022')
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
output_path = r'C:\Users\juliu\Desktop\DesinformationTermPaper\static\SVGs\number_of_speeches_1946_2022.svg'  # Path to save the SVG file
years, state_counts = process_all_sessions(base_path)
plot_state_counts(years, state_counts, output_path)
