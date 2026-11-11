"""
TAHAP 1 — Halo, Flask!
Tujuan: memahami route, fungsi view, variabel URL, dan query string.

Jalankan:  python app.py
Coba buka:
    http://127.0.0.1:5000/
    http://127.0.0.1:5000/halo/Budi
    http://127.0.0.1:5000/cari?q=krs
    http://127.0.0.1:5000/api/info
"""
from datetime import datetime

from flask import Flask, jsonify, request

app = Flask(__name__)          # membuat objek aplikasi


@app.route("/")                # route: URL "/" dipetakan ke fungsi index()
def index():
    return "<h1>Halo, Flask!</h1><p>Server Python Anda berjalan.</p>"


@app.route("/halo/<nama>")     # variabel URL: bagian <nama> menjadi argumen fungsi
def halo(nama):
    return f"<h1>Halo, {nama}!</h1>"


@app.route("/cari")            # query string: /cari?q=kata
def cari():
    q = request.args.get("q", "")          # ambil parameter q, default ""
    if not q:
        return "Tambahkan ?q=kata di akhir URL", 400   # kode status 400
    return f"Anda mencari: <b>{q}</b>"


@app.route("/api/info")        # mengembalikan JSON, bukan HTML
def info():
    return jsonify({"aplikasi": "Tahap 1", "waktu_server": datetime.now().strftime("%H:%M:%S")})


if __name__ == "__main__":
    app.run(debug=True)        # debug=True: muat ulang otomatis saat file disimpan
