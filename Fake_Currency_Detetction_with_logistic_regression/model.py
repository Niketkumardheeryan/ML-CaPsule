import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix, accuracy_score
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split

class LogisticRegression:
    def __init__(self):
        self.x = None
        self.y = None
        self._y = None
        self.w = None
        self.b = None
        self.w_error = None
        self.b_error = None
        self.epoch_count = 1
        self.epoch_limit = None
        self.loss_history = [] # Added to track loss for visualization

    def predict_proba(self, x):
        """Returns the raw probability between 0 and 1"""
        # Force the input to a float array to prevent dtype object errors
        x_array = np.array(x, dtype=float)
        
        # Now run the math safely
        return 1 / (1 + np.exp(-(np.dot(x_array, self.w) + self.b)))

    def predict(self, x, threshold=0.5):
        """Returns the binary class prediction (0 or 1)"""
        return (self.predict_proba(x) >= threshold).astype(int)

    def fit(self, x, y, epochs=1000, gamma=0.5):
        # Force pure numpy arrays and flatten y to prevent broadcasting bugs
        self.x = np.array(x, dtype=float)
        self.y = np.squeeze(np.array(y, dtype=float))
        
        self.w = np.random.randn(self.x.shape[1]) * 0.01
        self.b = 0
        self.cutoff = epochs / 10
        self.epoch_limit = epochs
        self.epoch_count = 1
        self.loss_history = []

        while self.epoch_count <= self.epoch_limit:
            self._y = self.predict_proba(self.x)
            
            # Calculate Gradients
            self.b_error = -(np.mean(self.y - self._y))
            self.w_error = -(np.dot(self.x.transpose(), self.y - self._y)) / self.x.shape[0]
            
            # Standard Gradient Descent Update
            self.w = self.w - gamma * self.w_error
            self.b = self.b - gamma * self.b_error
            
            # Loss Calculation
            epsilon = 1e-15 
            loss = -np.mean(self.y * np.log(self._y + epsilon) + (1 - self.y) * np.log(1 - self._y + epsilon))
            self.loss_history.append(loss)
            
            if self.epoch_count % self.cutoff == 0:
                print(f'Epoch : {self.epoch_count} Loss : {loss:.6f}')
                
            self.epoch_count += 1

def visualize_training_and_evaluation(model, X_train, y_train, X_test, y_test):
    """
    Takes a trained model and data, and plots the loss curve, 
    decision boundary (if 2D), and confusion matrix.
    """
    plt.figure(figsize=(18, 5))

    # 1. Plot Training Loss Curve
    plt.subplot(1, 3, 1)
    plt.plot(model.loss_history, color='blue', linewidth=2)
    plt.title('Training Loss over Epochs')
    plt.xlabel('Epoch')
    plt.ylabel('Binary Cross-Entropy Loss')
    plt.grid(True, linestyle='--', alpha=0.7)

    # 2. Plot Decision Boundary (Only works if data has exactly 2 features)
    plt.subplot(1, 3, 2)
    if X_train.shape[1] == 2:
        # Create a mesh grid
        x_min, x_max = X_train[:, 0].min() - 1, X_train[:, 0].max() + 1
        y_min, y_max = X_train[:, 1].min() - 1, X_train[:, 1].max() + 1
        xx, yy = np.meshgrid(np.arange(x_min, x_max, 0.02),
                             np.arange(y_min, y_max, 0.02))
        
        # Predict across the grid
        Z = model.predict(np.c_[xx.ravel(), yy.ravel()])
        Z = Z.reshape(xx.shape)
        
        # Plot contour and test data points
        plt.contourf(xx, yy, Z, alpha=0.3, cmap='coolwarm')
        plt.scatter(X_test[:, 0], X_test[:, 1], c=y_test, edgecolors='k', cmap='coolwarm')
        plt.title('Decision Boundary (Test Data)')
        plt.xlabel('Feature 1')
        plt.ylabel('Feature 2')
    else:
        plt.text(0.5, 0.5, f'Data has {X_train.shape[1]} features.\nDecision boundary requires exactly 2D data.', 
                 horizontalalignment='center', verticalalignment='center', fontsize=12)
        plt.axis('off')

    # 3. Plot Confusion Matrix
    plt.subplot(1, 3, 3)
    y_pred = model.predict(X_test)
    cm = confusion_matrix(y_test, y_pred)
    acc = accuracy_score(y_test, y_pred)
    
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', cbar=False, 
                annot_kws={"size": 16})
    plt.title(f'Test Confusion Matrix\nAccuracy: {acc * 100:.1f}%')
    plt.xlabel('Predicted Label')
    plt.ylabel('True Label')

    plt.tight_layout()
    plt.show()

# ==========================================
# Example Usage Block
# ==========================================
if __name__ == "__main__":
    # 1. Generate dummy 2D linearly separable data
    X, y = make_classification(n_samples=500, n_features=2, n_redundant=0, 
                               n_informative=2, random_state=42, n_clusters_per_class=1)
    
    # 2. Split into Train and Test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    from sklearn.preprocessing import StandardScaler
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    # 3. Initialize and Train the custom model
    model = LogisticRegression()
    print("Starting Training...")
    model.fit(X_train, y_train, epochs=1000, gamma=0.1)
    print("Training Complete!\n")

    # 4. Generate Visualizations
    visualize_training_and_evaluation(model, X_train, y_train, X_test, y_test)