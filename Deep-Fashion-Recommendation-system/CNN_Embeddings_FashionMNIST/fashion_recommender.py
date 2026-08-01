"""Fashion recommendation system built on Fashion-MNIST.

The pipeline has three stages:

1. **Classify** — a small CNN is trained to recognise the ten Fashion-MNIST
   categories (t-shirt, trouser, pullover, ...).
2. **Embed** — the penultimate dense layer of that trained CNN is reused as a
   feature extractor, turning every 28x28 image into a 128-dimensional vector
   that encodes what the item *looks like*.
3. **Recommend** — a nearest-neighbour index over those vectors retrieves the
   visually most similar items for any query image.

TensorFlow is imported lazily inside the functions that need it, so the
retrieval and metric helpers can be imported (and unit tested) in an
environment where only NumPy and scikit-learn are installed.
"""

from __future__ import annotations

import numpy as np

CLASS_NAMES = [
    "T-shirt/top",
    "Trouser",
    "Pullover",
    "Dress",
    "Coat",
    "Sandal",
    "Shirt",
    "Sneaker",
    "Bag",
    "Ankle boot",
]

IMAGE_SHAPE = (28, 28, 1)
EMBEDDING_LAYER = "embedding"


# --------------------------------------------------------------------- data
def load_fashion_mnist():
    """Load Fashion-MNIST, scaled to [0, 1] and shaped for a CNN.

    Returns ``(x_train, y_train), (x_test, y_test)`` where the images are
    float32 arrays of shape ``(n, 28, 28, 1)``.
    """
    from tensorflow import keras

    (x_train, y_train), (x_test, y_test) = keras.datasets.fashion_mnist.load_data()
    x_train = (x_train.astype("float32") / 255.0)[..., np.newaxis]
    x_test = (x_test.astype("float32") / 255.0)[..., np.newaxis]
    return (x_train, y_train), (x_test, y_test)


def class_distribution(labels) -> dict[str, int]:
    """Count how many samples each class contributes."""
    values, counts = np.unique(np.asarray(labels), return_counts=True)
    return {CLASS_NAMES[int(v)]: int(c) for v, c in zip(values, counts)}


# -------------------------------------------------------------------- model
def build_cnn(input_shape=IMAGE_SHAPE, num_classes=10, embedding_dim=128):
    """Build the classification CNN whose penultimate layer is the embedding.

    The layer named ``embedding`` is what the recommender reuses, so it is given
    an explicit name rather than relying on the layer index.
    """
    from tensorflow import keras
    from tensorflow.keras import layers

    return keras.Sequential(
        [
            layers.Input(shape=input_shape),
            layers.Conv2D(32, 3, padding="same", activation="relu"),
            layers.BatchNormalization(),
            layers.Conv2D(32, 3, padding="same", activation="relu"),
            layers.MaxPooling2D(),
            layers.Dropout(0.25),
            layers.Conv2D(64, 3, padding="same", activation="relu"),
            layers.BatchNormalization(),
            layers.Conv2D(64, 3, padding="same", activation="relu"),
            layers.MaxPooling2D(),
            layers.Dropout(0.25),
            layers.Flatten(),
            layers.Dense(embedding_dim, activation="relu", name=EMBEDDING_LAYER),
            layers.Dropout(0.5),
            layers.Dense(num_classes, activation="softmax", name="predictions"),
        ],
        name="fashion_cnn",
    )


def compile_model(model, learning_rate=1e-3):
    """Compile the CNN for integer-labelled multi-class classification."""
    from tensorflow import keras

    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=learning_rate),
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"],
    )
    return model


def train_model(model, x_train, y_train, epochs=15, batch_size=128,
                validation_split=0.1, patience=3, verbose=2):
    """Train the CNN, restoring the best weights seen on the validation split."""
    from tensorflow import keras

    early_stopping = keras.callbacks.EarlyStopping(
        monitor="val_accuracy", patience=patience, restore_best_weights=True
    )
    return model.fit(
        x_train,
        y_train,
        epochs=epochs,
        batch_size=batch_size,
        validation_split=validation_split,
        callbacks=[early_stopping],
        verbose=verbose,
    )


def build_feature_extractor(model, layer_name=EMBEDDING_LAYER):
    """Return a model that maps images to the trained embedding vectors."""
    from tensorflow import keras

    return keras.Model(inputs=model.inputs,
                       outputs=model.get_layer(layer_name).output,
                       name="fashion_feature_extractor")


