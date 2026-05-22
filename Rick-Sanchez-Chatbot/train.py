from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    Trainer,
    TrainingArguments,
    DataCollatorForLanguageModeling
)

from datasets import load_dataset

print("Loading tokenizer...")

# Load tokenizer
tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-small")

print("Loading model...")

# Load model
model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-small")

# Set padding token
tokenizer.pad_token = tokenizer.eos_token

print("Loading dataset...")

# Load text dataset
dataset = load_dataset(
    "text",
    data_files={"train": "/content/processed.txt"}
)

print("Tokenizing dataset...")

# Tokenization function
def tokenize_function(examples):
    return tokenizer(
        examples["text"],
        truncation=True,
        padding="max_length",
        max_length=128
    )

# Tokenize dataset
tokenized_dataset = dataset.map(
    tokenize_function,
    batched=True
)

print("Preparing data collator...")

# Data collator
data_collator = DataCollatorForLanguageModeling(
    tokenizer=tokenizer,
    mlm=False
)

print("Setting training arguments...")

# Training arguments
training_args = TrainingArguments(
    output_dir="./model",
    num_train_epochs=1,
    per_device_train_batch_size=2,
    logging_steps=10
)

print("Initializing trainer...")

# Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset["train"],
    data_collator=data_collator
)

print("Starting training...")

# Train model
trainer.train()

print("Saving model...")

# Save model
trainer.save_model("./model")

print("Training complete!")