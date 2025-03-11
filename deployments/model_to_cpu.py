import torch 
import gradio as gr 
from transformers import DistilBertForSequenceClassification
import numpy as np 

model_path = "models/distilroberta_model_with_thresholds.pth" 
thresholds_path = "models/thresholds_tensor.pth"
device = torch.device("mps" if torch.backends.mps.is_available() else "cuda" if torch.cuda.is_available() else "cpu")
 
 
model = DistilBertForSequenceClassification.from_pretrained(
    "distilbert-base-uncased", 
    num_labels=13, 
    problem_type="multi_label_classification"
)

model.to(device)
model.load_state_dict(torch.load(model_path, map_location=device)['model_state_dict'])

# Convert and save on CPU
model.to("cpu")
torch.save({"model_state_dict": model.state_dict()}, "models/model_cpu.pth")