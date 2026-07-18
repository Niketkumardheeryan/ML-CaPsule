# Deep-Fashion-Recommendation-system

A deep learning-based fashion recommendation system that suggests visually similar clothing items using CNN feature extraction (VGG16) and cosine similarity.

---

## Overview

This project builds a content-based image recommendation system for fashion products. Given an input image, the model analyzes its visual features and retrieves similar fashion items from the dataset.

It leverages a pre-trained VGG16 Convolutional Neural Network to extract meaningful image embeddings and compares them using similarity metrics.

---

## Key Features

* Image-based fashion recommendation
* Deep feature extraction using VGG16 (ImageNet pretrained)
* Similarity computation using cosine similarity
* Visual display of input and recommended items
* Feature and filename persistence using pickle

---

## Dataset

* Dataset: Women Fashion Images
* Format: `.jpg`, `.png`, `.jpeg`, `.webp`
* Extracted from a ZIP file stored in Google Drive
* Link: [Women Fashion Images (Google Drive)](https://drive.google.com/file/d/1KjHfcp8xjL1j-q5eJp8ucloQHhe7Xju7/view?usp=sharing)

⚠️ Dataset is not included due to size limitations.  
You can use any fashion dataset from Kaggle.

---

## Tech Stack

* Python
* TensorFlow / Keras
* NumPy
* Matplotlib
* PIL (Python Imaging Library)
* SciPy
* pickle (Python standard library)

---

## Project Workflow

1. Data Extraction

   * Unzip dataset from Google Drive
   * Load and explore image files

2. Preprocessing

   * Resize images to 224x224
   * Normalize using VGG16 preprocessing

3. Feature Extraction

   * Use VGG16 (without top layer)
   * Flatten and normalize feature vectors

4. Similarity Calculation

   * Compute cosine similarity between images

5. Recommendation

   * Retrieve top-N similar images
   * Display results visually

---

## How to Run

### 1. Clone the Repository
Clone this repository and navigate to the project directory:
 git clone [<REPO_URL>](https://github.com/Niketkumardheeryan/ML-CaPsule)
 cd ML-CaPsule/Deep-Fashion-Recommendation-system

### 2. Install Dependencies

```bash
pip install tensorflow numpy matplotlib pillow scipy
```

### 3. Run the Notebook

Open the `.ipynb` file using:

* Google Colab
* Jupyter Notebook

---

## Usage

Provide the path of an input image:

```python
input_image_path = "path/to/image.jpg"

recommend_fashion_items_cnn(
    input_image_path,
    all_features,
    all_image_names,
    model,
    top_n=5
)
```

Output:

* Displays the input image and top-N visually similar fashion items

---

## Saving Features

To avoid recomputation:

```python
import pickle

pickle.dump(all_features, open('features.pkl', 'wb'))
pickle.dump(all_image_names, open('filenames.pkl', 'wb'))
```

---

## Example Output

### Input: Anarkali suit
<img width="356" height="475" alt="image" src="https://github.com/user-attachments/assets/8fd02a36-c7f6-4e6e-9478-4e12568c2704" />


### Output: Similar ethnic wear recommendations based on design, color, and texture
<img width="677" height="458" alt="image" src="https://github.com/user-attachments/assets/9f7107ab-a567-4157-8fd6-e0569c6846da" />
<img width="685" height="550" alt="image" src="https://github.com/user-attachments/assets/a59fbf59-e7f3-4f7f-a261-640ef715ea69" />

---

## Future Improvements

* Use advanced models like ResNet or EfficientNet
* Add FAISS or Annoy for faster similarity search
* Deploy as a web application using Streamlit or Flask
* Add user personalization
* Integrate text and image-based hybrid recommendations

---

## Contributing

Contributions are welcome:

1. Fork the repository
2. Create a new branch
3. Make your changes
4. Submit a Pull Request

---

## License

This project is open-source and available under the MIT License.

---

## Author

Saloni Pandagale
**(Deep Learning and AI Enthusiast)**
