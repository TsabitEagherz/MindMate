"""
TAHAP 5 — Antarmuka chat dengan HTML, CSS, dan JavaScript fetch()
Tujuan: halaman chat yang mengirim pesan ke /api/chat TANPA memuat ulang halaman.
Masih satu tema dan belum menyimpan riwayat (ditambahkan di aplikasi final).

Jalankan:  python app.py   lalu buka http://127.0.0.1:5000
"""
from pathlib import Path

from flask import Flask, jsonify, render_template, request

from engine import SimilarityBot, load_theme

app = Flask(__name__)
theme = load_theme(Path(__file__).parent / "themes" / "kampus.json")
bot = SimilarityBot(theme)


@app.get("/")
def index():
    # data tema dikirim ke template untuk nama bot, warna, sapaan, dan tombol saran
    return render_template("chat.html", theme=theme)


@app.post("/api/chat")
def api_chat():
    data = request.get_json(silent=True) or {}
    message = str(data.get("message", "")).strip()
    if not message:
        return jsonify({"error": "Pesan tidak boleh kosong"}), 400
    if len(message) > 500:
        return jsonify({"error": "Pesan maksimal 500 karakter"}), 400
    return jsonify(bot.reply(message))


if __name__ == "__main__":
    app.run(debug=True)
