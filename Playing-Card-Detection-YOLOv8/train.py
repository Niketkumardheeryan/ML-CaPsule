from ultralytics import YOLO

def main():
    model = YOLO("yolov8n.pt")  # nano model — fastest, good for real-time
    model.train(
        data="Playing-cards-10/data.yaml",
        epochs=50,
        imgsz=640,
        batch=16,
        name="playing_card_detector"
    )

if __name__ == "__main__":
    main()
