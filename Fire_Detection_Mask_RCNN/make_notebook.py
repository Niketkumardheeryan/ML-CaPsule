import nbformat as nbf

nb = nbf.v4.new_notebook()

nb.cells = [
    nbf.v4.new_markdown_cell(
        "# Image Segmentation using Mask R-CNN with TensorFlow for Fire Detection\n\n"
        "Fire is an abnormal event that can quickly cause significant injury and property damage in a very concise time frame. "
        "The best possible way to reduce the wreckage caused by fire is to detect the fire source as early as we can before it spreads.\n\n"
        "This notebook demonstrates end-to-end fire detection, localization, and image segmentation using **Mask R-CNN** built with TensorFlow/Keras and RGB chromatic analysis."
    ),
    nbf.v4.new_code_cell(
        "import os\n"
        "import numpy as np\n"
        "import cv2\n"
        "import matplotlib.pyplot as plt\n"
        "import tensorflow as tf\n"
        "from tensorflow.keras import layers, models\n\n"
        "print('TensorFlow Version:', tf.__version__)"
    ),
    nbf.v4.new_code_cell(
        "from model import generate_dataset, SimpleMaskRCNN, calculate_iou, detect_fire_rgb_heuristic\n\n"
        "# Generate synthetic fire dataset\n"
        "X_train, Y_mask, Y_bbox = generate_dataset(num_samples=150, img_size=(128, 128))\n"
        "print('Training Images Shape:', X_train.shape)\n"
        "print('Masks Shape:', Y_mask.shape)\n"
        "print('Bounding Boxes Shape:', Y_bbox.shape)"
    ),
    nbf.v4.new_code_cell(
        "# Instantiate Simple Mask R-CNN Model\n"
        "model = SimpleMaskRCNN(input_shape=(128, 128, 3))\n"
        "model.compile(optimizer='adam', loss={'bbox': 'mse', 'mask': 'binary_crossentropy'}, loss_weights={'bbox': 1.0, 'mask': 2.0})\n\n"
        "# Train model on synthetic fire dataset\n"
        "history = model.fit(X_train, {'bbox': Y_bbox, 'mask': Y_mask}, epochs=5, batch_size=16, validation_split=0.2)\n"
        "print('Training Complete!')"
    ),
    nbf.v4.new_code_cell(
        "# Evaluate IoU Metric\n"
        "X_test, Y_test_mask, Y_test_bbox = generate_dataset(num_samples=20, img_size=(128, 128))\n"
        "preds = model(X_test)\n"
        "pred_masks = preds['mask'].numpy()\n\n"
        "ious = [calculate_iou(Y_test_mask[i, :, :, 0], pred_masks[i, :, :, 0]) for i in range(len(X_test))]\n"
        "print(f'Mean Test IoU Score: {np.mean(ious):.4f}')"
    ),
    nbf.v4.new_code_cell(
        "# Plot Sample Predictions\n"
        "fig, axes = plt.subplots(1, 3, figsize=(15, 5))\n"
        "axes[0].imshow(X_test[0])\n"
        "axes[0].set_title('Input Image')\n"
        "axes[1].imshow(Y_test_mask[0, :, :, 0], cmap='gray')\n"
        "axes[1].set_title('Ground Truth Mask')\n"
        "axes[2].imshow(pred_masks[0, :, :, 0] > 0.5, cmap='gray')\n"
        "axes[2].set_title('Predicted Mask R-CNN Segmentation')\n"
        "plt.tight_layout()\n"
        "plt.savefig('sample_output.png')\n"
        "plt.show()"
    )
]

with open('Fire_Detection_Mask_RCNN/mask_rcnn_fire_segmentation.ipynb', 'w', encoding='utf-8') as f:
    nbf.write(nb, f)

print("Notebook generated successfully.")
