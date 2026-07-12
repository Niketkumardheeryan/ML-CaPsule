# Face Mask Detection

This project uses Convolutional Neural Networks (CNN) and OpenCV to detect whether a person is wearing a face mask or not, in real time via webcam. The model is trained on thousands of labeled images and can classify faces as "With Mask" or "Without Mask" with high confidence, making it useful for public safety monitoring in settings like offices, hospitals, and public transport.

## Dataset
- Source: Face Mask dataset (with_mask / without_mask images)
- Total images: 7553
- Classes: `with_mask`, `without_mask`

## Key Features
1. CNN-based image classification (with_mask vs without_mask)
2. Real-time face mask detection using webcam feed (OpenCV)
3. Achieves 97.7% classification accuracy
4. Training/validation accuracy and loss visualization
5. Confidence-scored predictions on sample test images
6. Trained using TensorFlow/Keras

## Tech Stack
- Python
- TensorFlow / Keras
- OpenCV
- NumPy
- Matplotlib
- scikit-learn (train_test_split)

## Usage
1. Open `Face_Mask_Detection.ipynb` in Jupyter Notebook or Google Colab.
2. Run all cells to train the CNN model on the dataset.
3. Run `webcam_detection.py` to start real-time face mask detection using your webcam.
4. Review the accuracy/loss plots and sample predictions in `results.pdf`.
