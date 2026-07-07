from ultralytics import YOLO

def main():
    """
    Main function to load the custom-trained YOLOv8 model
    and run real-time inference using the webcam.
    """
    # 1. Path to the trained model weights
    # Using raw string (r"") to handle Windows file paths correctly
    model_path = r"C:\Users\shiva\runs\detect\card_detector\weights\best.pt"
    
    # 2. Load the custom model
    print("[INFO] Loading custom YOLOv8 model...")
    model = YOLO(model_path)
    
    print("[INFO] Starting webcam for real-time card detection...")
    print("[INFO] Press 'q' in the camera window to stop the feed.")
    
    # 3. Run inference on the default webcam (source=0)
    # show=True: Displays the live camera feed with bounding boxes
    # conf=0.5: Confidence threshold (only shows detections >= 50% sure)
    results = model.predict(source=0, show=True, conf=0.5)

if __name__ == '__main__':
    main()