## Description:

This PR adds a dashboard that helps begginers understand about mixup and cutmix implementations from the scratch

### Tech Stack 
- streamlit
- torchvision
- numpy 
- pillow
- numpy

### Features:
- Will allow you to upload same size images and applies mixup & cutmix on them
- Provides scratch implementation for mixup and cutmix

### Setup:

- Install dependencies

```bash
pip install -r requirements.txt
```

- To run dashboard

```bash
streamlit run app.py
```
- Upload any two images of same size to simulate the augumentations!

### Future Improvements:

- Add training pipeline with these augumentations showing improvement in generalization