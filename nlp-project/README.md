<h1 align="center"> NLP Project </h1> <br>

<p align="center">
  <a href="https://github.com/Apoorva57/NLP-Project">
    <img alt="NLP" title="NLP" src="https://user-images.githubusercontent.com/97695341/195971438-b44982d0-0663-47c6-bda6-ed4d7f9a0431.gif" width="450">
  </a>
</p>
Video of code run: https://drive.google.com/file/d/1hjh0WyZ0e2CJ83K_lmVXIFlMNWvFuNTs/view?usp=sharing

## NLP
Natural Language Processing (NLP) enables machine learning algorithms to organize and understand human language. NLP enables machines to not only gather text and speech but also identify the core meaning it should respond to.

## Tokenization
Tokenization is one of the many pieces of the puzzle in how NLP works. Tokenization is a simple process that takes raw data and converts it into a useful data string. While tokenization is well known for its use in cybersecurity and the creation of NFTs, tokenization is also an important part of the NLP process. Tokenization is used in natural language processing to split paragraphs and sentences into smaller units that can be more easily assigned meaning. The first step of the NLP process is gathering the data (a sentence) and breaking it into understandable parts (words). Here’s an example of a string of data:
<br><br>“What restaurants are nearby?”  <br><br>
For this sentence to be understood by a machine, tokenization is performed on the string to break it into individual parts. With tokenization, we’d get something like this:
<br><br>‘what’ ‘restaurants’ ‘are’ ‘nearby’ <br><br>
This may seem simple, but breaking a sentence into its parts allows a machine to understand the parts as well as the whole. This will help the program understand each of the words by themselves, as well as how they function in the larger text.
<br>
* Tokenizing by word: Words are like the atoms of natural language. They’re the smallest unit of meaning that still makes sense on its own. Tokenizing your text by word allows you to identify words that come up particularly often.<br>
* Tokenizing by sentence: When you tokenize by sentence, you can analyze how those words relate to one another and see more context.
<p/>

## Stop words
A stop word is a commonly used word (such as “the”, “a”, “an”, “in”) that a search engine has been programmed to ignore, both when indexing entries for searching and when retrieving them as the result of a search query. 
We would not want these words to take up space in our database, or taking up valuable processing time. For this, we can remove them easily, by storing a list of words that you consider to stop words. NLTK(Natural Language Toolkit) in python has a list of stopwords stored in 16 different languages.
Here's an example of sentence with stop words:<br><br>
"Can listening be exhausting?"<br><br>
Without stop words, the sentence will have just these tokens:<br><br>
Listening, exhausting

## Stemming
Stemming is the process of producing morphological variants of a root/base word. Stemming programs are commonly referred to as stemming algorithms or stemmers. Stemming is an important part of the pipelining process in Natural language processing. The input to the stemmer is tokenized words. A stemming algorithm reduces the words “chocolates”, “chocolatey”, “choco” to the root word, “chocolate” and “retrieval”, “retrieved”, “retrieves” reduce to the stem “retrieve”.

## POS Tagging
Part-of-Speech (PoS) tagging may be defined as the process of assigning one of the parts of speech to the given word. It is generally called POS tagging. In simple words, we can say that POS tagging is a task of labelling each word in a sentence with its appropriate part of speech. We already know that parts of speech include nouns, verb, adverbs, adjectives, pronouns, conjunction and their sub-categories. Here is an example for POS Tagging: <br><br>
"I am going to school"
<br><br>Upon using POS tagiing we get the following result for the given sentence:<br><br>
('I', 'PRP'), ('am', 'VBP'), ('going', 'VBG'), ('to', 'TO'), ('school', 'NN')

## Lemmatizing
Lemmatization is the process of grouping together the different inflected forms of a word so they can be analyzed as a single item. Lemmatization is similar to stemming but it brings context to the words. So it links words with similar meanings to one word. Examples of lemmatization:<br><br>
rocks : rock<br>
corpora : corpus

