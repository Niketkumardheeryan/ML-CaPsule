# Song-Genre-Classifier
# ABOUT 
<br>

1) This project aims to identify which genre a song belongs to on the basis of its lyrics
2) The dataset contains 62155 songs
3) Each song is classified into 5 genres- Country, Rock, Hip-Hop, Pop and Rhythm and Blues
4) Two major text classification method were tested- Logistic Regression and Naïve Bayes
5) Under Naïve Bayes, 3 models were tested- Count Vectorizer, TF-IDF, and Text Cleaning
6) Upon testing, Multinomial Naïve Bayes with Text Cleaning was found to give the highest accuracy
7) Further analysis was also done to find top songs and generate WordClouds

# WHY WE BUILT IT
<br>

1) For music enthusiasts to have some fun by giving desired lyrics as an input to the classifier and getting the closest matching genre as output
2) To find out if there is any direct correlation between lyrics and genres of songs
3) To organize songs on the basis of their genre, for example top hip-hop songs, most hip-hop like rock songs, hip-hop like country songs, hip -hop like RnB songs, hip-hop like    pop songs; similarly for rock, country and RnB
4) To create WordClouds, a technique to find words are the most frequent in the given dataset, and to find  the most common lyrics used in a particular genre

# ADVANTAGES
<br>

1) Works on bulk data
2) Consistent and meaningful results
3) Improved accuracy of the models
4) Top songs in each genre apart from genre classification
5) Confusion matrix: gives the basic idea of distribution of genres in the given dataset
6) Basic building block for more sophisticated music genre predication systems
7) Applications include music retrieval and recommendation

# CODE
<br>

The code can be found <a href="https://github.com/TANYA-CHAN/SongGenreClassifiernlp/blob/master/SongGenreClassifier.ipynb">here</a>

# Accuracy Obtained
 Count Vectorizer = 75%
 TF-IDF = 74%
 Text Cleaning = 83%

# Dataset Used
dataset can be found here

<a href="https://drive.google.com/file/d/1FD2o5QAmW143gtrfwgZHBbv4RI3klNHI/view?usp=sharing">lyrics.csv</a>

# Libraries Used
Pandas
Sklearn
Nltk
Seaborn