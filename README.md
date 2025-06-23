Here is a **copy-paste ready** `README.md` for your GitHub repository. It follows scientific conventions, includes structured headings, and integrates your result images at the end.

---

# **UNGA Linguistic Patterns (1946–2022)**

This repository contains the code, data, and results for analyzing linguistic trends in speeches made at the United Nations General Assembly (UNGA) from 1946 to 2022. The study focuses on linguistic markers that may reflect changing geopolitical, cultural, and rhetorical patterns in global diplomacy.

---

## **Overview**

This project uses the UN General Debate Corpus to extract time-series features from political speeches, capturing how countries express themselves over time. It quantifies linguistic changes across multiple dimensions including:

* Self-reference
* Direct audience address
* Modal and degree adverbs
* Negation
* Sentiment
* Readability
* Vocabulary richness
* Use of numbers and swear words

All results are plotted as normalized time series to highlight long-term developments in rhetorical style and content.

---

## **Data Source**

The speeches were extracted from the [UN General Debate Corpus](https://doi.org/10.7910/DVN/0TJX8Y), a large, annotated collection of all country statements delivered at the UN General Debate since 1970. For years before 1970, archival documents were processed with OCR and matched manually where necessary.

---

## **Methodology**

We applied a pipeline of linguistic preprocessing and feature extraction, including:

* Tokenization and lemmatization
* Part-of-speech tagging
* Readability and sentiment analysis
* Calculation of stylistic features (e.g., average sentence length)
* Use of wordlists for topic-specific content (e.g., crisis vocabulary)

Time series were smoothed using moving averages and normalized by total word count.

---

## **Key Features Analyzed**

| Feature                           | Description                                                           |
| --------------------------------- | --------------------------------------------------------------------- |
| **Self-Reference Rate**           | Frequency of first-person singular/plural pronouns (e.g., “I”, “we”)  |
| **Direct Addressee Rate**         | Use of second-person pronouns or phrases directed at the audience     |
| **Modal Adverb Rate**             | Words indicating possibility or obligation (e.g., “probably”, “must”) |
| **Degree Adverb Rate**            | Words modifying intensity (e.g., “very”, “extremely”)                 |
| **Negation Rate**                 | Occurrence of negations (e.g., “not”, “no”)                           |
| **Average Sentence Length**       | Mean number of words per sentence                                     |
| **Moving Type-Token Ratio (TTR)** | Proxy for lexical diversity over moving windows                       |
| **Flesch-Kincaid Score**          | A readability index estimating required education level               |
| **Sentiment Polarity**            | Scale from negative (−1) to positive (+1) sentiment                   |
| **Sentiment Subjectivity**        | Degree of subjectivity in statements                                  |
| **Swear Word Rate**               | Use of profanities (rare, but relevant in crises)                     |
| **Crisis Word Rate**              | Frequency of terms linked to conflict, disaster, urgency              |
| **Number Rate**                   | Use of numerical expressions or statistics                            |

---

## **Results**

### **Stylistic and Semantic Trends (1946–2022)**

![Self Reference Rate](https://raw.githubusercontent.com/Pigeon-Effect/UNGD-linguistic-patterns/refs/heads/main/results/time%20series%20analysis/g1_self_reference_rate_1946_2022.svg)
![Direct Addressee Rate](https://raw.githubusercontent.com/Pigeon-Effect/UNGD-linguistic-patterns/refs/heads/main/results/time%20series%20analysis/g2_direct_addresse_rate_1946_2022.svg)
![Modal Adverb Rate](https://raw.githubusercontent.com/Pigeon-Effect/UNGD-linguistic-patterns/refs/heads/main/results/time%20series%20analysis/g3_modal_adverb_rate_1946_2022.svg)
![Degree Adverb Rate](https://raw.githubusercontent.com/Pigeon-Effect/UNGD-linguistic-patterns/refs/heads/main/results/time%20series%20analysis/g4_degree_adverb_rate_1946_2022.svg)
![Negation Rate](https://raw.githubusercontent.com/Pigeon-Effect/UNGD-linguistic-patterns/refs/heads/main/results/time%20series%20analysis/g5_negation_rate_1946_2022.svg)

---

### **Readability, Sentiment & Lexical Diversity**

![Average Sentence Length](https://raw.githubusercontent.com/Pigeon-Effect/UNGD-linguistic-patterns/refs/heads/main/results/time%20series%20analysis/s1_average_sentence_length_1946_2022.svg)
![Average Moving TTR](https://raw.githubusercontent.com/Pigeon-Effect/UNGD-linguistic-patterns/refs/heads/main/results/time%20series%20analysis/s2_average_moving_ttr_1946_2022.svg)
![Flesch Kincaid Readability](https://raw.githubusercontent.com/Pigeon-Effect/UNGD-linguistic-patterns/refs/heads/main/results/time%20series%20analysis/s3_flesch_kincaid_readability_1946_2022.svg)
![Sentiment Polarity](https://raw.githubusercontent.com/Pigeon-Effect/UNGD-linguistic-patterns/refs/heads/main/results/time%20series%20analysis/s4_sentiment_polarity_1946_2022.svg)
![Sentiment Subjectivity](https://raw.githubusercontent.com/Pigeon-Effect/UNGD-linguistic-patterns/refs/heads/main/results/time%20series%20analysis/s5_sentiment_subjectivity_1946_2022.svg)

---

### **Topical Trends and Rhetorical Intensity**

![Swear Word Rate](https://raw.githubusercontent.com/Pigeon-Effect/UNGD-linguistic-patterns/refs/heads/main/results/time%20series%20analysis/t1_swear_word_rate_1946_2022.svg)
![Crisis Word Rate](https://raw.githubusercontent.com/Pigeon-Effect/UNGD-linguistic-patterns/refs/heads/main/results/time%20series%20analysis/t2_crisis_word_rate_1946_2022.svg)
![Number Rate](https://raw.githubusercontent.com/Pigeon-Effect/UNGD-linguistic-patterns/refs/heads/main/results/time%20series%20analysis/t3_number_rate_1946_2022.svg)

---

## **Repository Structure**

```bash
├── data/                    # Preprocessed speech transcripts
├── notebooks/              # Jupyter notebooks for analysis
├── results/                # Time series plots and exported figures
├── src/                    # Scripts for preprocessing and feature extraction
├── requirements.txt        # Python dependencies
└── README.md               # This file
```

---

## **How to Cite**

If you use this repository or the results, please cite:

**Julius Pfundstein & Jonas Krenzer**,
*Mapping International Alliances: A Study of UNGA Voting Behavior*,
Leipzig University, 2024.

---

## **License**

This project is licensed under the MIT License. See the `LICENSE` file for more details.
