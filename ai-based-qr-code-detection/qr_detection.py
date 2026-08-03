import argparse
import cv2
from pyzbar import pyzbar


def detect_qr_codes_from_image(image_path):
    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError(f'Image not found: {image_path}')

    decoded_objects = pyzbar.decode(image)
    results = []
    for obj in decoded_objects:
        data = obj.data.decode('utf-8')
        results.append({
            'type': obj.type,
            'data': data,
            'rect': obj.rect,
        })
    return results


def scan_live_camera(camera_id=0):
    cap = cv2.VideoCapture(camera_id)
    if not cap.isOpened():
        raise RuntimeError('Camera could not be opened')

    print('Press q to exit')
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        decoded_objects = pyzbar.decode(frame)
        for obj in decoded_objects:
            text = obj.data.decode('utf-8')
            x, y, w, h = obj.rect
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            print('Detected QR data:', text)

        cv2.imshow('QR Scanner', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--image', help='Path to image containing a QR code')
    args = parser.parse_args()

    if args.image:
        results = detect_qr_codes_from_image(args.image)
        if not results:
            print('No QR code found.')
        for item in results:
            print(f"Type: {item['type']}")
            print(f"Data: {item['data']}")
            print(f"Rect: {item['rect']}")
    else:
        print('Provide --image or extend for live camera scanning.')
