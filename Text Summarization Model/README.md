# Text Summarization Using TextRank Algorithm

## Overview:
This Python script provides a text summarization algorithm based on the TextRank algorithm. It automatically generates summaries for input text by identifying important sentences using graph-based ranking techniques.

## Dependencies:
Ensure you have the following dependencies installed:
- NLTK (Natural Language Toolkit)
- NumPy
- NetworkX

You can install NLTK and NumPy using pip:

'''
$ pip install nltk numpy networkx
$ pip install nltk
$ pip install numpy
$ pip install networkx
'''

## Usage:
1. Clone the repository to your local machine.
2. Install the required dependencies using the provided command.
3. Use the `generate_summary` function in the `text_summarization.py` file to generate summaries for your text data.

## How It Works:
1. **Text Preprocessing:**
   - The input text is tokenized into sentences using NLTK's `sent_tokenize` function.
   - Stop words and punctuation are removed from each sentence.

2. **Sentence Similarity:**
   - Cosine similarity is computed between each pair of sentences based on the occurrence of words after preprocessing.
   - A similarity matrix is constructed to represent the similarity between sentences.

3. **Graph Representation:**
   - The similarity matrix is converted into a graph representation, where each node represents a sentence and edges represent the similarity between sentences.

4. **Ranking:**
   - The PageRank algorithm, implemented using NetworkX, is applied to the sentence similarity graph to assign importance scores to each sentence.
   - Sentences are ranked based on their importance scores.

5. **Summary Generation:**
   - Sentences with importance scores above a specified threshold are selected to form the summary.
   - The selected sentences are concatenated to generate the final summary.

## Example:
```python
text = "Dave watched as the forest burned up on the hill, only a few miles from her house. The car had been hastily packed and Marta was inside trying to round up the last of the pets. Dave went through his mental list of the most important papers and documents that they couldn't leave behind. He scolded himself for not having prepared these better in advance and hoped that he had remembered everything that was needed. He continued to wait for Marta to appear with the pets, but she still was nowhere to be seen.
"
summary = generate_summary(text)
print(summary)

Contributing:
    Contributions are welcome! Feel free to submit bug reports, feature requests, or pull requests.


This project is licensed under the MIT License. See the LICENSE file for details.

Feel free to customize this README file according to your preferences and requirements!
