"""Uji unit untuk mesin MindMate (tanpa Flask)."""
from pathlib import Path

import pytest

from chatbot.engine import ChatbotEngine, load_themes, preprocess, similarity

THEMES = load_themes(Path(__file__).resolve().parent.parent / "themes")
THEME = THEMES["mindmate"]


def test_preprocess_normalisasi_dan_stopword():
    assert preprocess("Gimana cara menenangkan pikiran, kak?") == ["bagaimana", "menenangkan", "pikiran"]


def test_similarity_kalimat_sama_bernilai_satu():
    t = ["latihan", "pernapasan"]
    assert similarity(t, t) == 1.0


def test_similarity_kalimat_berbeda_rendah():
    assert similarity(["hujan"], ["latihan", "pernapasan"]) < 0.3


def test_hanya_tema_mindmate_yang_termuat():
    assert set(THEMES) == {"mindmate"}


@pytest.mark.parametrize("pesan, intent", [
    ("halo", "salam"),
    ("aku ingin cerita", "teman_bicara"),
    ("ajari latihan pernapasan", "latihan_pernapasan"),
    ("kuis cek tingkat stres", "skrining_stres_kuliah"),
    ("cara mengatasi burnout kuliah", "tips_burnout_kuliah"),
    ("kirim afirmasi positif", "afirmasi_positif"),
    ("aku ingin bicara dengan psikolog", "mencari_bantuan"),
    ("aku ingin menyakiti diri", "kontak_bantuan_darurat"),
    ("makasih mindmate", "terima_kasih"),
])
def test_klasifikasi_intent_mindmate(pesan, intent):
    tag, _ = ChatbotEngine(THEME).classify(pesan)
    assert tag == intent


def test_salah_ketik_masih_dikenali():
    tag, _ = ChatbotEngine(THEME).classify("ajari latihan pernapasann")
    assert tag == "latihan_pernapasan"


def test_pertanyaan_di_luar_tema_memberi_fallback():
    hasil = ChatbotEngine(THEME).reply("siapa pemenang piala dunia")
    assert hasil["intent"] is None
    assert hasil["reply"] in THEME["fallback"]


def test_explain_mengurutkan_kandidat_dari_skor_tertinggi():
    kandidat = ChatbotEngine(THEME).explain("ajari latihan pernapasan")
    assert kandidat[0]["intent"] == "latihan_pernapasan"
    skor = [k["score"] for k in kandidat]
    assert skor == sorted(skor, reverse=True)


def test_validate_theme_menemukan_kesalahan():
    from chatbot.engine import validate_theme
    rusak = {"id": "x", "name": "X", "bot_name": "B", "avatar": "*", "color": "#000",
             "description": "d", "greeting": "g", "suggestions": [], "fallback": ["f"],
             "intents": [{"tag": "a", "patterns": ["halo"], "responses": ["hai"]},
                         {"tag": "b", "patterns": ["halo"], "responses": []}]}
    masalah = validate_theme(rusak)
    assert any("responses kosong" in m for m in masalah)
    assert any("'a' dan 'b'" in m for m in masalah)


def test_tema_mindmate_valid():
    from chatbot.engine import validate_theme
    assert validate_theme(THEME) == []


def test_evaluasi_data_mindmate_mengembalikan_skor_valid():
    from evaluate import baca_data, evaluasi
    data = baca_data("mindmate")
    akurasi, hasil = evaluasi(THEME, data, 0.45)
    assert 0.0 <= akurasi <= 1.0
    assert len(hasil) == len(data) > 0
