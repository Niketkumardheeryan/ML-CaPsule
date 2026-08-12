# Chess Piece Classification using Machine Learning

This project involves developing a machine learning application to classify chess pieces from images using a Convolutional Neural Network (CNN). The process begins with collecting and preprocessing a dataset of chess piece images, including various classes such as bishop, king, knight, pawn, queen, and rook. The images are resized, normalized, and split into training and validation sets to train the CNN model. The model's performance is evaluated based on accuracy, precision, recall, and F1 score.

For real-time predictions, a Streamlit application is created. Users can upload images of chess pieces, which are then processed and classified by the trained model. The application displays the prediction result in a styled success box with bold white text, and also provides additional information about the identified chess piece.

## Model Training and Evaluation

CNN model is trained over batch size = 128, with 100 epochs, input image size = (128,128,3), achieved average validation accuracy of 97.11%.

## Dataset

https://www.kaggle.com/datasets/s4lman/chess-pieces-dataset-85x85

## Inference

Deployed the model with the help of a Streamlit web application to classify the chess piece and provide info regarding its moves with the help of text and visuals.

## Results

See `Classification_Results.pdf` for EDA visualizations, training curves, confusion matrix, and prediction examples.

## Libraries Used

1. **Scikit-learn**: For machine learning processing and operations
2. **Matplotlib**: For plotting and visualizing the detection results
3. **Pandas**: For image manipulation
4. **NumPy**: For efficient numerical operations
5. **Seaborn**: For advanced data visualizations
6. **Plotly**: For 3D data visualizations
7. **Streamlit**: For creating the GUI of the web application
8. **TensorFlow**: For image-based manipulation operations

## How to Use

1. **Clone the Repository**:
```sh
   git clone https://github.com/Niketkumardheeryan/ML-CaPsule.git
   cd "ML-CaPsule/Chess Based Project/Chess_Piece_Classification"
```

2. **Install Dependencies**:
```sh
   pip install -r requirements.txt
```

3. **Download the Model**:
   Download `final_chess.h5` from the link below and place it in this same directory:
   https://drive.google.com/file/d/1QK6a2yCJo3EvKvoEJA6QGkcFEmzm5IiG/view?usp=sharing

4. **Run the App**:
```sh
   streamlit run app.py
```

5. **View Results**: Upload a chess piece image to classify it and see information about its moves, with text and visuals.

## Demo

https://github.com/user-attachments/assets/c06554e5-81ff-4151-97a9-74fdfb4ff760
