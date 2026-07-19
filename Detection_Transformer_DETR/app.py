import torch
import torchvision.transforms as T
from PIL import Image, ImageDraw
import gradio as gr

# COCO class labels
CLASSES = [
    "N/A",
    "person",
    "bicycle",
    "car",
    "motorcycle",
    "airplane",
    "bus",
    "train",
    "truck",
    "boat",
    "traffic light",
    "fire hydrant",
    "N/A",
    "stop sign",
    "parking meter",
    "bench",
    "bird",
    "cat",
    "dog",
    "horse",
    "sheep",
    "cow",
    "elephant",
    "bear",
    "zebra",
    "giraffe",
    "N/A",
    "backpack",
    "umbrella",
    "N/A",
    "N/A",
    "handbag",
    "tie",
    "suitcase",
    "frisbee",
    "skis",
    "snowboard",
    "sports ball",
    "kite",
    "baseball bat",
    "baseball glove",
    "skateboard",
    "surfboard",
    "tennis racket",
    "bottle",
    "N/A",
    "wine glass",
    "cup",
    "fork",
    "knife",
    "spoon",
    "bowl",
    "banana",
    "apple",
    "sandwich",
    "orange",
    "broccoli",
    "carrot",
    "hot dog",
    "pizza",
    "donut",
    "cake",
    "chair",
    "couch",
    "potted plant",
    "bed",
    "N/A",
    "dining table",
    "N/A",
    "N/A",
    "toilet",
    "N/A",
    "tv",
    "laptop",
    "mouse",
    "remote",
    "keyboard",
    "cell phone",
    "microwave",
    "oven",
    "toaster",
    "sink",
    "refrigerator",
    "N/A",
    "book",
    "clock",
    "vase",
    "scissors",
    "teddy bear",
    "hair drier",
    "toothbrush",
]

# Load model once at startup
print("Loading DETR model...")
model = torch.hub.load("facebookresearch/detr", "detr_resnet50", pretrained=True)
model.eval()
print("Model loaded!")

# Image transforms
transform = T.Compose(
    [
        T.Resize(800),
        T.ToTensor(),
        T.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
    ]
)


def box_cxcywh_to_xyxy(x):
    x_c, y_c, w, h = x.unbind(1)
    b = [(x_c - 0.5 * w), (y_c - 0.5 * h), (x_c + 0.5 * w), (y_c + 0.5 * h)]
    return torch.stack(b, dim=1)


def rescale_bboxes(out_bbox, size):
    img_w, img_h = size
    b = box_cxcywh_to_xyxy(out_bbox)
    b = b * torch.tensor([img_w, img_h, img_w, img_h], dtype=torch.float32)
    return b


def detect_objects(image, threshold):
    """Run DETR inference and return annotated image + detection summary."""

    img_tensor = transform(image).unsqueeze(0)

    with torch.no_grad():
        outputs = model(img_tensor)

    probas = outputs["pred_logits"].softmax(-1)[0, :, :-1]
    keep = probas.max(-1).values > threshold

    if keep.sum() == 0:
        return image, "No objects detected. Try lowering the confidence threshold."

    bboxes = rescale_bboxes(outputs["pred_boxes"][0, keep], image.size)
    probs = probas[keep]

    # Draw boxes
    draw = ImageDraw.Draw(image)
    colors = [
        "#FF6B6B",
        "#4ECDC4",
        "#45B7D1",
        "#96CEB4",
        "#FFEAA7",
        "#DDA0DD",
        "#98D8C8",
        "#F7DC6F",
        "#BB8FCE",
        "#85C1E9",
    ]

    detections = []
    for i, (box, p) in enumerate(zip(bboxes, probs)):
        cl = p.argmax().item()
        score = p[cl].item()
        label = CLASSES[cl]
        color = colors[i % len(colors)]

        x0, y0, x1, y1 = box.tolist()

        # Draw bounding box
        draw.rectangle([x0, y0, x1, y1], outline=color, width=3)

        # Draw label background
        draw.rectangle([x0, y0 - 20, x0 + len(label) * 8 + 55, y0], fill=color)

        # Draw label text
        draw.text((x0 + 4, y0 - 18), f"{label} {score:.0%}", fill="white")

        detections.append(f"✅ {label}: {score:.1%}")

    summary = f"### Detected {len(detections)} object(s):\n" + "\n".join(detections)
    return image, summary


# Gradio UI
with gr.Blocks(title="DETR Object Detection") as demo:

    gr.Markdown("""
        # 🔍 DETR Object Detection
        **DEtection TRansformer** by Facebook AI Research  
        Upload any image to detect objects using a pretrained DETR (ResNet-50) model trained on COCO 2017.
        """)

    with gr.Row():
        with gr.Column():
            input_image = gr.Image(type="pil", label="Upload Image")
            threshold = gr.Slider(
                minimum=0.3,
                maximum=0.99,
                value=0.7,
                step=0.05,
                label="Confidence Threshold",
            )
            detect_btn = gr.Button("Detect Objects 🚀", variant="primary")

        with gr.Column():
            output_image = gr.Image(type="pil", label="Detection Result")
            output_text = gr.Markdown(label="Detections")

    detect_btn.click(
        fn=detect_objects,
        inputs=[input_image, threshold],
        outputs=[output_image, output_text],
    )

    gr.Markdown("""
        ---
        **Model Details:** ResNet-50 backbone | 6 Encoder + 6 Decoder layers | 
        100 object queries | Trained on COCO 2017 (91 classes)  
        **Paper:** [End-to-End Object Detection with Transformers (Carion et al., 2020)](https://arxiv.org/abs/2005.12872)
        """)

if __name__ == "__main__":
    demo.launch()