## Data/Packages used
We have used the package -
<br>NLTK: It is a leading platform for building Python programs to work with human language data. It provides easy-to-use interfaces to over 50 corpora and lexical resources such as WordNet, along with a suite of text processing libraries for classification, tokenization, stemming, tagging, parsing, and semantic reasoning, wrappers for industrial-strength NLP libraries.<br>
Natural Language Processing with Python provides a practical introduction to programming for language processing. Written by the creators of NLTK, it guides the reader through the fundamentals of writing Python programs, working with corpora, categorizing text, analyzing linguistic structure, and more.
<br><br>Natural Language Toolkit for Indic Languages (iNLTK): This package helps by providing out-of-the-box support for various NLP tasks that an application developer might need.
It supports a wide variety of languages:
Language | Hindi | Punjabi | Gujarati | Kannada | Malayalam | Oriya | Marathi | Bengali | Tamil | Urdu | Nepali | Sanskrit | English | Telugu
--- | --- | --- | --- |--- |--- |--- |--- |--- |--- |--- |--- |--- |--- |---
Code | hi | pa | gu | kn | ml | or | mr | bn | ta | ur | ne | sa | en | te

https://github.com/goru001/inltk
<br><br>We have used the dataset called as “HindiEnglish Corpora” provided by Aiswaryaramachandran.
The dataset comprises Hindi English Truncated Corpus that is, it contains a huge list of sentences translated from English to Hindi, thus providing us with enough data to work on.
<br>https://www.kaggle.com/datasets/aiswaryaramachandran/hindienglish-corpora

## Code
https://colab.research.google.com/drive/1ER82yTQX0r-qlUep55n5xa35OU2KJwtW?usp=sharing

