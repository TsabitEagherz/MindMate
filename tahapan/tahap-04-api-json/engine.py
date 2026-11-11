"""
Mesin chatbot: salinan engine_v2_kemiripan.py dari Tahap 3
(praproses + skor kemiripan + ambang batas).
"""
import json
import random
import re
from difflib import SequenceMatcher

NORMALISASI = {
    "gak": "tidak", "ga": "tidak", "nggak": "tidak", "gimana": "bagaimana", "gmn": "bagaimana",
    "brp": "berapa", "yg": "yang", "utk": "untuk", "sy": "saya", "aku": "saya",
    "kak": "", "min": "", "dong": "", "sih": "", "ya": "",
    "makasih": "terima kasih", "hai": "halo", "hi": "halo",
}
STOPWORDS = {"yang", "di", "ke", "dari", "dan", "itu", "ini", "untuk", "dengan", "apa",
             "saya", "mau", "ingin", "tolong", "bisa", "ada", "tentang", "info", "informasi"}


def load_theme(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def preprocess(teks):
    """Langkah 1-4: huruf kecil, buang tanda baca, normalisasi, buang kata henti."""
    teks = re.sub(r"[^a-z0-9\s]", " ", teks.lower())
    tokens = []
    for kata in teks.split():
        for k in NORMALISASI.get(kata, kata).split():
            if k and k not in STOPWORDS:
                tokens.append(k)
    return tokens


def similarity(a, b):
    """Skor 0..1 = 0,4 Jaccard + 0,3 kemiripan huruf + 0,3 cakupan."""
    if not a or not b:
        return 0.0
    sa, sb = set(a), set(b)
    jaccard = len(sa & sb) / len(sa | sb)
    fuzzy = SequenceMatcher(None, " ".join(a), " ".join(b)).ratio()
    cakupan = len(sa & sb) / len(sb)
    return round(0.4 * jaccard + 0.3 * fuzzy + 0.3 * cakupan, 4)


class SimilarityBot:
    def __init__(self, theme, threshold=0.45):
        self.theme, self.threshold = theme, threshold
        self.patterns = [(i["tag"], pola, preprocess(pola))
                         for i in theme["intents"] for pola in i["patterns"]]

    def explain(self, pesan, top=3):
        tokens = preprocess(pesan)
        best = {}
        for tag, pola, pt in self.patterns:
            s = similarity(tokens, pt)
            if tag not in best or s > best[tag][1]:
                best[tag] = (pola, s)
        return sorted(((t, p, s) for t, (p, s) in best.items()), key=lambda x: -x[2])[:top]

    def classify(self, pesan):
        kandidat = self.explain(pesan, 1)
        if not kandidat or kandidat[0][2] < self.threshold:
            return None, (kandidat[0][2] if kandidat else 0.0)
        return kandidat[0][0], kandidat[0][2]

    def reply(self, pesan):
        tag, skor = self.classify(pesan)
        if tag is None:
            return {"reply": random.choice(self.theme["fallback"]), "intent": None, "score": skor}
        intent = next(i for i in self.theme["intents"] if i["tag"] == tag)
        return {"reply": random.choice(intent["responses"]), "intent": tag, "score": skor}
