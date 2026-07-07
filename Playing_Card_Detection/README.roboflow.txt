
Playing Cards - v4 FASTmodel-resized640-aug3x
==============================

This dataset was exported via roboflow.com on March 7, 2023 at 7:04 PM GMT

Roboflow is an end-to-end computer vision platform that helps you
* collaborate with your team on computer vision projects
* collect & organize images
* understand and search unstructured image data
* annotate, and create datasets
* export, train, and deploy computer vision models
* use active learning to improve your dataset over time

For state of the art Computer Vision training notebooks you can use with this dataset,
visit https://github.com/roboflow/notebooks

To find over 100k other datasets and pre-trained models, visit https://universe.roboflow.com

The dataset includes 24240 images.
Cards are annotated in YOLOv8 format.

The following pre-processing was applied to each image:
* Auto-orientation of pixel data (with EXIF-orientation stripping)
* Resize to 640x640 (Stretch)

The following augmentation was applied to create 3 versions of each source image:
* 50% probability of horizontal flip
* 50% probability of vertical flip
* Equal probability of one of the following 90-degree rotations: none, clockwise, counter-clockwise, upside-down
* Randomly crop between 0 and 15 percent of the image
* Random rotation of between -10 and +10 degrees
* Random shear of between -2° to +2° horizontally and -2° to +2° vertically
* Random brigthness adjustment of between -25 and +25 percent
* Random exposure adjustment of between -15 and +15 percent
* Random Gaussian blur of between 0 and 1.75 pixels
* Salt and pepper noise was applied to 2 percent of pixels