## Code Explanation
To upload the file from the local drive we write the following code in the cell and run it
<br>
Importing nltk and punkt package by using the download(‘punkt’) function in the nltk library. The punkt package is an important part of the tokenization process.The NLTK corpus and module downloader is called by nltk.download. This module defines several interfaces which can be used to download corpora, models, and other data packages that can be used with NLTK. Further, I have imported sentence and word tokenizer from nltk.tokenize module.
```
import nltk
nltk.download('punkt')
nltk.download
from nltk.tokenize import sent_tokenize, word_tokenize
```
I have provided a quote of Steve Jobs as a sentence to the machine for tokenizing.
```
Steve_Jobs="Your time is limited, so don’t waste it living someone else’s life. Don’t be trapped by dogma – which is living with the results of other people’s thinking."
```
Now, we call the sentence tokenizer function to get sentence as tokens and word tokenizer funtion to get words as tokens of the given quote.
```
sent_tokenize(Steve_Jobs)
```
```
word_tokenize(Steve_Jobs)
```
For removal of stop words, we download the stopwords module from nltk package and import the stopwords from the NLTK corpus.
```
nltk.download("stopwords")
```
```
from nltk.corpus import stopwords
```
I have provide a quote of Will Smith as a sentence to the machine for tokenizing and further to removing stop words from it.
```
Will_Smith="Money and success don’t change people; they merely amplify what is already there."
```
The code below will tokenize the given quote and displays the words as tokens.
```
words_in_quote = word_tokenize(Will_Smith)
```
```
words_in_quote
```
Next, we need to set the stop words to english language stop words.
```
stop_words = set(stopwords.words("english"))
```
Lastly, we generate a filtered list. The filtered list will display us only the tokens in the quote that are not stop words.
```
filtered_list = [
    word for word in words_in_quote if word.casefold() not in stop_words
    ]
```
```
filtered_list
```
For stemming, we import the PorterStemmer from stem module of NLTK and set stemmer as PorterStemmer function
```
from nltk.stem import PorterStemmer
```
```
stemmer = PorterStemmer()
```
I have provide a string to machine for stemming, firstly we generate tokens of the given sentence by calling the word tokenizer function.
```
string_for_stemming = """The crew of the USS Discovery discovered many discoveries. Discovering is what explorers do."""
```
```
words = word_tokenize(string_for_stemming)
```
```
words
```
Further, we call upon stemmer function to produce the stemmed words for word in tokenized words.
```
stemmed_words = [stemmer.stem(word) for word in words]
```
```
stemmed_words
```
Next, I have implemented is POS Tagging and for that I have provide a quote of Oprah Winfrey as input and tokenized it to get the word tokens from the sentence.
```
Oprah_Winfrey = """The biggest adventure you can take is to live the life of your dreams."""
```
```
words_in_quote = word_tokenize(Oprah_Winfrey)
```
```
words_in_quote
```
We download the POS Tagger by downloading it from the nltk package.
```
import nltk
nltk.download('averaged_perceptron_tagger')
```
Then, we call upon the pos tag function on the tokenized words to generate the POS Tags of the given sentence.
```
nltk.pos_tag(words_in_quote)
```
In order to lemmatize, you need to create an instance of the WordNetLemmatizer() and call the lemmatize() function on a single word. Therefore, I have imported WordNetLemmatizer from stem module of nltk as well as downloaded Open Multilingual Wordnet. They both serve the same purpose.
```
from nltk.stem import WordNetLemmatizer
nltk.download('omw-1.4')
```
```
lemmatizer = WordNetLemmatizer()
```
Next, we download the package wordnet and then get the lemmatizers for a few user input words to check the functioning of lemmatizer.
```
nltk.download('wordnet')
```
```
print("runners :", lemmatizer.lemmatize("runners"))
print("items :", lemmatizer.lemmatize("items"))
```
Further, I have also provide a string for lemmatizing and tokenized it first, to generate tokens of the given string.
```
string_for_lemmatizing = "The world needs dreamers and the world needs doers. But above all, the world needs dreamers who do."
```
```
words = word_tokenize(string_for_lemmatizing)
```
```
words
```
Next, the lemmatizer function is called upon the words generated by tokenizers and output generated is a list of lemmatized words as output.
```
lemmatized_words = [lemmatizer.lemmatize(word) for word in words]
```
```
lemmatized_words
```
For implementing Hindi POS tagger, we need to first import the indian corpus and tnt from tag module of nltk.
```
from nltk.corpus import indian
from nltk.tag import tnt
import string
```
After downloading the indian pachage we set the tags set as hindi POS.The function given below tell us about the total number of sentences as data and also the no of sentences to be trained and tested against.
```
nltk.download('indian')
```
```
tagged_set = 'hindi.pos'
word_set = indian.sents(tagged_set)
count = 0
for sen in word_set:
    count = count + 1
    sen = "".join([" "+i if not i.startswith("'") and i not in string.punctuation else i for i in sen]).strip()
    print (count, sen)
print ('Total sentences in the tagged file are',count)

train_perc = .9

train_rows = int(train_perc*count)
test_rows = train_rows + 1

print ('Sentences to be trained',train_rows, 'Sentences to be tested against',test_rows)
```
We set the data as indian tagged sentence which we got from the previous code and then call upon the pos tagger function on the data so that whenever a sentence from the given data is chosen we will get displayed the pos tags if the pos tagger function is called upon the same.
```
data = indian.tagged_sents(tagged_set)
train_data = data[:train_rows]
test_data = data[test_rows:]


pos_tagger = tnt.TnT()
pos_tagger.train(train_data)
pos_tagger.evaluate(test_data)
```
For example I have taken a sentence from the data and have first tokenized the sentence then further called the pos tagger function upon generated tokens. The output will display the POS tags of the given sentence.
```
sentence_to_be_tagged = "प्रधानमंत्री ने कहा कि उन्हें उम्मीद है कि पड़ोसी देश पाकिस्तान, भारत विरोधी दुष्प्रचार रोक कर सीमा पार आतंकवाद को रोकने में सहयोग करेगा ।"

tokenized = nltk.word_tokenize(sentence_to_be_tagged)


hindi_pos = pos_tagger.tag(tokenized)
```
```
hindi_pos
```
Next, I have implemented the Tokenizer for Hindi language
```
from google.colab import files
uploaded = files.upload()
```
We click on the “choose files” option, then select and download the CSV data set file (which we downloaded from Kaggle known as 'Hindi_English_Truncated_Corpus.csv') from our local drive.  Later we write the following code snippet to import it into a pandas data frame.
```
import pandas as pd
import io

df = pd.read_csv(io.BytesIO(uploaded['Hindi_English_Truncated_Corpus.csv']))
```
The head() function is used to get the first n rows. This function returns the first n rows for the object based on position. It is useful for quickly testing if your object has the right type of data in it.
```
df.head()
```
Next, we install the torch. PyTorch is a Python package that provides two high-level features:
* Tensor computation (like NumPy) with strong GPU acceleration
* Deep neural networks built on a tape-based autograd system 
<p />

