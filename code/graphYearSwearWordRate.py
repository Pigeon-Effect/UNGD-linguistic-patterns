import os
import glob
import re
import nltk
import matplotlib.pyplot as plt
import numpy as np

# Ensure you have NLTK's punkt tokenizer data
nltk.download('punkt')


def calculate_swear_word_rate(text):
    """Calculate the rate of swear words in the text."""
    '''
    swear_words = {
        "damn", "arse", "arsehole", "ass", "hell", "shit", "fuck", "crap", "bastard", "bitch",
        "asshole", "douche", "slut", "whore", "dick", "piss", "cunt", "ass hole", "asshole", "bloody", "hell",
        "prick", "motherfucker", "fucker", "cock", "bollocks", "bugger", "fuck", "cock", "nigga", "pussy",
        "wanker", "bloody", "arse", "git", "tosser", "twat", "shite", "slut", "son of a whore", "fucker",
        "damned", "fucking", "freaking", "frigging", "effing", "god damn", "twat", "wanker",
        "shitty", "bitchy", "dickhead", "pissed", "pissing",
        "cocksucker", "dumbass", "jackass", "butthead",
        "son of a bitch", "son of a gun", "crappy", "asshat",
        "asswipe", "shithead", "shitface", "fuckface", "fuckhead",
        "dipshit", "dumbshit", "bullshit", "horseshit",
        "bastarding", "dicking", "pricking", "screwing",
        "bastardize", "bastardized", "fucked", "fucked up",
        "screwed", "screwed up", "dickwad", "cuntface",
        "dickweed", "dickless", "dicking around", "prickish"
    }
    '''
    # crisis words
    '''
    swear_words = {
        "war", "crisis", "conflict", "battle", "struggle", "fight", "dispute",
        "emergency", "catastrophe", "calamity", "chaos", "disaster", "tumult",
        "turbulence", "tragedy", "fiasco", "pandemic", "epidemic", "contagion",
        "upheaval", "revolt", "revolution", "uprising", "insurrection", "rebellion",
        "siege", "raid", "assault", "skirmish", "clash", "combat", "quarrel",
        "feud", "confrontation", "collision", "turmoil", "disruption", "breakdown",
        "collapse", "implosion", "chaotic", "hostility", "aggression", "violence",
        "bloodshed", "havoc", "destruction", "annihilation", "ruin", "devastation",
        "suffering", "hardship", "adversity", "trouble", "dilemma", "predicament",
        "peril", "danger", "jeopardy", "threat", "risk", "hazard", "menace",
        "distress", "panic", "alarm", "urgency", "alert", "plight", "emergency",
        "displacement", "refugee", "exodus", "massacre", "genocide", "atrocity",
        "terrorism", "siege", "assassination", "homicide", "murder", "extremism",
        "hostage", "detention", "subversion", "insurgency", "guerrilla", "coup",
        "oppression", "tyranny", "dictatorship", "famine", "drought", "earthquake",
        "flood", "hurricane", "tsunami", "wildfire", "eruption", "landslide"
    }
    '''
    # degree adverbs
    '''
    swear_words = {
        "actually", "AFAIAA", "AFAIK", "all else being equal", "all in all",
        "allegedly", "all things considered", "apparently", "arguably", "as a matter of fact",
        "assuredly", "at bottom", "at first blush", "at first glance", "at first sight",
        "believably", "certainly", "clearly", "conceivably", "conditionally",
        "credibly", "debatably", "defendably", "defensibly", "definitely",
        "doubtless", "doubtlessly", "essentially", "evidently", "evitably",
        "fortunately", "hypothetically", "impossibly", "in essence", "in fact",
        "in point of fact", "incontestably", "indeed", "indisputably", "indubitably",
        "ineluctably", "inescapably", "inevitably", "IPOF", "likely",
        "literally", "loosely", "manifestly", "maybe", "more and more",
        "necessarily", "needlessly", "noticeably", "observably", "obviously",
        "ostensibly", "ostensively", "patently", "perhaps", "plainly",
        "plausibly", "positively", "possibly", "presumably", "presumptively",
        "probably", "purportedly", "putatively", "questionlessly", "really",
        "reportedly", "reputedly", "rumoredly", "rumouredly", "scarcely",
        "seemingly", "statistically", "strictly", "sure", "surely",
        "technically", "totally", "transparently", "truly", "unarguably",
        "unavoidably", "undeniably", "undoubtably", "undoubtedly", "unfortunately",
        "unnecessarily", "unquestionably", "verifiably", "without a doubt", "without doubt",
        "arguably", "evidently", "apparently", "seemingly", "purportedly",
        "ostensibly", "reportedly", "supposedly", "presumably", "allegedly",
        "likely", "possibly", "potentially", "conceivably", "theoretically",
        "categorically", "indisputably", "incontestably", "unquestionably",
        "plainly", "distinctly", "manifestly", "patently", "self-evidently",
        "axiomatically", "indubitably", "undoubtedly"
    }
    '''
    #degree adverbs
    '''
    swear_words = {
    "100 percent", "110 proof", "a bit", "a good deal", "a lot", "a tad",
    "abnormally", "aboundingly", "about", "absolutely", "absurdly",
    "abundantly", "acceptably", "accursedly", "ad infinitum", "ad nauseam",
    "adequately", "admirably", "alarmingly", "all", "all-fired",
    "almost", "altogether", "amazingly", "anything but", "approaching",
    "as", "astronomically", "at all", "awfully", "bally",
    "barely", "blasted", "bleeding", "bleeping", "blimming",
    "blindingly", "bloody", "blooming", "boiling", "breathtakingly",
    "clearly", "completely", "confederally", "considerably", "crazy",
    "cussed", "damn", "damned", "darn", "darned",
    "dead", "deservedly", "deuced", "deucedly", "doosed",
    "downright", "dreadfully", "durn", "easily", "effing",
    "embarrassingly", "enormously", "entirely", "epically", "equally",
    "even", "ever so", "everloving", "exceedingly", "excessively",
    "extensively", "extra", "extremely", "fairly", "fantastically",
    "far", "flipping", "freaking", "fricking", "frigging",
    "fucking", "fully", "goldurn", "good and", "greatly",
    "hardly", "hella", "herostratically", "hideously", "highly",
    "honkin'", "honkingly", "horribly", "how", "however",
    "hugely", "immensely", "impossibly", "incredibly", "indeed",
    "infinitely", "intensely", "jolly", "just", "largely",
    "least", "less", "literally", "little", "lovely and",
    "mad", "majorly", "mammothly", "mighty", "moderately",
    "more", "more and more", "most", "motherfreaking", "motherfucking",
    "much", "nearly", "needlessly", "nice and", "normally",
    "not", "not at all", "noticeably", "observably", "outright",
    "particularly", "partly", "peculiarly", "perfectly", "plain",
    "pleasantly", "plum", "positively", "practically", "precious",
    "pretty", "profoundly", "purely", "quite", "rather",
    "real", "really", "reasonably", "relatively", "remarkably",
    "scarcely", "shockingly", "simply", "slightly", "so",
    "sofa king", "something", "somewhat", "spanking", "staggeringly",
    "still", "stone", "strikingly", "strongly", "sufficiently",
    "supremely", "suspiciously", "terminally", "terribly", "that",
    "though", "to death", "too", "totally", "transfinitely",
    "transitorily", "tremendously", "truly", "uberly", "unbelievably",
    "unimaginably", "unnecessarily", "unrelatedly", "utterly", "very",
    "virtually", "way", "well", "whole hog", "whoopingly",
    "wicked", "wonderfully", "yet", "zoomorphically"
}
'''

