# Menjalankan MindMate

Panduan utama proyek ada di [README.md](README.md). Aplikasi akhir berada di folder `aplikasi-final`.

```bash
cd aplikasi-final
python -m venv .venv
```

Aktifkan lingkungan virtual (`.venv\Scripts\Activate.ps1` pada PowerShell Windows atau `source .venv/bin/activate` pada macOS/Linux), kemudian:

```bash
pip install -r requirements.txt
python app.py
```

Buka http://127.0.0.1:5000 di browser. Folder `tahapan` berisi materi praktikum contoh dan tidak diperlukan untuk menjalankan MindMate.
