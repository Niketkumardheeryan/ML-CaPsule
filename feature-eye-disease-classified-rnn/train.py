import argparse
import tensorflow as tf
from model import build_model
from data_preprocessing import prepare_dataset_from_dir, IMG_SIZE
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping


def main(args):
    train_ds, val_ds = prepare_dataset_from_dir(args.data_dir, batch_size=args.batch_size, img_size=IMG_SIZE)

    # infer number of classes from dataset
    for batch_x, batch_y in train_ds.take(1):
        num_classes = int(batch_y.shape[1])

    model = build_model(input_shape=(*IMG_SIZE, 3), num_classes=num_classes)
    model.compile(
        optimizer='adam',
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )

    callbacks = [
        ModelCheckpoint('best_model.h5', save_best_only=True, monitor='val_accuracy'),
        EarlyStopping(monitor='val_accuracy', patience=5, restore_best_weights=True)
    ]

    model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=args.epochs,
        callbacks=callbacks
    )

    results = model.evaluate(val_ds)
    print('Eval results:', results)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_dir', required=True, help='Path to data directory with train/ and val/ subfolders')
    parser.add_argument('--epochs', type=int, default=20)
    parser.add_argument('--batch_size', type=int, default=16)
    args = parser.parse_args()
    main(args)