def extract_embeddings(model, images, layer_name=EMBEDDING_LAYER, batch_size=256):
    """Run ``images`` through the feature extractor and return the embeddings."""
    extractor = build_feature_extractor(model, layer_name)
    return extractor.predict(images, batch_size=batch_size, verbose=0)


# ---------------------------------------------------------------- retrieval
def l2_normalize(matrix, epsilon: float = 1e-10):
    """Scale each row to unit length so dot products become cosine similarity."""
    matrix = np.asarray(matrix, dtype="float32")
    if matrix.ndim == 1:
        matrix = matrix[np.newaxis, :]
    norms = np.linalg.norm(matrix, axis=1, keepdims=True)
    return matrix / np.maximum(norms, epsilon)


class FashionRecommender:
    """Nearest-neighbour recommender over a gallery of image embeddings."""

    def __init__(self, embeddings, labels, images=None, metric: str = "cosine") -> None:
        self.embeddings = l2_normalize(embeddings)
        self.labels = np.asarray(labels)
        self.images = images
        self.metric = metric
        self._index = None

        if len(self.embeddings) != len(self.labels):
            raise ValueError(
                f"embeddings and labels disagree: {len(self.embeddings)} vs {len(self.labels)}"
            )

    def fit(self, n_neighbors: int = 10) -> "FashionRecommender":
        """Build the nearest-neighbour index over the gallery."""
        from sklearn.neighbors import NearestNeighbors

        n_neighbors = min(n_neighbors, len(self.embeddings))
        self._index = NearestNeighbors(n_neighbors=n_neighbors, metric=self.metric)
        self._index.fit(self.embeddings)
        return self

    def recommend(self, query, k: int = 5):
        """Return ``(indices, similarities)`` for the ``k`` closest gallery items.

        ``query`` may be a single embedding or a batch of them. Similarities are
        cosine similarities in ``[0, 1]``, highest first.
        """
        if self._index is None:
            raise RuntimeError("call fit() before recommend()")

        queries = l2_normalize(query)
        k = min(k, len(self.embeddings))
        distances, indices = self._index.kneighbors(queries, n_neighbors=k)
        return indices, 1.0 - distances

    def recommend_labels(self, query, k: int = 5):
        """Return the class names of the ``k`` recommended items."""
        indices, _ = self.recommend(query, k=k)
        return [[CLASS_NAMES[int(self.labels[i])] for i in row] for row in indices]


def precision_at_k(recommender: FashionRecommender, query_embeddings,
                   query_labels, k: int = 5) -> float:
    """Fraction of recommended items that share the query's category.

    This is the standard way to score a content-based recommender when the only
    ground truth available is the category label: a perfect system returns
    ``k`` items of the same kind as the query, giving 1.0.
    """
    indices, _ = recommender.recommend(query_embeddings, k=k)
    retrieved = recommender.labels[indices]
    expected = np.asarray(query_labels).reshape(-1, 1)
    return float((retrieved == expected).mean())


def per_class_precision_at_k(recommender: FashionRecommender, query_embeddings,
                             query_labels, k: int = 5) -> dict[str, float]:
    """Precision@k broken down by query category, to expose weak spots."""
    indices, _ = recommender.recommend(query_embeddings, k=k)
    retrieved = recommender.labels[indices]
    query_labels = np.asarray(query_labels)
    hits = (retrieved == query_labels.reshape(-1, 1)).mean(axis=1)

    scores = {}
    for label in np.unique(query_labels):
        scores[CLASS_NAMES[int(label)]] = float(hits[query_labels == label].mean())
    return scores


# ----------------------------------------------------------------- plotting
def plot_training_curves(history, save_path=None):
    """Plot accuracy and loss for the training and validation splits."""
    import matplotlib.pyplot as plt

    metrics = history.history if hasattr(history, "history") else history
    figure, axes = plt.subplots(1, 2, figsize=(12, 4))

    axes[0].plot(metrics["accuracy"], label="train", marker="o", markersize=3)
    axes[0].plot(metrics["val_accuracy"], label="validation", marker="o", markersize=3)
    axes[0].set_title("Model accuracy")
    axes[0].set_xlabel("epoch")
    axes[0].set_ylabel("accuracy")

    axes[1].plot(metrics["loss"], label="train", marker="o", markersize=3)
    axes[1].plot(metrics["val_loss"], label="validation", marker="o", markersize=3)
    axes[1].set_title("Model loss")
    axes[1].set_xlabel("epoch")
    axes[1].set_ylabel("loss")

    for axis in axes:
        axis.legend()
        axis.grid(alpha=0.3)

    figure.tight_layout()
    if save_path:
        figure.savefig(save_path, dpi=120, bbox_inches="tight")
    return figure


