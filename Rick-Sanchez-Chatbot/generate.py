from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

print("Loading trained model...")

# Load trained model
tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-small")
model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-small")

print("Chatbot ready!")

# Chat loop
while True:

    user_input = input("You: ")

    if user_input.lower() == "exit":
        break

    input_ids = tokenizer.encode(
        user_input + tokenizer.eos_token,
        return_tensors="pt"
    )

    output = model.generate(
        input_ids,
        max_new_tokens=40,
        pad_token_id=tokenizer.eos_token_id,
        do_sample=False
    )

    response = tokenizer.decode(
        output[:, input_ids.shape[-1]:][0],
        skip_special_tokens=True
    )

    print("Rick:", response)