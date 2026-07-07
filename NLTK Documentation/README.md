## NLTK : A Guide to Natural Language Processing

NLTK is a Natural Laguage Processing toolkit for building Python programs in order to work with human language data. It provides various text processing libraries as well as lexical resources such as WordNet with a lot of test datasets. NLTK can be used for performing NLP tasks such as classification, tokenization, stemming, tagging, parsing, semantic reasoning and more.

### Installing NLTK

To install NLTK in our local system, we use the pip installation technique.

```
pip install nltk
```

### NLP Techniques using NLTK

- **Tokenization** : the process of breaking down of text into smaller units called tokens. It helps to build a vocabulary such that we can represent all words and numbers present in a sentence uniquely in a list.

- **Lower case conversion** : Conversion of all the tokens into lowercase helps to avoid redundancy in the token list.

- **Stop Words removal** : With NLTK we can see all the stop words available in the English language. Removal of these stopwords facilitates cleaner processing inside the model.

- **Stemming** : Stemming is the process of extracting the root word and removing the rest so that they have the same meaning. For eg: processing and process.

- **Lemmatization** : Lemmatization is the process of extracting the base form of the word known as Lemma, available in the dictionary.NLTK provides us with the WordNet Lemmatizer that makes use of the WordNet Database to lookup lemmas of words.

- **Parse tree or Syntax Tree generation** : For generation of parse tree, we can define grammar and then use NLTK RegexpParser to extract all parts of speech from the sentence.

- **POS Tagging** : Part of Speech tagging is used in text processing to avoid confusion between two same words that have different meanings.NLTK provides us with `word_tokenize` and `pos_tag` to implement POS Tagging.

- **Chunking** : Chunking allows us to identify phrases using chunk grammar and Regular Expressions.

- **Chinking** : Chinking is used together with chunking, but while chunking is used to include a pattern, chinking is used to exclude a pattern.

- **NER** : Named entities are noun phrases that refer to specific locations, people, organizations, and so on.Named Entity Recognition helps to find the named entities in your texts and also determine what kind of named entity they are.

To see a demo of these text-processing tasks implemented with the help of NLTK, refer [here](./NLTK.ipynb)

### Advantages of NLTK

- NLTK provides hands-on guide introducing programming fundamentals alongside topics in computational linguistics, with a comprehensive API documentation.
- NLTK is free and open-source, available for Windows, Mac OS X, and Linux.
- NLTK is an amazing library to play with natural language.
- NLTK guides through the fundamentals of writing Python programs, working with corpora, categorizing text, analyzing linguistic structure, and more.

## References

Different text-processing techniques discussed here have been referred from [this](https://www.nltk.org/book_1ed.) online version of the book.

#### CONTRIBUTED BY

[Shreya Ghosh](https://github.com/shreya024)
