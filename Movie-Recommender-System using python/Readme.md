# Movie Recommendation System
It is a basic movie recommender using python. The data has been taken from kaggle, this data consists of 5000 movies. This system basically recommends 5 movies to the user on the basis of genre, cast, crew etc
## APPROACH
The basic approach was to recommend movies on the basis of keywords rather than rating

- First of all I gathered all the data from kaggle website

- Then I kept all the important coloumns like genre, cast, crew, title.
And converted all the data inside them into readable format and in the cast and crew section removed most of the names and kept only a few, like main 3 actors in cast and only director in crew.

- Now I merged all of the coloumns into a single tag.

- Since all the data is combined, I converted it into vector form using "sklearn.feature_extraction.text".

- Finally, when the search is done by the user, this system prints the closest vector's movie name using "cosine_similarity"

