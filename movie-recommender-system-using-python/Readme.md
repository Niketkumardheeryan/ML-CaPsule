## Movie Recommendation System

### Data Set
[Data Set](https://github.com/Binal02Singh/ML-CaPsule/blob/Movie-Recommender-System/Movie-Recommender-System%20using%20python/data/movies%20(1).csv) : This data set has been taken from Kaggle.com.

### Use
This feature will recommend movies on the basis of the searches they did.


### Dependencies
- numpy
- sklearn
- difflab
- pandas

## APPROACH
The basic approach was to recommend movies on the basis of keywords rather than rating

- First of all we gathered all the data from kaggle website

- Then we kept all the important coloumns like genre, cast, crew, title.
And converted all the data inside them into readable format and in the cast and crew section removed most of the names and kept only a few, like main 3 actors in cast and only director in crew.

- Now we merged all of the coloumns into a single tag.
 <img width="350" alt="Screenshot 2022-03-14 at 11 22 36 AM" src="https://user-images.githubusercontent.com/72695669/158113146-32586f2f-7d1b-4e2a-8b2a-28352bd36b4b.png">

- Since all the data is combined, we converted it into vector form using "sklearn.feature_extraction.text".
  <img width="350" alt="Screenshot 2022-03-14 at 11 22 50 AM" src="https://user-images.githubusercontent.com/72695669/158113253-e3dd7b50-7012-4aa6-a046-fca31e377f8b.png">


- Finally, when the search is done by the user, this system prints the closest vector's movie name using "cosine_similarity"
  <img width="606" alt="Screenshot 2022-03-14 at 11 23 04 AM" src="https://user-images.githubusercontent.com/72695669/158113297-cc79389b-3335-4c9e-8218-455fc74b31bc.png">

### Prediction
<img width="399" alt="Screenshot 2022-03-14 at 11 23 21 AM" src="https://user-images.githubusercontent.com/72695669/158113320-8ee72e83-db9b-4882-aeda-12eecd7bb8e4.png">


