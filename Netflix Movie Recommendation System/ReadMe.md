# Netflix-Recommendation-System

### Goal:
- The goal is to recommend Netflix movies based on their genres.
- The system allows users to input a movie title and receive recommendations of similar movies.

### Project Overview:
The project utilizes a combination of data preprocessing techniques, feature extraction methods, and machine learning algorithms to build a content-based recommendation system for Netflix movies. The interactive web interface is developed using Streamlit to enhance user experience and accessibility.

### Workflow Summary:
- The dataset containing movie titles, descriptions, content types, and genres is loaded and preprocessed.
- Text data (genres) is transformed into numerical form using TF-IDF vectors.
- Cosine similarity is calculated between TF-IDF vectors of different movies to determine their similarity.
- A function is created to take user input (movie title) and return recommendations based on similarity scores.
- Streamlit is employed to create a user-friendly interface, allowing users to input movie titles and view recommendations seamlessly.

### Output Screenshot:
![netflix_recommendation_system](https://github.com/manikdamle/Netflix-Recommendation-System/assets/115721290/8002c92f-ceea-4828-90c1-a66390e42403)
