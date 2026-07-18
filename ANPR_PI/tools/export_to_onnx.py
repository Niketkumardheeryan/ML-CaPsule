import argparse
import os
import torch

try:
    from ultralytics import YOLO
except Exception:
    YOLO = None


def export_detector(det_pt: str, det_onnx: str, imgsz: int = 640):
    if YOLO is None:
        raise RuntimeError("Ultralytics not installed")
    model = YOLO(det_pt)
    model.fuse()
    model.export(format="onnx", imgsz=imgsz, opset=12, dynamic=True, optimize=True, simplify=True)
    # Ultralytics writes to default path; move if needed
    if os.path.exists("yolov8n.onnx") and det_onnx:
        os.replace("yolov8n.onnx", det_onnx)


def export_ocr(ocr_pt: str, ocr_onnx: str):
    # Placeholder: expects a scripted torch module that accepts (N,1,32,160) and returns (text, conf)
    # For real CRNN/PARSeq, replace with the correct export function.
    model = torch.jit.load(ocr_pt)
    model.eval()
    dummy = torch.randn(1, 1, 32, 160)
    torch.onnx.export(model, dummy, ocr_onnx, input_names=["input"], output_names=["text", "confidence"], opset_version=12, dynamic_axes={"input": {0: "batch"}})


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--detector", type=str, default=None)
    ap.add_argument("--detector_out", type=str, default="models/plate_yolov8.onnx")
    ap.add_argument("--ocr", type=str, default=None)
    ap.add_argument("--ocr_out", type=str, default="models/ocr_crnn.onnx")
    ap.add_argument("--imgsz", type=int, default=640)
    args = ap.parse_args()

    if args.detector:
        export_detector(args.detector, args.detector_out, imgsz=args.imgsz)
    if args.ocr:
        export_ocr(args.ocr, args.ocr_out)


if __name__ == "__main__":
    main()


