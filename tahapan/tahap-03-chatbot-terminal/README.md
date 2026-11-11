# Tahap 3 — Mesin chatbot di terminal

**Tujuan:** memahami cara kerja chatbot tanpa gangguan web.

| File | Isi |
| --- | --- |
| `kampus.json` | Basis pengetahuan: intent, pola, respons |
| `engine_v1_kata_kunci.py` | Versi 1: pola harus muncul persis di pesan |
| `engine_v2_kemiripan.py` | Versi 2: praproses + skor kemiripan + ambang 0,45 |
| `cli.py` | Chat di terminal |
| `bandingkan.py` | Bandingkan v1 dan v2 pada 9 kalimat |

```bash
python bandingkan.py        # hasil: versi 1 = 6/9, versi 2 = 9/9
python cli.py --debug
python cli.py --versi 1
```

**Latihan:** tambahkan 3 kata tidak baku ke `NORMALISASI` di `engine_v2_kemiripan.py`
lalu buktikan bot mengenalinya.
