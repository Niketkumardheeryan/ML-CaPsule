from ultralytics import YOLO
import cv2
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-s","--source",default=0)
parser.add_argument("-x", default=0)
parser.add_argument("-y", default=0)
parser.add_argument("--height",default=0)
parser.add_argument("--width",default=0)


args = parser.parse_args()


cap = cv2.VideoCapture(args.source)

model= YOLO("yolov8m.pt")



while (cap.isOpened()):



    suc,frame = cap.read()
    if(args.x == 0 and args.y == 0 and args.height == 0 and args.width == 0):
        print("User did not mentioned the values for the bounding box, by default, analyzing the whole image")
    else:

        frame = frame[args.y:args.y + args.height, args.x:args.x+args.width]


    if not suc:
        print("video sequence ended.")
        break

    result = model.predict(source=frame,classes=[0])

    if result[0].boxes.xyxy is not None:
        print("alert Person Detected in the Frame.")

    else:
        print("clear for now.")

    