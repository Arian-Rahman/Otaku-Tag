import torch 
import gradio as gr 
from transformers import AutoTokenizer,DistilBertForSequenceClassification,DistilBertTokenizerFast
import numpy as np 
from huggingface_hub import hf_hub_download
import os

os.chdir("..")
os.chdir("models")
mps_model_path = "distilroberta_model_with_thresholds.pth" 
cpu_model_path = "model_cpu.pth"
thresholds_path = "thresholds_tensor.pth"

device = torch.device("mps" if torch.backends.mps.is_available() else "cuda" if torch.cuda.is_available() else "cpu")
model = DistilBertForSequenceClassification.from_pretrained(
    "distilbert-base-uncased", 
    num_labels=13, 
    problem_type="multi_label_classification"
)

model.to(device)
if device=='mps':
    model.load_state_dict(torch.load(mps_model_path, map_location=device)['model_state_dict'])
else :
    model.load_state_dict(torch.load(cpu_model_path, map_location=device)['model_state_dict'])
model.eval()

tokenizer = DistilBertTokenizerFast.from_pretrained("distilbert-base-uncased")

thresholds_tensor = torch.load(thresholds_path, map_location=device, weights_only=True)
best_thresholds = thresholds_tensor.cpu().numpy()

GENRE_NAMES = ['Action', 'Adventure', 'Comedy', 'Drama', 'Fantasy', 'Horror', 'Mystery', 'Romance', 'Sci-Fi', 'Slice of Life', 'Sports', 'Supernatural', 'Suspense']


def predict_genres(description):
    """Processes the text input and returns predicted genres based on thresholds and sorted by confidence."""
    input = tokenizer(description, return_tensors="pt", padding=True, truncation=True)
    
    with torch.no_grad():
        logits = model(**input).logits
        probs = torch.sigmoid(logits).cpu().numpy()
        
    # Create a list of (genre, confidence_score) tuples
    genre_confidence = [(GENRE_NAMES[i], probs[0][i]) for i in range(len(GENRE_NAMES))]
    
    # Filter genres based on the threshold and sort by confidence
    genre_confidence = [(genre, confidence) for i, (genre, confidence) in enumerate(genre_confidence) if confidence >= best_thresholds[i]]
    genre_confidence.sort(key=lambda x: x[1], reverse=True)  # Sort by confidence descending
    genre_confidence = genre_confidence[:4]
    if genre_confidence:
        sorted_genres = ", ".join([genre for genre, _ in genre_confidence])
        return sorted_genres
    else:
        return "No strong genre detected"


interface = gr.Interface(
    fn=predict_genres,  
    inputs=gr.Textbox(
        lines=5, 
        placeholder="Paste an anime/manga description here...",
        label="Anime/Manga Description"
    ),  
    outputs=gr.Label(num_top_classes=4, label="Predicted Genres"),  
    title="🎌 Otaku Tag - AI Genre Predictor 🎌",
    description="🔹 Enter an **anime** or **manga** description, and AI will predict its **top genres**!\n\n"
                "💡 *Supports multi-label classification with confidence-based ranking!*",
    theme="soft",
    live=True,
)

interface.launch(share=True)