## Movie Genre Classification

### Data Set
The dataset used for this project is stored in the file `train_data.txt`.

### Use
The "Movie Genre.ipynb" file is a Jupyter notebook that analyzes movie genres using machine learning techniques. 

### Dependencies
The notebook imports the following libraries:
- Matplotlib for plotting visualizations
- Seaborn for enhancing the visualizations with different styles and color palettes
- GridSearchCV from scikit-learn for hyperparameter tuning in the Logistic Regression model
- LogisticRegression from scikit-learn for training the classification model

## APPROACH
The provided file is a Jupyter notebook named "Movie Genre.ipynb" that analyzes movie genres using machine learning techniques. Here is a summary of its contents:

Data Preprocessing
- The notebook starts by loading the movie data into a DataFrame named "train_df".
- It extracts the unique genres from the 'Genre' column and displays the list of 28 unique genres
- A horizontal bar plot is created to visualize the distribution of genres, showing the count of each genre
- The 'Description' column is preprocessed using the 'preprocessing' function, and the cleaned descriptions are    added to the DataFrame as a new column 'Description_clean'

Exploratory Data Analysis
- The first few rows of the DataFrame are displayed to show the structure of the data
- Another bar plot is created to visualize the distribution of genres using a different color palette and edge color

Feature Engineering and Modeling
- Unnecessary columns ('Title', 'Id', 'Description') are dropped from the DataFrame, leaving only 'Genre' and 'Description_clean'
- The 'Genre' column is encoded using a dictionary mapping each genre to a unique integer value
- The encoded genres are added to the DataFrame as a new column 'Genre_encoded'
- The data is split into features (X) and target variable (y), where X is the 'Description_clean' column and y is the 'Genre_encoded' column
- The text data in X is vectorized using TF-IDF vectorization with a maximum of 5000 features
- A Logistic Regression model is trained using GridSearchCV to find the best hyperparameter (C) based on 5-fold cross-validation
- The best model is evaluated on the test set, and the score is printed
- A classification report is generated to show the precision, recall, f1-score, and support for each genre


The notebook demonstrates the process of preprocessing movie data, exploring genre distributions, and training a Logistic Regression model to classify movies based on their descriptions. The model's performance is evaluated using the test set and a classification report.

## Author

### [Manav Malhotra](https://github.com/Manav173)

## License

This project is licensed under the MIT License.