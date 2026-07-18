# Virtual Drag and Drop Using OpenCV

Simple demo that implements a virtual drag-and-drop interface using computer vision.

Files
- `virtualDragDrop.py` — main script. Uses the webcam to detect hand/finger position and simulate dragging visual objects on screen.

Quick start

```bash
pip install opencv-python numpy
python virtualDragDrop.py
```

Notes
- The script expects a webcam and may require tuning thresholds for your lighting conditions.
- Inspect the code to change object shapes or detection parameters.
