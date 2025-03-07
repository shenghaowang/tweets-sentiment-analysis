import nltk
import torch
from nltk.sentiment import SentimentIntensityAnalyzer
from sklearn.metrics.pairwise import cosine_similarity
from transformers import DistilBertModel, DistilBertTokenizer

nltk.download("vader_lexicon")


class TweetClassifier:
    def __init__(self):
        self.sia = SentimentIntensityAnalyzer()
        self.tokenizer = DistilBertTokenizer.from_pretrained("distilbert-base-uncased")
        self.model = DistilBertModel.from_pretrained("distilbert-base-uncased")

        self.high_risk_ref = self.get_embedding("I want to end my life")
        self.moderate_risk_ref = self.get_embedding("I feel lost and alone")
        self.low_risk_ref = self.get_embedding("Mental health is important")

    def classify_sentiment(self, text: str) -> str:
        compound = self.sia.polarity_scores(text)["compound"]
        if compound >= 0.05:
            return "Positive"

        elif compound <= -0.05:
            return "Negative"

        else:
            return "Neutral"

    def get_embedding(self, text: str) -> torch.Tensor:
        inputs = self.tokenizer(
            text, return_tensors="pt", truncation=True, padding=True
        )

        with torch.no_grad():
            outputs = self.model(**inputs)

        return outputs.last_hidden_state.mean(dim=1)

    def classify_risk(self, text: str) -> str:
        embedding = self.get_embedding(text)
        scores = {
            "High": cosine_similarity(embedding, self.high_risk_ref),
            "Moderate": cosine_similarity(embedding, self.moderate_risk_ref),
            "Low": cosine_similarity(embedding, self.low_risk_ref),
        }

        return max(scores, key=scores.get)
