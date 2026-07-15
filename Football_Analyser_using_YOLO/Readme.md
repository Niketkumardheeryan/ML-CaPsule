
# Football Player Detection and Monitoring System Using YOLO

Welcome to the Football Player Detection and Monitoring System! This project is an industry-level endeavor aimed at providing precise detection and monitoring capabilities for football players, referees, and the ball using state-of-the-art YOLO models and various utility libraries.

![Demo](https://github.com/chiragHimself/FootballAnalyserYolo/blob/main/demo/demo1.jpg)

## Features

- **Player Tracking**: Track individual players with high precision.
- **Team Separation**: Distinguish between players from different teams.
- **Camera Movement Tracking**: Monitor camera movements for enhanced analysis.
- **Distance and Speed Monitoring**: Calculate distance covered by players and their speed during movement.
- **Ball Tracking**: Accurately trace the movement of the ball.
- **Team Possession Analysis**: Analyze team possession based on player movements.

## Prerequisites

- **Python 3.9 – 3.11** (required for PyTorch / YOLO compatibility)
- **pip** (Python package manager, ships with Python)
- **Git** (to clone the repository)
- A GPU with CUDA support is recommended for faster inference, but the project works on CPU as well.

## Environment Setup & Installation

Follow the steps below to set up the project in a **clean virtual environment**.

### 1. Clone the Repository

```bash
git clone https://github.com/chiragHimself/FootballAnalyserYolo.git
cd FootballAnalyserYolo/Football_Analyser_using_YOLO
```

### 2. Create and Activate a Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

All required packages and their compatible version ranges are listed in `requirements.txt`.

```bash
pip install -r requirements.txt
```

> **Note:** The `ultralytics` package automatically installs PyTorch (`torch`) as a dependency. If you need a specific CUDA version of PyTorch, install it **before** running the command above by following the [official PyTorch installation guide](https://pytorch.org/get-started/locally/).

### 4. Add Model Weights

Place your trained YOLO model weights (`.pt` file) inside the `models/` directory. The default expected path in `main.py` is `models/newBest100.pt`. Update the path in `main.py` if your model file has a different name.

### 5. Add Input Video

Place your input video file inside the `input_videos/` directory. The default expected path in `main.py` is `input_videos/08fd33_4.mp4`. Update the path in `main.py` if your video file has a different name.

## Dependencies

| Package | Purpose |
|---|---|
| `ultralytics` | YOLOv8 model loading, inference, and object detection |
| `supervision` | Detection result handling and annotation utilities |
| `opencv-python` | Video I/O, image processing, and drawing |
| `numpy` | Numerical operations and array manipulation |
| `pandas` | Data manipulation for track interpolation |
| `scikit-learn` | KMeans clustering for team color assignment |
| `matplotlib` | Plotting and visualization |

## Folder Structure

- **`camera_movement_estimator/`** — Camera motion estimation and position adjustment.
- **`development_and_analysis/`** — Notebooks for development and experimentation.
- **`input_videos/`** — Place input video files here.
- **`models/`** — YOLO model weights (`.pt` files).
- **`output_videos/`** — Generated output videos are saved here.
- **`player_ball_assigner/`** — Logic for assigning ball possession to players.
- **`speed_and_distance_estimator/`** — Player speed and distance calculations.
- **`stubs/`** — Cached tracking/estimation data (pickle stubs).
- **`team_assigner/`** — Team color assignment via KMeans clustering.
- **`trackers/`** — YOLO-based object tracker.
- **`training/`** — Training notebooks for the YOLO model.
- **`utils/`** — Utility functions (video I/O, bounding box helpers).
- **`view_transformer/`** — Perspective transformation for real-world coordinate mapping.

## Usage

1. Complete the [Environment Setup & Installation](#environment-setup--installation) steps above.
2. Configure the system by modifying parameters in the scripts if needed (e.g., model path, video path).
3. Run the main script:
   ```bash
   python main.py
   ```
4. View the output generated in the `output_videos/` folder.

## Demo

![Demo](https://github.com/chiragHimself/FootballAnalyserYolo/blob/main/demo/demo2.jpg)

## Contribution

Contributions are welcome! Feel free to submit issues, feature requests, or pull requests to improve the system.
