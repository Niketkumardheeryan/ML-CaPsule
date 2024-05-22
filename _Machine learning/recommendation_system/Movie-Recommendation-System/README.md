
# MOVIE-RECOMMENDATION-SYSTEM


## What are recommender systems?
Well, like I said Amazon is a great example, and one I'm very familiar with. So, if you go to their recommendations section, you can see that it will recommend things that you might be interested in purchasing based on your past behavior on the site. The recommender system might include things that you've rated, or things that you bought, and other data as well. But, it's pretty cool. You can also think of the people who bought this also bought feature on Amazon as a form of recommender system.
## Approach

The problem was divided into several steps:

* **Data Collection**: Data was collected from the MovieLens website and through a script that queried for data from various TMDB Endpoints.


* **Data Wrangling**: The datasets were uploaded to a dataframe and explored. Null values were filled in wherever appropriate and polluted values were discarded or wrangled.


* **EDA**: Extensive data visualisation and summary statistics were used to extract insights and pattern from the various datasets. The history, facts and trivia behind movies were narrated through data.


* **Machine Learning**: Gradient Boosting Classifer and Regressor were trained on our feature engineered dataset to predict movie success and revenue respectively. Their feature importances were noted to gain insights into what factors influence the revenues of a movie relative to budget.


* **Recommendation Systems**: Four different recommendation systems were built using various ideas and algorithms such as IMDB's Weighted Rating, Content Based Filtering and Collaborative Filtering.

## Collaborative Filtering

First, let's talk about recommending stuff based on your past behavior. One technique is called user-based collaborative filtering, and here's how it works:

Collaborative filtering, by the way, is just a fancy name for saying recommending stuff based on the combination of what you did and what everybody else did, okay? So, it's looking at your behavior and comparing that to everyone else's behavior, to arrive at the things that might be interesting to you that you haven't heard of yet.
1. The idea here is we build up a matrix of everything that every user has ever bought, or viewed, or rated, or whatever signal of interest that you want to base the system on. So basically, we end up with a row for every user in our system, and that row contains all the things they did that might indicate some sort of interest in a given product. So, picture a table, I have users for the rows, and each column is an item, okay? That might be a movie, a product, a web page, whatever; you can use this for many different things.
2. I then use that matrix to compute the similarity between different users. So, I basically treat each row of this as a vector and I can compute the similarity between each vector of users, based on their behavior.
## Item-based collaborative filtering
Let's now try to address some of the shortcomings in user-based collaborative filtering with a technique called item-based collaborative filtering, and we'll see how that can be more powerful. It's actually one of the techniques that Amazon uses under the hood, and they've talked about this publicly so I can tell you that much, but let's see why it's such a great idea. With user-based collaborative filtering we base our recommendations on relationships between people, but what if we flip that and base them on relationships between items? That's what item-based collaborative filtering is.


The other advantage is that there are generally fewer things that you're trying to recommend than there are people you're recommending to. So again, 7 billion people in the world, you're probably not offering 7 billion things on your website to recommend to them, so you can save a lot of computational resources by evaluating relationships between items instead of users, because you will probably have fewer items than you have users in your system. That means you can run your recommendations more frequently, make them more current, more up-to-date, and better! You can use more complicated algorithms because you have less relationships to compute, and that's a good thing!

## Software Required
* Jupyter Notebook
* Python 

## Python Libraries 
* Numpy
* Matplotlib and seaborn
* scikit-learn
* nltk
* surprise