def plot_confusion_matrix(y_true, y_pred, save_path=None, normalize=True):
    """Plot the confusion matrix of the classifier over the ten categories."""
    import matplotlib.pyplot as plt
    from sklearn.metrics import confusion_matrix

    matrix = confusion_matrix(y_true, y_pred)
    if normalize:
        matrix = matrix.astype("float") / matrix.sum(axis=1, keepdims=True)

    figure, axis = plt.subplots(figsize=(8, 7))
    image = axis.imshow(matrix, cmap="Blues", vmin=0, vmax=matrix.max())
    axis.set_xticks(range(len(CLASS_NAMES)), CLASS_NAMES, rotation=45, ha="right")
    axis.set_yticks(range(len(CLASS_NAMES)), CLASS_NAMES)
    axis.set_xlabel("predicted")
    axis.set_ylabel("actual")
    axis.set_title("Confusion matrix" + (" (row-normalised)" if normalize else ""))

    threshold = matrix.max() / 2.0
    for row in range(matrix.shape[0]):
        for column in range(matrix.shape[1]):
            value = matrix[row, column]
            axis.text(column, row, f"{value:.2f}" if normalize else f"{value:d}",
                      ha="center", va="center", fontsize=7,
                      color="white" if value > threshold else "black")

    figure.colorbar(image, ax=axis, fraction=0.046)
    figure.tight_layout()
    if save_path:
        figure.savefig(save_path, dpi=120, bbox_inches="tight")
    return figure


def plot_recommendations(query_images, query_labels, gallery_images, gallery_labels,
                         indices, similarities, save_path=None):
    """Show each query image beside the items recommended for it."""
    import matplotlib.pyplot as plt

    n_queries, k = indices.shape
    figure, axes = plt.subplots(n_queries, k + 1, figsize=(1.6 * (k + 1), 1.9 * n_queries))
    axes = np.atleast_2d(axes)

    for row in range(n_queries):
        axes[row, 0].imshow(query_images[row].squeeze(), cmap="gray")
        axes[row, 0].set_title(f"query\n{CLASS_NAMES[int(query_labels[row])]}",
                               fontsize=8, color="#1f4e79")
        axes[row, 0].set_xticks([])
        axes[row, 0].set_yticks([])
        for spine in axes[row, 0].spines.values():
            spine.set(color="#1f4e79", linewidth=2)

        for column in range(k):
            index = indices[row, column]
            axis = axes[row, column + 1]
            axis.imshow(gallery_images[index].squeeze(), cmap="gray")
            same = gallery_labels[index] == query_labels[row]
            axis.set_title(
                f"{CLASS_NAMES[int(gallery_labels[index])]}\n{similarities[row, column]:.3f}",
                fontsize=7, color="#2e7d32" if same else "#c62828",
            )
            axis.set_xticks([])
            axis.set_yticks([])

    figure.suptitle("Query (blue) and its top recommendations "
                    "— green = same category, red = different", fontsize=11)
    # Reserve a strip for the suptitle so it never lands on the first row's labels.
    figure.tight_layout(rect=(0, 0, 1, 1 - 0.45 / figure.get_figheight()))
    if save_path:
        figure.savefig(save_path, dpi=120, bbox_inches="tight")
    return figure


def plot_embedding_projection(embeddings, labels, save_path=None, sample_size=3000,
                              random_state=42):
    """Project embeddings to 2-D with PCA to show the learned class clusters."""
    import matplotlib.pyplot as plt
    from sklearn.decomposition import PCA

    rng = np.random.default_rng(random_state)
    labels = np.asarray(labels)
    sample_size = min(sample_size, len(embeddings))
    picks = rng.choice(len(embeddings), size=sample_size, replace=False)

    projected = PCA(n_components=2, random_state=random_state).fit_transform(
        l2_normalize(embeddings)[picks]
    )

    figure, axis = plt.subplots(figsize=(8, 6))
    for label in range(len(CLASS_NAMES)):
        mask = labels[picks] == label
        axis.scatter(projected[mask, 0], projected[mask, 1], s=6, alpha=0.6,
                     label=CLASS_NAMES[label])
    axis.set_title("PCA projection of the learned 128-D embedding space")
    axis.set_xlabel("component 1")
    axis.set_ylabel("component 2")
    axis.legend(markerscale=2, fontsize=8, loc="best")
    axis.grid(alpha=0.3)

    figure.tight_layout()
    if save_path:
        figure.savefig(save_path, dpi=120, bbox_inches="tight")
    return figure
