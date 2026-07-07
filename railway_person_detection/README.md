# Railway Person Detection using YOLOv8

This project aims to detect people in railway environments using YOLOv8, a state-of-the-art object detection model. The system can be deployed for real-time monitoring of railway stations, platforms, or tracks to ensure safety and security.

## Requirements

- Python 3.x
- OpenCV
- PyTorch
- Ultralytics YOLO library
- Pre-trained YOLOv8 model weights (`yolov8m.pt`)
- GPU (optional, for faster inference)

## Installation

1. Clone this repository:
    ```bash
    git clone https://github.com/TAHIR0110/ThereForYou.git
    cd THEREFORYOU
    cd railway_person_detection
    ```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```


## Usage

Run the `railway_person_detection.py` script to start detecting people in railway environments. You can specify various command-line arguments to customize the detection process:

- `-s, --source`: Specify the video source (default is webcam, provide the path to a video file for offline detection).
- `-x`: X-coordinate of the bounding box.
- `-y`: Y-coordinate of the bounding box.
- `--height`: Height of the bounding box.
- `--width`: Width of the bounding box.

Example usage:
```bash
python railway_person_detection.py --source 0 -x 100 -y 100 --height 200 --width 200
