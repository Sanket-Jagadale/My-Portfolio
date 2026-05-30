import json
import random
import re
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Load knowledge base
BASE_DIR = Path(__file__).resolve().parent
with open(BASE_DIR / 'knowledge_base.json', 'r', encoding='utf-8') as file:
    knowledge_base = json.load(file)

# ---- Text Preprocessing ----
def preprocess(text):
    text = text.lower().strip()
    text = re.sub(r"[^\w\s]", "", text)   # remove punctuation
    text = re.sub(r"\s+", " ", text)       # collapse spaces
    return text

# Prepare training data
corpus = []
tags = []
for intent in knowledge_base['intents']:
    for pattern in intent.get('patterns', []):
        corpus.append(preprocess(pattern))
        tags.append(intent['tag'])

# ---- TF-IDF with Bigrams for better phrase matching ----
vectorizer = TfidfVectorizer(
    lowercase=True,
    stop_words='english',
    ngram_range=(1, 2),   # unigrams + bigrams
    analyzer='word'
)

if corpus:
    X = vectorizer.fit_transform(corpus)
else:
    X = None

def get_response(user_input):
    if not corpus or X is None:
        return "My knowledge base is empty."

    cleaned = preprocess(user_input)
    user_vec = vectorizer.transform([cleaned])
    similarities = cosine_similarity(user_vec, X)

    best_match_idx = int(np.argmax(similarities))
    best_match_score = float(similarities[0, best_match_idx])

    # Lowered threshold (0.15) to be more lenient with varied phrasing
    if best_match_score > 0.15:
        best_tag = tags[best_match_idx]
        for intent in knowledge_base['intents']:
            if intent['tag'] == best_tag:
                return random.choice(intent['responses'])

    # Fallback
    for intent in knowledge_base['intents']:
        if intent['tag'] == 'fallback':
            return random.choice(intent['responses'])

    return "I don't know that yet — I'll update my memory if you tell me."

