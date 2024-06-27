# AI Virtual Drag and Drop

This project uses OpenCV and cvzone's HandTrackingModule to create a virtual drag and drop interface. The program captures video from the webcam, detects hands, and allows the user to drag and drop an image using their index finger and thumb.

## Features
- Real-time hand detection using the webcam.
- Virtual drag and drop functionality for a specified image.
- Simple and intuitive interface.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/AI-Virtual-Drag-and-Drop.git
    cd AI-Virtual-Drag-and-Drop
    ```

2. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. Place the image you want to use (e.g., `gates.jpg`) in the same directory as the script.
2. Run the script:
    ```bash
    python drag_and_drop.py
    ```

## Requirements
- Python 3.x
- OpenCV
- cvzone

## How it works

The script captures video frames from the webcam and uses the HandTrackingModule from cvzone to detect hands. When the distance between the index finger and thumb is less than a certain threshold, the image can be dragged around the screen by moving the hand.


