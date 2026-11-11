"""
TAHAP 2 — Template Jinja2 dan form
Tujuan: memisahkan HTML ke folder templates/, mengirim data ke template,
dan menerima input pengguna lewat form (metode GET dan POST).
Hasilnya "bot beo" sederhana: membalas dengan mengulang pesan Anda.
Kekurangannya: setiap kirim pesan, seluruh halaman dimuat ulang (diperbaiki di Tahap 5).

Jalankan:  python app.py   lalu buka http://127.0.0.1:5000
"""
from flask import Flask, render_template, request

app = Flask(__name__)

TEMA = [   # data sementara di Python; di tahap berikutnya pindah ke file JSON
    {"id": "kampus", "nama": "Asisten Akademik Kampus", "avatar": "🎓"},
    {"id": "kuliner", "nama": "Pemandu Kuliner Nusantara", "avatar": "🍲"},
    {"id": "wisata", "nama": "Pemandu Wisata Yogyakarta", "avatar": "🏯"},
]

percakapan = []   # disimpan di memori: hilang saat server dimatikan


@app.route("/")
def index():
    return render_template("index.html", tema=TEMA)


@app.route("/beo", methods=["GET", "POST"])
def beo():
    if request.method == "POST":                 # form dikirim
        pesan = request.form.get("pesan", "").strip()
        if pesan:
            balasan = f"Anda berkata: “{pesan}”"
            percakapan.append(("Anda", pesan))
            percakapan.append(("Bot", balasan))
    return render_template("beo.html", percakapan=percakapan)


if __name__ == "__main__":
    app.run(debug=True)
