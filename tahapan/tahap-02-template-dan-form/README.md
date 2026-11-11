# Tahap 2 — Template Jinja2 dan form

**Tujuan:** memindahkan HTML ke `templates/`, mengirim data ke template, pewarisan `base.html`,
dan menerima input dari form dengan metode POST.

```bash
python app.py
```

Buka http://127.0.0.1:5000 lalu **Coba bot beo**. Setiap pesan memuat ulang seluruh halaman;
riwayat disimpan di variabel `percakapan` sehingga hilang saat server dimatikan.

**Latihan:** buat bot beo membalas dengan huruf kapital semua (`pesan.upper()`).
