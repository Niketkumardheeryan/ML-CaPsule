from experiment_logger import ExperimentLogger
from metrics_tracker import track_accuracy, display_metrics

# Dummy values for demonstration
y_true = [1, 0, 1, 1, 0]
y_pred = [1, 0, 1, 0, 0]

# Calculate accuracy
accuracy = track_accuracy(y_true, y_pred)

# Display metrics
display_metrics(accuracy)

# Initialize logger
logger = ExperimentLogger()

# Log experiment
logger.log_experiment(
    model_name="DemoClassifier",
    dataset="Dummy Dataset",
    accuracy=accuracy,
    parameters={
        "learning_rate": 0.01,
        "epochs": 10
    }
)