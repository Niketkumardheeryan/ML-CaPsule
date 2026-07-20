def track_accuracy(y_true, y_pred):
    correct = sum(y_true[i] == y_pred[i] for i in range(len(y_true)))
    return correct / len(y_true)


def display_metrics(accuracy):
    print(f"📊 Model Accuracy: {accuracy * 100:.2f}%")