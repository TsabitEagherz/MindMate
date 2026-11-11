# Tahap 4 — Chatbot sebagai REST API

**Tujuan:** membungkus mesin chatbot menjadi endpoint `POST /api/chat` yang menerima dan
mengembalikan JSON, lengkap dengan validasi input dan kode status 400.

Terminal 1:

```bash
python app.py
```

Terminal 2:

```bash
python uji_api.py
```

**Latihan:** tambahkan endpoint `GET /api/intents` yang mengembalikan daftar tag intent.
