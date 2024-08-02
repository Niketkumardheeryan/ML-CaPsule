# Chess Piece Classification using Machine learning

This project involves developing a machine learning application to classify chess pieces from images using a Convolutional Neural Network (CNN). The process begins with collecting and preprocessing a dataset of chess piece images, including various classes such as bishop, king, knight, pawn, queen, and rook. The images are resized, normalized, and split into training and validation sets to train the CNN model. The model's performance is evaluated based on accuracy, precision, recall, and F1 score.

For real-time predictions, a Streamlit application is created. Users can upload images of chess pieces, which are then processed and classified by the trained model. The application displays the prediction result in a styled success box with bold white text, and also provides additional information about the identified chess piece. The project integrates image preprocessing, model inference, and user interaction, showcasing how machine learning models can be deployed in web applications for practical use cases.


## Model Training and evaluation :
 
CNN model is trained over batch size = 128 ,with 100 epochs input image size =(128,128,3)  achieved average validation accuracy of 97.11 %

## Dataset :

https://www.kaggle.com/datasets/akshayramakrishnan28/cataract-classification-dataset/data


## Inference : 

Deployed the model with the help streamlit web application to classify the chess piece and provide info regarding its moves with the help of text and visuals.

## Libraries Used


1. **Scikit learn**: For machine learning processing  and operations
2. **Matplotlib**: For plotting and visualizing the detection results.
3. **Pandas**: For image manipulation.
4. **NumPy**: For efficient numerical operations.
5. **Seaborn** : for advanced data visualizations
6. **plotly** : for 3D data visualizations .
7. **Streamlit** : for creating gui of the web application.
8. **Tensorflow** : for image based manipulation operations.


## How to Use

1. **Clone the Repository**: 
    ```sh
    git clone url_to_this_repository
    ```

2. **Install Dependencies**: 
    ```sh
    pip install -r requirements.txt
    ```

3. **Run the Model**: 
    (download the model final_chess.h5 from below link and put in same directoy :
      https://drive.google.com/file/d/1QK6a2yCJo3EvKvoEJA6QGkcFEmzm5IiG/view?usp=sharing)

    ```python
    streamlit run app.py
    ```

4. **View Results**: The script will allow you to classify the chess image and give information regrading tis moves with the help of text and visuals .

**DEMO** :

