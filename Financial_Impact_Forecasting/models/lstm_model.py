from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense, Dropout, SpatialDropout1D

def build_lstm_model(vocab_size, embedding_dim=128, input_length=50, num_classes=3):
    """
    Builds an LSTM Deep Learning model to classify financial news impact levels.
    """
    model = Sequential([
        Embedding(vocab_size, embedding_dim, input_length=input_length),
        SpatialDropout1D(0.3),
        LSTM(64, dropout=0.2, recurrent_dropout=0.2, return_sequences=False),
        Dense(32, activation='relu'),
        Dropout(0.3),
        Dense(num_classes, activation='softmax') # Multi-class output (LOW, MEDIUM, HIGH)
    ])
    
    model.compile(
        loss='sparse_categorical_crossentropy',
        optimizer='adam',
        metrics=['accuracy']
    )
    return model
