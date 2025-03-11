# 🎌 OtakuTag - Genre Prediction 🎌

OtakuTag is an AI-powered web application that predicts the genres of anime and manga based on their descriptions. Whether you're exploring new shows or want to know more about a manga, simply input a brief description, and OtakuTag will generate a list of genres associated with it.

---

## 📊 Features

- **Multi-label Genre Classification**: The model predicts multiple genres for a given anime/manga description.
- **Data Scraping**: Data is scraped from MyAnimeList to build a rich dataset for training the model.
- **Data Cleaning**: To ensure maximum utility of data.
- **Model Training**: We use `distil-roberta-base` for multi-label classification, incorporating:
  - **Weighted Binary Cross-Entropy Loss** for improved handling of imbalanced data.
  - **Threshold Tuning** to optimize for 13 distinct genres against F1 score for each.
  - **Stratified Sampling** to ensure a balanced dataset during model training.

---

## 🚀 How to Use

1. **Visit the Web App**: You can try out OtakuTag directly on Hugging Face Spaces:
   - [Otaku-Tag on Hugging Face](https://huggingface.co/spaces/soothsayer1221/Otaku-Tag/)

2. **Enter Description**: Simply type in a short description of an anime or manga.
   
3. **Get Predicted Genres**: Click the "Get Predicted Genres" button, and you'll receive a list of relevant genres like "Slice of Life, Drama, Comedy, Action", and more!

---

## 🧠 Model Details

- **Model**: `distil-roberta-base`
- **Loss Function**: Weighted Binary Cross-Entropy
- **Threshold Tuning**: Optimized for predicting 13 genres.
- **Sampling Strategy**: Stratified sampling to ensure a balanced dataset for training.

---

## 🌍 Live Demo

- **GitHub Webpage**: [Otaku-Tag GitHub Page](https://arian-rahman.github.io/Otaku-Tag/)

- **Hugging Face Space**: [Otaku-Tag on Hugging Face](https://huggingface.co/spaces/soothsayer1221/Otaku-Tag/)

---

## 🛠️ Technologies Used

- **Gradio**: For the interactive front-end interface.
- **Hugging Face Spaces**: For easy model deployment and integration.
- **Distil-Roberta-Base**: A transformer-based model for multi-label text classification.
- **Python**: The primary language used for the backend logic and model training.

---

## 💻 Installation

To run the project locally, you can follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/Otaku-Tag.git
   ```
2. Install Requirements:

   ```bash 
   pip install -r requirements.txt
   ```

3. Fetch Models from my Hugginface repo and paste under the models folder :

    --[Download Models From Here](https://huggingface.co/spaces/soothsayer1221/Otaku-Tag/tree/main/models)

4. Run the app.py :

   ```bash
   cd deployments
   python app.py
   ```

