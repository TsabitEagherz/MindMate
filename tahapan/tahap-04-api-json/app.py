"""
TAHAP 4 — Chatbot sebagai REST API (JSON)
Tujuan: membungkus mesin chatbot dari Tahap 3 menjadi endpoint web
POST /api/chat yang menerima dan mengembalikan JSON. Belum ada tampilan.

Jalankan:  python app.py
Uji (terminal lain):  python uji_api.py
           atau curl -X POST http://127.0.0.1:5000/api/chat -H "Content-Type: application/json" -d "{\"message\": \"cara bayar ukt\"}"
"""
from pathlib import Path

from flask import Flask, jsonify, request

from engine import SimilarityBot, load_theme

app = Flask(__name__)
bot = SimilarityBot(load_theme(Path(__file__).parent / "themes" / "kampus.json"))   # dibuat sekali saat server start


@app.get("/")
def index():
    return jsonify({"pesan": "API chatbot berjalan. Kirim POST ke /api/chat"})


def galat(pesan):
    """Balasan galat standar: JSON + kode status 400 (Bad Request)."""
    return jsonify({"error": pesan}), 400


@app.post("/api/chat")
def api_chat():
    data = request.get_json(silent=True)          # None jika body bukan JSON
    if data is None:
        return galat("Body harus berformat JSON")
    message = str(data.get("message", "")).strip()
    if not message:
        return galat("Pesan tidak boleh kosong")
    if len(message) > 500:
        return galat("Pesan maksimal 500 karakter")
    return jsonify(bot.reply(message))            # dict Python -> teks JSON


if __name__ == "__main__":
    app.run(debug=True)
