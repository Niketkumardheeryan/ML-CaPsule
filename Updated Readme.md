Simplifying Medicine: Developing an Accessible Health Information Platform #880

Problem description - Not everyone is familiar with all diseases and the medical terminology used by professionals. Therefore, an interface should be created to address this issue.

Solution - To develop an LLM model trained on a dataset encompassing various medical terms and diseases, the fundamental concept is for users to inquire about specific diseases and receive relevant, accurate responses. I aim to leverage a pre-trained model, such as LLaMA 2, using Hugging Face

##Dataset
DS from huggingface : https://huggingface.co/datasets/gamino/wiki_medical_terms

##Libraries Involved: 

torch
accelerate==0.21.0 
peft==0.4.0 
bitsandbytes==0.40.2 
transformers==4.31.0 
trl==0.4.7 
gradio 

## Steps Involved: 

### Step 1: Installing and importing the libraries

## Step 2: Loading the model
pretrained model used - aboonaji/llama2finetune-v2

## Step 3: Loading the tokenizer
Leveraging AutoTokenizer.from_pretrained for the pretrained model used - aboonaji/llama2finetune-v2

## Step 4: Setting the training arguments

## Step 5: Creating the Supervised Fine-Tuning trainer
Leveraging SFTTrainer

## Step 6: Model Training

## Step 7: Model Testing

## Step 8: User Interface
Leveraging Gradio ui