# negation

    swear_words = {
    "no", "none", "not", "nothing", "nobody", "nowhere", "neither",
    "nor", "never",
    }


    # Tokenize the text into words
    words = nltk.word_tokenize(text.lower())
    total_words = len(words)
    swear_word_count = sum(1 for word in words if word in swear_words)

    # Calculate the rate of swear words
    if total_words == 0:
        return 0
    return swear_word_count / total_words


def process_folder_by_session(folder_path):
    """Process each session folder, calculate average swear word rate per year."""
    swear_word_rates = []
    years = []

    session_folders = glob.glob(os.path.join(folder_path, "Session*"))

    for session_folder in session_folders:
        # Extract year from folder name
        match = re.search(r'Session\s\d{2}\s-\s(\d{4})$', session_folder)
        if match:
            year = int(match.group(1))

            # use this when 1948 and 1949 are not part of calculus

            if year in [1948, 1949]:
                continue  # Skip years 1948 and 1949
            year_swear_word_rates = []
            print(f"Processing year: {year}")

            # Process each txt file in the session folder
            txt_files = glob.glob(os.path.join(session_folder, "*.txt"))
            for txt_file in txt_files:
                with open(txt_file, 'r', encoding='utf-8') as file:
                    content = file.read()
                    swear_word_rate = calculate_swear_word_rate(content)
                    year_swear_word_rates.append(swear_word_rate)

            # Calculate the average swear word rate for the year
            if year_swear_word_rates:
                avg_swear_word_rate = sum(year_swear_word_rates) / len(year_swear_word_rates)
                swear_word_rates.append(avg_swear_word_rate)
                years.append(year)
            else:
                print(f"No valid text files found for year: {year}")

    if not years:
        print("No data found. Please check the folder path and structure.")
    return years, swear_word_rates


def plot_swear_word_rate_timeline(years, swear_word_rates, output_path):
    if not years or not swear_word_rates:
        print("No data to plot.")
        return

    fig, ax = plt.subplots(figsize=(10, 3))
    ax.plot(years, swear_word_rates, marker='o', label='Swear Word Rate')

    # Polynomial regression (e.g., a degree 3 polynomial)
    polynomial_degree = 5
    coefficients = np.polyfit(years, swear_word_rates, polynomial_degree)
    polynomial = np.poly1d(coefficients)

    # Generate x values for plotting the polynomial regression curve
    x_values = np.linspace(min(years)+4, max(years), 500)
    y_values = polynomial(x_values)

    # Plot the polynomial regression curve
    ax.plot(x_values, y_values, color='red')

    # Set title with padding
    ax.set_title('G5 - Negation Rate from 1946 to 2022', pad=20)

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
output_path = r'C:\Users\juliu\Desktop\DesinformationTermPaper\static\SVGs\g5_negation_rate_1946_2022.svg'  # Path to save the SVG file
years, swear_word_rates = process_folder_by_session(folder_path)
plot_swear_word_rate_timeline(years, swear_word_rates, output_path)
