import streamlit as st
import random
import PIL.Image as Image
import numpy as np
from torchvision.transforms import ToTensor, ToPILImage 

#helper functions

def mixup_augmentation(image1, image2, alpha=0.2):
    """Applies Mixup augmentation to two images."""
    lam = random.betavariate(alpha, alpha)
    mixed_image = lam * image1 + (1 - lam) * image2
    return mixed_image

def cutmix_augmentation(image1, image2, alpha=0.2):
    """Applies CutMix augmentation to two images."""
    lam = random.betavariate(alpha, alpha)
    h, w, _ = image1.shape
    cut_rat = np.sqrt(1. - lam)
    cut_w = int(w * cut_rat)
    cut_h = int(h * cut_rat)

    # Randomly choose the position for the cut
    cx = np.random.randint(w)
    cy = np.random.randint(h)

    x1 = np.clip(cx - cut_w // 2, 0, w)
    y1 = np.clip(cy - cut_h // 2, 0, h)
    x2 = np.clip(cx + cut_w // 2, 0, w)
    y2 = np.clip(cy + cut_h // 2, 0, h)

    mixed_image = image1.copy()
    mixed_image[y1:y2, x1:x2] = image2[y1:y2, x1:x2]
    
    return mixed_image

#page confihuration
st.set_page_config(
    page_title="Mixup & Cutmix Dashboard",
    layout = "wide",
    menu_items={
        'Get Help': 'https://github.com/your-repo-link'
    }   
)

st.header("Mixup & Cutmix Dashboard" , divider= True)


mixup , cutmix = st.tabs(["Mixup", "Cutmix"])

with mixup:
    st.header("Mixup")
    st.write("Mixup is a data augmentation technique that creates new training samples by combining pairs of examples and their labels. It helps improve model generalization and robustness.")

    uploaded_files = st.file_uploader("Upload two images for Mixup augmentation", type=["jpg", "jpeg", "png"], key="mixup_uploader" ,accept_multiple_files=True)

    if uploaded_files is not None:
        if len(uploaded_files) != 2:
            st.warning("Please upload exactly two images to see the Mixup augmentation.")
        else:
            image1 = Image.open(uploaded_files[0]).convert("RGB")
            image2 = Image.open(uploaded_files[1]).convert("RGB")

            # Convert images to numpy arrays
            image1_np = np.array(image1)
            image2_np = np.array(image2)

            mixed_image_np = mixup_augmentation(image1_np, image2_np)

            # Convert back to PIL Image for display
            mixed_image = Image.fromarray(np.uint8(mixed_image_np))

            cols = st.columns(3)

            cols[0].image(image1, caption="Image 1", width="content")
            cols[1].image(image2, caption="Image 2", width="content")
            cols[2].image(mixed_image, caption="Mixed Image", width="content")

with cutmix:
    st.header("Cutmix")
    st.write("CutMix is a data augmentation technique that combines two images by cutting a patch from one image and pasting it onto another. It helps improve model generalization and robustness.")

    uploaded_files = st.file_uploader("Upload two images for CutMix augmentation", type=["jpg", "jpeg", "png"], key="cutmix_uploader" , accept_multiple_files=True)

    if uploaded_files is not None and len(uploaded_files) == 2:
        image1 = Image.open(uploaded_files[0]).convert("RGB")
        image2 = Image.open(uploaded_files[1]).convert("RGB")

        # Convert images to numpy arrays
        image1_np = np.array(image1)
        image2_np = np.array(image2)

        mixed_image_np = cutmix_augmentation(image1_np, image2_np)

        # Convert back to PIL Image for display
        mixed_image = Image.fromarray(np.uint8(mixed_image_np))

        cols = st.columns(3)

        cols[0].image(image1, caption="Image 1", width = "content")
        cols[1].image(image2, caption="Image 2", width= "content")
        cols[2].image(mixed_image, caption="CutMix Image", width= "content")
    else:
        st.info("Please upload exactly two images to see the CutMix augmentation.")

