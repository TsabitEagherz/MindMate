"""
TAHAP 3a — Chatbot versi 1: pencocokan kata kunci persis.

Cara kerja: sebuah intent cocok jika salah satu polanya muncul PERSIS
(sebagai potongan teks) di dalam pesan pengguna. Intent pertama yang cocok menang.

Kelemahan yang akan terlihat (jalankan bandingkan.py):
- "jadwl kuliah"               -> GAGAL: salah ketik tidak dikenali
- "perpus buka jam berapa"     -> GAGAL: kata berbeda dari pola
- "halo, kapan pengisian krs?" -> SALAH: berhenti di intent pertama yang cocok (salam)
- "cara byar ukt"              -> benar hanya karena ada pola satu kata "ukt"
Tidak ada skor: hasilnya hanya cocok (1.0) atau tidak (0.0).
"""
import json
import random


def load_theme(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


class KeywordBot:
    def __init__(self, theme):
        self.theme = theme

    def classify(self, pesan):
        teks = pesan.lower()
        for intent in self.theme["intents"]:
            for pola in intent["patterns"]:
                if pola.lower() in teks:          # cocok persis sebagai potongan teks
                    return intent["tag"], 1.0
        return None, 0.0

    def reply(self, pesan):
        tag, skor = self.classify(pesan)
        if tag is None:
            return {"reply": random.choice(self.theme["fallback"]), "intent": None, "score": skor}
        intent = next(i for i in self.theme["intents"] if i["tag"] == tag)
        return {"reply": random.choice(intent["responses"]), "intent": tag, "score": skor}
