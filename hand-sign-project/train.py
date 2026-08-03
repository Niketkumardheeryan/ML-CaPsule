"""Train an LSTM model on the collected hand landmark sequences.

Usage:
    python train.py --data_dir data --model_dir models
"""
import os
import json
import numpy as np
from glob import glob
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt
try:
    import tensorflow as tf
    from tensorflow.keras.models import Sequential
    from tensorflow.keras.layers import LSTM, Dense, Dropout
    from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping
    TF_AVAILABLE = True
except Exception:
    TF_AVAILABLE = False


def load_data(data_dir, gestures):
    X = []
    y = []
    for idx, gesture in enumerate(gestures):
        files = glob(os.path.join(data_dir, gesture, '*.npy'))
        for f in files:
            seq = np.load(f)
            # ensure shape (sequence_length, 63)
            X.append(seq)
            y.append(gesture)
    X = np.array(X)
    y = np.array(y)
    return X, y


def build_model(input_shape, num_classes):
    model = Sequential([
        LSTM(64, return_sequences=True, input_shape=input_shape),
        Dropout(0.3),
        LSTM(128, return_sequences=True),
        Dropout(0.3),
        LSTM(64),
        Dense(64, activation='relu'),
        Dropout(0.3),
        Dense(num_classes, activation='softmax')
    ])
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    return model


def plot_history(history, out_dir):
    plt.figure(figsize=(8,4))
    plt.plot(history.history['accuracy'], label='train_acc')
    plt.plot(history.history['val_accuracy'], label='val_acc')
    plt.legend(); plt.title('Accuracy')
    plt.savefig(os.path.join(out_dir, 'accuracy.png'))
    plt.close()

    plt.figure(figsize=(8,4))
    plt.plot(history.history['loss'], label='train_loss')
    plt.plot(history.history['val_loss'], label='val_loss')
    plt.legend(); plt.title('Loss')
    plt.savefig(os.path.join(out_dir, 'loss.png'))
    plt.close()


def main(data_dir='data', model_dir='models', outputs_dir='outputs', gestures=None):
    if gestures is None:
        gestures = ['A','B','C','D','E','Hello','Thanks','Yes','No','I_Love_You']
    os.makedirs(model_dir, exist_ok=True)
    os.makedirs(outputs_dir, exist_ok=True)

    X, y = load_data(data_dir, gestures)
    if len(X) == 0:
        raise RuntimeError('No data found. Run collect_data.py first')

    if not TF_AVAILABLE:
        print('\nTensorFlow is not available in this environment.\n')
        print('To train the model, install TensorFlow (see requirements-tf.txt) and re-run this script.')
        return

    # padding/trimming sequences to same length
    seq_len = X[0].shape[0]
    X = np.array([x if x.shape[0]==seq_len else np.resize(x, (seq_len, x.shape[1])) for x in X])

    le = LabelEncoder()
    y_enc = le.fit_transform(y)
    num_classes = len(le.classes_)
    y_cat = tf.keras.utils.to_categorical(y_enc, num_classes=num_classes)

    X_train, X_test, y_train, y_test = train_test_split(X, y_cat, test_size=0.2, random_state=42, stratify=y)

    model = build_model((X.shape[1], X.shape[2]), num_classes)
    model.summary()

    checkpoint = ModelCheckpoint(os.path.join(model_dir, 'best_model.h5'), monitor='val_accuracy', save_best_only=True, verbose=1)
    early = EarlyStopping(monitor='val_accuracy', patience=10, restore_best_weights=True)

    history = model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=100, batch_size=16, callbacks=[checkpoint, early])

    # save final model
    model.save(os.path.join(model_dir, 'final_model.h5'))

    # save label encoder classes
    with open(os.path.join(model_dir, 'labels.json'), 'w') as f:
        json.dump(list(le.classes_), f)

    plot_history(history, outputs_dir)

    # predictions
    y_pred = np.argmax(model.predict(X_test), axis=1)
    y_true = np.argmax(y_test, axis=1)

    cm = confusion_matrix(y_true, y_pred)
    cr = classification_report(y_true, y_pred, target_names=le.classes_)
    print('Classification Report:\n', cr)

    # save confusion matrix figure
    plt.figure(figsize=(8,6))
    plt.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
    plt.title('Confusion matrix')
    plt.colorbar()
    tick_marks = np.arange(len(le.classes_))
    plt.xticks(tick_marks, le.classes_, rotation=45)
    plt.yticks(tick_marks, le.classes_)
    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    plt.tight_layout()
    plt.savefig(os.path.join(outputs_dir, 'confusion_matrix.png'))
    plt.close()

    with open(os.path.join(outputs_dir, 'classification_report.txt'), 'w') as f:
        f.write(cr)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_dir', type=str, default='data')
    parser.add_argument('--model_dir', type=str, default='models')
    parser.add_argument('--outputs_dir', type=str, default='outputs')
    args = parser.parse_args()
    main(args.data_dir, args.model_dir, args.outputs_dir)
