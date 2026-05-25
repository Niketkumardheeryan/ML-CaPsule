# Smart Parking Detection System 

An AI-powered parking detection system that uses YOLOv8 and OpenCV to identify available and occupied parking slots in real-time.

## Features
* Real-time vehicle detection using YOLOv8 (Nano)
* Custom Region of Interest (ROI) polygon mapping 
* Dynamic occupancy logic (Green = Available, Red = Occupied)

## How to Run
1. Install dependencies:
   `pip install -r requirements.txt`
2. Ensure you have a sample video named `parking_video.mp4` in the root directory.
3. Run the main script:
   `python main.py`