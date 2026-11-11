"""
TAHAP 3 — Bandingkan versi 1 (kata kunci) dan versi 2 (kemiripan) pada kalimat yang sama.

    python bandingkan.py
"""
from pathlib import Path

from engine_v1_kata_kunci import KeywordBot
from engine_v2_kemiripan import SimilarityBot, load_theme

theme = load_theme(Path(__file__).parent / "kampus.json")
v1, v2 = KeywordBot(theme), SimilarityBot(theme)

KALIMAT = [
    ("cara bayar ukt", "ukt"),
    ("Gimana cara bayar UKT, kak?", "ukt"),
    ("cara byar ukt", "ukt"),                 # salah ketik
    ("ukt bayarnya gimana", "ukt"),           # urutan kata berbeda
    ("jadwl kuliah", "jadwal_kuliah"),        # salah ketik
    ("perpus buka jam berapa", "perpustakaan"),
    ("syarat beasiswa apa aja", "beasiswa"),
    ("halo, kapan pengisian krs?", "krs"),    # dua maksud: v1 berhenti di "halo"
    ("harga bensin berapa", None),            # di luar tema
]

print(f"{'kalimat':<30}{'harapan':<16}{'versi 1':<16}{'versi 2':<22}")
print("-" * 84)
benar1 = benar2 = 0
for kalimat, harapan in KALIMAT:
    t1, _ = v1.classify(kalimat)
    t2, s2 = v2.classify(kalimat)
    benar1 += t1 == harapan
    benar2 += t2 == harapan
    tanda = lambda t: "✓" if t == harapan else "✗"
    print(f"{kalimat:<30}{str(harapan):<16}{tanda(t1)} {str(t1):<14}{tanda(t2)} {str(t2)} ({s2:.2f})")
print("-" * 84)
print(f"Benar: versi 1 = {benar1}/{len(KALIMAT)}, versi 2 = {benar2}/{len(KALIMAT)}")