```
pip install torch==1.12.1+cpu -f https://download.pytorch.org/whl/torch_stable.html
```
iNLTK runs on CPU, as is the desired behaviour for most of the Deep Learning models in production. The command above will install PyTorch for CPU, which, as the name suggests, does not have Cuda support.
<br>The iNLTK is installed once all its requirements are satisfied with python libraries and packages by the following code:
```
pip install inltk
```
The torch-1.12.1-cp37-cp37m-manylinux1_x86_64.whl version gets downloaded. Once the download has been successfully completed we set up the language we want to use the tokenizer for:
```
from inltk.inltk import setup
setup('hi')
```
We used ‘hi’ since we will be using the language Hindi for the tokenizer.
<br>Note: ignore the runtime error as it is probably caused by the difference in the torch version of the package used and the latest one we are using. At the end of the output, we can see the code does run without error and provides output as “Done!”.
<br>We import the tokenizer using the following command from the iNLTK package:
```
from inltk.inltk import tokenize
```
Since we have already provided data set for the program. Therefore we just call the tokenizer function and sentence by its code which was shown in the df.head() command’s output.
```
tokenize(df.hindi_sentence[0],"hi")
tokenize(df.hindi_sentence[1],"hi")
tokenize(df.hindi_sentence[2],"hi")
tokenize(df.hindi_sentence[3],"hi")
tokenize(df.hindi_sentence[4],"hi")
```
We will receive the output in the form of tokens of the sentence provided.
<br>Alternative way to provide sentence to our program is by specifying the string name and providing the sentence or paragraph as input, like this:
```
hindi_input = """प्राचीन काल में विक्रमादित्य नाम के एक आदर्श राजा हुआ करते थे।<br>
अपने साहस, पराक्रम और शौर्य के लिए  राजा विक्रम मशहूर थे। <br>
ऐसा भी कहा जाता है कि राजा विक्रम अपनी प्राजा के जीवन के दुख दर्द जानने के लिए रात्री के पहर में भेष बदल कर नगर में घूमते थे।"""
```
The tokenize command now will be provided in the format of:<br>
tokenize(input text, language code)
```
tokenize(hindi_input, "hi")
```
This command’s output will also provide us tokens of the given paragraph which we provided in “hindi_input”.
<br>Further in this tokenizer, we have imported the feature to remove foreign languages as well.
```
from inltk.inltk import remove_foreign_languages
```
The command to implement this import is of the format:
```
Remove_foreign_languages(text, “<language-code>”)
```
If any word in the sentence is detected by the program which doesn’t belong to the language whose language code we have provided in the command, then the word will turn out in the output as <unk>
```
remove_foreign_languages("इस्लाम धर्म (الإسلام) ईसाई धर्म के बाद अनुयाइयों के आधार पर दुनिया का दूसरा सब से बड़ा धर्म है।", "hi")
```
Here, الإسلام is not a Hindi word, hence it will be <unk> in the output.
