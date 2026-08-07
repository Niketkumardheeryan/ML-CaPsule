"""
Train and save MobileNetV2 Cat vs Dog classification model
"""
import os
import numpy as np
import pathlib
import tensorflow as tf
from tensorflow.keras import layers
from PIL import Image
import warnings
warnings.filterwarnings('ignore')

# Config
DATA_DIR = "kagglecatsanddogs/PetImages"
IMG_SIZE = (160, 160)
BATCH_SIZE = 64
EPOCHS = 5
MODEL_PATH = "pet_classifier.keras"

AUTOTUNE = tf.data.AUTOTUNE


def clean_folder(folder_path):
    """Remove corrupt images from folder"""
    for file in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file)
        if not os.path.isfile(file_path):
            continue
        try:
            Image.open(file_path).verify()
        except Exception:
            os.remove(file_path)
    print(f"Corrupt images removed from {folder_path} ✅")


def load_datasets():
    """Load training and validation datasets"""
    train_ds = tf.keras.utils.image_dataset_from_directory(
        DATA_DIR,
        validation_split=0.2,
        subset="training",
        seed=123,
        image_size=IMG_SIZE,
        batch_size=BATCH_SIZE
    )

    val_ds = tf.keras.utils.image_dataset_from_directory(
        DATA_DIR,
        validation_split=0.2,
        subset="validation",
        seed=123,
        image_size=IMG_SIZE,
        batch_size=BATCH_SIZE
    )

    class_names = train_ds.class_names
    print("Classes:", class_names)
    return train_ds, val_ds, class_names


def preprocess_dataset(ds):
    """Apply MobileNetV2 preprocessing and optimize dataset pipeline"""
    return ds.map(
        lambda x, y: (tf.keras.applications.mobilenet_v2.preprocess_input(x), y),
        num_parallel_calls=AUTOTUNE
    ).shuffle(1000).cache().prefetch(AUTOTUNE)


def build_model(num_classes):
    """Build MobileNetV2 transfer learning model"""
    base_model = tf.keras.applications.MobileNetV2(
        input_shape=(160, 160, 3),
        include_top=False,
        weights="imagenet"
    )
    base_model.trainable = False

    inputs = layers.Input(shape=(160, 160, 3))
    x = tf.keras.applications.mobilenet_v2.preprocess_input(inputs)
    x = base_model(x, training=False)
    x = layers.GlobalAveragePooling2D()(x)
    x = layers.Dropout(0.2)(x)
    outputs = layers.Dense(num_classes, activation="softmax")(x)

    model = tf.keras.Model(inputs, outputs)
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=1e-3),
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"]
    )
    return model


def train_with_fallback(model, train_ds, val_ds, epochs):
    """Train model with fallback for corrupt images"""
    callbacks = [
        tf.keras.callbacks.EarlyStopping(
            monitor="val_accuracy",
            patience=2,
            restore_best_weights=True
        )
    ]

    try:
        history = model.fit(
            train_ds,
            validation_data=val_ds,
            epochs=epochs,
            callbacks=callbacks
        )
        return history
    except tf.errors.InvalidArgumentError:
        print("⚠️ Corrupt images detected, rebuilding dataset with PIL...")
        return train_with_pil_fallback(model, train_ds, val_ds, epochs, callbacks)


def train_with_pil_fallback(model, train_ds, val_ds, epochs, callbacks):
    """Rebuild dataset using PIL to handle corrupt images"""
    data_root = pathlib.Path(DATA_DIR)
    classes = sorted([d.name for d in data_root.iterdir() if d.is_dir()])

    file_paths = []
    labels = []
    for idx, cname in enumerate(classes):
        for p in (data_root / cname).glob('*'):
            file_paths.append(str(p))
            labels.append(idx)

    file_paths = np.array(file_paths)
    labels = np.array(labels)
    rng = np.random.default_rng(123)
    idxs = rng.permutation(len(file_paths))
    file_paths = file_paths[idxs]
    labels = labels[idxs]

    split = int(0.8 * len(file_paths))
    train_fp, val_fp = file_paths[:split], file_paths[split:]
    train_lab, val_lab = labels[:split], labels[split:]

    def make_ds(fpaths, labs):
        ds = tf.data.Dataset.from_tensor_slices((fpaths, labs))

        def _load(path, label):
            path = path.numpy().decode("utf-8")
            label = label.numpy()
            img = Image.open(path).convert("RGB").resize(IMG_SIZE)
            arr = np.array(img)
            arr = tf.keras.applications.mobilenet_v2.preprocess_input(arr)
            return arr.astype(np.float32), np.int32(label)

        def _tf_load(path, label):
            img, lab = tf.py_function(_load, [path, label], [tf.float32, tf.int32])
            img.set_shape((IMG_SIZE[0], IMG_SIZE[1], 3))
            lab.set_shape(())
            return img, lab

        ds = ds.map(_tf_load, num_parallel_calls=AUTOTUNE)
        ds = ds.batch(BATCH_SIZE).shuffle(1000).cache().prefetch(AUTOTUNE)
        return ds

    train_ds = make_ds(train_fp, train_lab)
    val_ds = make_ds(val_fp, val_lab)

    history = model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=epochs,
        callbacks=callbacks
    )
    return history


def main():
    print("🐱🐶 Cat vs Dog Classifier Training")
    print("=" * 50)

    # Clean corrupt images
    print("🧹 Cleaning corrupt images...")
    clean_folder(os.path.join(DATA_DIR, "Cat"))
    clean_folder(os.path.join(DATA_DIR, "Dog"))

    # Load datasets
    print("📂 Loading datasets...")
    train_ds, val_ds, class_names = load_datasets()

    # Preprocess
    print("⚙️ Preprocessing datasets...")
    train_ds = preprocess_dataset(train_ds)
    val_ds = preprocess_dataset(val_ds)

    # Build model
    print("🏗️ Building MobileNetV2 model...")
    model = build_model(len(class_names))
    model.summary()

    # Train
    print(f"🚀 Training for {EPOCHS} epochs...")
    history = train_with_fallback(model, train_ds, val_ds, EPOCHS)

    # Save model
    print(f"💾 Saving model to {MODEL_PATH}...")
    model.save(MODEL_PATH)

    # Save class names
    import json
    with open("class_names.json", "w") as f:
        json.dump(class_names, f)

    print("✅ Training complete!")
    print(f"Model saved to: {MODEL_PATH}")
    print(f"Class names saved to: class_names.json")

    if history:
        print(f"\nFinal Training Accuracy: {history.history['accuracy'][-1]:.4f}")
        print(f"Final Validation Accuracy: {history.history['val_accuracy'][-1]:.4f}")


if __name__ == "__main__":
    main()