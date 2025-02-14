import pandas as pd
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

class OffensiveDetector:
    def __init__(self, model_name="Hate-speech-CNERG/bert-base-uncased-hatexplain", csv_path="list.csv"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_name)
        self.toxic_words = self._load_toxic_words(csv_path)

    def _load_toxic_words(self, csv_path):
        try:
            df = pd.read_csv(csv_path)
            if "Offensive_Word" not in df.columns:
                raise ValueError("CSV missing 'Offensive_Word' column")
            return set(df["Offensive_Word"].str.lower().dropna())
        except Exception as e:
            print(f"Error loading toxic words: {e}")
            return set()

    def detect(self, text):
        if not text.strip():
            return [], text
        offensive_words = [word for word in text.split() if word.lower() in self.toxic_words]
        highlighted = text
        for word in offensive_words:
            highlighted = highlighted.replace(word, f"**{word}**")
        return list(set(offensive_words)), highlighted
