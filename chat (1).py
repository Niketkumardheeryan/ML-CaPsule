from peft import AutoPeftModelForCausalLM
from transformers import GenerationConfig
from transformers import AutoTokenizer
import torch
tokenizer = AutoTokenizer.from_pretrained("Vasanth/mistral-finetuned-alpaca")

model = AutoPeftModelForCausalLM.from_pretrained(
    "Vasanth/mistral-finetuned-alpaca",
    low_cpu_mem_usage=True,
    return_dict=True,
    torch_dtype=torch.float16,
    device_map="cuda")

generation_config = GenerationConfig(
    do_sample=True,
    top_k=1,
    temperature=0.1,
    max_new_tokens=100,
    pad_token_id=tokenizer.eos_token_id
)

def chatbot(message):
    input_str = "###Human: " + message + " ###Assistant: "
    inputs = tokenizer(input_str, return_tensors="pt").to("cuda")
    outputs = model.generate(**inputs, generation_config=generation_config)
    return tokenizer.decode(outputs[0], skip_special_tokens=True).replace(input_str, '')