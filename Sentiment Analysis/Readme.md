<h1> Sentiment Analysis </h1>

Dataset used to do the Analysis is https://www.kaggle.com/datasets/bababullseye/depression-analysis.

The Python Notebook added splits the entire Dataset into 95% Training and 5% Test Data.

**WordCloud** is used to do a preliminary simple Analysis.

Two Methods are used to Classify the Data.

<h2>TF-IDF</h2>
It stands for Term Frequency — Inverse Document Frequency”. This is a technique to quantify words in a set of documents. We generally compute a score for each word to signify its importance in the document. It is mainly used in Text Mining Techniques.

<h2>Bag of Words (BoW) </h2>
It is called a “bag” of words, because any information about the order or structure of words in the document is discarded. The model is only concerned with whether known words occur in the document, not where in the document.  <br/>  <br/> 

Unlike, bag-of-words, tf-idf creates a normalized count where each word count is divided by the number of documents this word appears in. It makes it a better model than BoW. 
