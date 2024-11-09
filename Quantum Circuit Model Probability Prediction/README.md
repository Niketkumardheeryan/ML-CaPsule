# Quantum-Circuit-Probability-Prediction-using-ML

The Quantum Circuit Probability Predictor is a machine learning-based application designed to predict the probability of measuring a specific quantum state after applying a series of quantum gates to a qubit. Leveraging the principles of quantum mechanics and classical machine learning, this project aims to create a robust model that accurately estimates the probabilities associated with different quantum states resulting from varied input parameters.

The core functionalities include:

Quantum Circuit Simulation: 
-----------------------------
Utilizing Qiskit's advanced quantum simulation capabilities, the project creates quantum circuits that implement rotations around the X-axis based on user-defined angles.

State Probability Calculation:
-------------------------------
The application computes the probabilities of measuring the |0⟩ and |1⟩ states for various angles, using statevector sampling to retrieve the state vector of the quantum circuit after the operations are performed.

Model Training: 
----------------
A machine learning model is trained on the computed probabilities to predict outcomes for angles not seen during training, enabling the model to generalize well to new inputs.

Interactive Visualization: 
--------------------------
The project features an intuitive interface that allows users to input angles and visualize the resulting probabilities and model predictions, enhancing the understanding of quantum state dynamics.

Educational Tool:
-----------------
This project serves as an educational resource for students and enthusiasts interested in quantum computing and machine learning, demonstrating the intersection of these fields through hands-on experience.

Technologies Used:
------------------
Quantum Computing Framework: Qiskit
Machine Learning: Python, NumPy, and relevant ML libraries (e.g., scikit-learn, TensorFlow, or PyTorch)
Data Visualization: Matplotlib or similar libraries for plotting probabilities and predictions
User Interface: Streamlit or Flask for creating a web application interface (to be deployed soon after making model more optimized)

Sample Output of predicted probability 
![1000034342](https://github.com/user-attachments/assets/bc3fc538-ef41-47bb-a685-a2ff63d942cc)
![1000034344](https://github.com/user-attachments/assets/dc0d666e-8417-4c9c-88eb-2ae33b85ccc0)
