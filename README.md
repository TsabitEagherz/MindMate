# MindMate — Chatbot Edukasi Kesehatan Mental

**MindMate** adalah chatbot tematik berbasis aturan yang dibuat dengan Flask. Chatbot ini menyediakan edukasi singkat tentang relaksasi, stres kuliah, refleksi diri, afirmasi, dan cara mencari bantuan profesional.

> MindMate bukan alat diagnosis, terapi, atau layanan darurat. Chatbot ini tidak menyimpan percakapan ke database secara default.

## Menjalankan aplikasi

Pastikan Python 3.10+ sudah terpasang. Dari folder repository, jalankan:

```bash
cd aplikasi-final
python -m venv .venv
```

Aktifkan lingkungan virtual:

```powershell
# Windows PowerShell
.venv\Scripts\Activate.ps1
```

```bash
# macOS / Linux
source .venv/bin/activate
```

Lalu pasang dependensi dan mulai server:

```bash
pip install -r requirements.txt
python app.py
```

Buka [http://127.0.0.1:5000](http://127.0.0.1:5000). Hentikan server dengan `Ctrl+C`.

## Struktur proyek

```text
chatbot-tematik-flask/
├── README.md
├── requirements.txt
├── template-tema.json
├── tahapan/                   # materi contoh praktikum dari paket dosen
└── aplikasi-final/
    ├── app.py                 # aplikasi Flask dan REST API
    ├── chatbot/               # mesin pencocokan intent dan database
    ├── themes/mindmate.json   # basis pengetahuan MindMate
    ├── templates/             # halaman web
    └── static/                # CSS dan JavaScript
```

## Mengubah basis pengetahuan

Intent, variasi pertanyaan, saran pertanyaan, dan respons berada di `aplikasi-final/themes/mindmate.json`. Formatnya mengikuti struktur tema pada contoh dosen. Engine mengukur kemiripan teks; tambahkan variasi pertanyaan yang alami agar pertanyaan pengguna lebih mungkin dikenali.

## API chat

Endpoint `POST /api/chat` menerima JSON berikut:

```json
{
  "message": "Aku sedang cemas, bantu aku tenang",
  "theme": "mindmate"
}
```

Balasan berisi `reply`, `intent`, dan `score`. Daftar tema tersedia melalui `GET /api/themes`.

## Privasi percakapan

Penyimpanan percakapan ke SQLite nonaktif secara default karena pengguna dapat membagikan informasi pribadi. Untuk mengaktifkannya secara eksplisit pada lingkungan lokal, setel `LOG_CONVERSATIONS=1` sebelum menjalankan aplikasi. Jangan aktifkan pada layanan publik tanpa pemberitahuan, perlindungan akses, dan kebijakan retensi data yang sesuai.

## Bantuan profesional

Untuk dukungan awal kesehatan jiwa di Indonesia, pengguna dapat mengunjungi [healing119.id](https://www.healing119.id/) atau menghubungi 119 ekstensi 8. Periksa situs resmi untuk informasi layanan terkini.
