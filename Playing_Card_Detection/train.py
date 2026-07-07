from ultralytics import YOLO
import os

def main():
    """
    Main function to initialize and train the YOLOv8 model 
    on the custom playing cards dataset.
    """
    # 1. Path to the dataset configuration file
    # Ensure data.yaml is in the exact same directory as this script
    data_config_path = "data.yaml"
    
    # 2. Load the pre-trained YOLOv8 Nano model
    # The 'nano' (n) version is chosen because it is incredibly fast 
    # and highly suitable for real-time webcam inference.
    print("[INFO] Loading YOLOv8 Nano model...")
    model = YOLO("yolov8n.pt") 
    
    print("[INFO] Starting the training process...")
    print("[WARNING] Your laptop fans might spin up, and the process will take some time. This is completely normal!")
    
    # 3. Train the model on our custom dataset
    # epochs=5: The model will iterate over the entire dataset 5 times.
    # imgsz=640: Standard image size for YOLO models.
    # batch=16: Feeds 16 images at a time to the CPU/GPU.
    # name="card_detector": The final trained model will be saved in the 'runs' folder under this name.
    results = model.train(
        data=data_config_path,
        epochs=5,
        imgsz=640,
        batch=16,
        name="card_detector"
    )
    
    print("[SUCCESS] Training successfully completed!")

# This if-statement is strictly required for Windows systems 
# to prevent freezing and crash loops during PyTorch multiprocessing.
if __name__ == '__main__':
    main()