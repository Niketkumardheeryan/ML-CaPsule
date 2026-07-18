#!/bin/bash
# Compile ONNX models to Hailo HEF format for Raspberry Pi 5
# Requires: Hailo Dataflow Compiler (hailo_sdk_client)

set -e

MODELS_DIR="models"
CALIB_DIR="datasets/calibration"  # Optional calibration images

echo "============================================"
echo "  Hailo Model Compilation Script"
echo "============================================"
echo ""

# Check if Hailo compiler is installed
if ! command -v hailo &> /dev/null; then
    echo "❌ Error: Hailo compiler not found"
    echo "   Install Hailo SDK: https://hailo.ai/developer-zone/"
    exit 1
fi

echo "✅ Hailo compiler found"
echo ""

# 1. Compile CRNN OCR Model
echo "📦 Compiling CRNN OCR model..."
if [ -f "$MODELS_DIR/ocr_crnn.onnx" ]; then
    hailo compile \
        --onnx "$MODELS_DIR/ocr_crnn.onnx" \
        --output "$MODELS_DIR/ocr_crnn.hef" \
        --input-shape 1,32,100,1 \
        --output-shape 1,26,37 \
        --normalize mean=0.5 std=0.5 \
        --quantization int8 \
        --batch-size 1 \
        --hw-arch hailo8
    
    echo "✅ CRNN OCR compiled: $MODELS_DIR/ocr_crnn.hef"
else
    echo "⚠️  $MODELS_DIR/ocr_crnn.onnx not found, skipping OCR compilation"
    echo "   Export ONNX first: python tools/export_to_onnx.py"
fi

echo ""

# 2. Compile YOLOv8 Plate Detector
echo "📦 Compiling YOLOv8 plate detector..."
if [ -f "$MODELS_DIR/plate_yolov8.onnx" ]; then
    hailo compile \
        --onnx "$MODELS_DIR/plate_yolov8.onnx" \
        --output "$MODELS_DIR/plate_yolov8.hef" \
        --input-shape 1,3,512,512 \
        --yolo-version 8 \
        --quantization int8 \
        --batch-size 1 \
        --hw-arch hailo8
    
    echo "✅ YOLOv8 detector compiled: $MODELS_DIR/plate_yolov8.hef"
else
    echo "⚠️  $MODELS_DIR/plate_yolov8.onnx not found, skipping detector compilation"
fi

echo ""
echo "============================================"
echo "  Compilation Complete!"
echo "============================================"
echo ""
echo "Next steps:"
echo "1. Copy HEF files to Raspberry Pi 5:"
echo "   scp models/*.hef pi@raspberrypi.local:~/number-plate/models/"
echo ""
echo "2. Update config.yaml:"
echo "   inference:"
echo "     use_hailo: true"
echo "     device: hailo"
echo ""
echo "3. Run on Raspberry Pi:"
echo "   python -m src.multi_camera_infer"
