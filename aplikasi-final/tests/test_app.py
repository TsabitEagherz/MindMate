"""Uji integrasi route Flask untuk aplikasi MindMate."""
import pytest

from app import create_app


@pytest.fixture
def client(tmp_path):
    app = create_app({"TESTING": True, "DATABASE": str(tmp_path / "test.db")})
    return app.test_client()


def test_halaman_utama_menampilkan_mindmate(client):
    res = client.get("/")
    assert res.status_code == 200
    html = res.get_data(as_text=True)
    assert "MindMate" in html
    assert "kesehatan mental" in html.lower()
    assert "119 ekstensi 8" in html


def test_halaman_chat_mindmate_menampilkan_privasi_dan_bantuan(client):
    res = client.get("/chat/mindmate")
    assert res.status_code == 200
    html = res.get_data(as_text=True)
    assert "MindMate" in html
    assert "tidak disimpan ke database" in html
    assert "healing119.id" in html


def test_tema_lama_tidak_tersedia(client):
    assert client.get("/chat/kampus").status_code == 404
    assert client.get("/chat/kuliner").status_code == 404
    assert client.get("/api/history/wisata").status_code == 404


def test_api_themes_hanya_menampilkan_mindmate(client):
    data = client.get("/api/themes").get_json()
    assert len(data) == 1
    assert data[0]["id"] == "mindmate"


def test_api_chat_mengembalikan_intent_mindmate(client):
    res = client.post("/api/chat", json={"message": "ajari latihan pernapasan", "theme": "mindmate"})
    assert res.status_code == 200
    data = res.get_json()
    assert data["intent"] == "latihan_pernapasan"
    assert data["reply"]


@pytest.mark.parametrize("payload", [
    {"message": "", "theme": "mindmate"},
    {"message": "halo", "theme": "salah"},
    {"message": "a" * 501, "theme": "mindmate"},
    {},
])
def test_api_chat_input_tidak_valid(client, payload):
    assert client.post("/api/chat", json=payload).status_code == 400


def test_riwayat_tidak_disimpan_secara_default(client):
    client.post("/api/chat", json={"message": "halo", "theme": "mindmate"})
    assert client.get("/api/history/mindmate").get_json() == []


def test_riwayat_hanya_disimpan_jika_diaktifkan(tmp_path):
    app = create_app({"TESTING": True, "DATABASE": str(tmp_path / "logged.db"),
                      "LOG_CONVERSATIONS": True})
    client = app.test_client()
    client.post("/api/chat", json={"message": "halo", "theme": "mindmate"})
    rows = client.get("/api/history/mindmate").get_json()
    assert [r["sender"] for r in rows] == ["user", "bot"]


def test_statistik_intent_dengan_logging_diaktifkan(tmp_path):
    app = create_app({"TESTING": True, "DATABASE": str(tmp_path / "stats.db"),
                      "LOG_CONVERSATIONS": True})
    client = app.test_client()
    client.post("/api/chat", json={"message": "halo", "theme": "mindmate"})
    stats = client.get("/api/stats/mindmate").get_json()
    assert stats[0]["intent"] == "salam"


def test_api_explain_mindmate(client):
    data = client.post("/api/explain", json={"message": "ajari latihan pernapasan",
                                             "theme": "mindmate"}).get_json()
    assert data["threshold"] == 0.45
    assert data["candidates"][0]["intent"] == "latihan_pernapasan"


def test_halaman_admin_mindmate_memakai_riwayat_lokal(tmp_path):
    app = create_app({"TESTING": True, "DATABASE": str(tmp_path / "admin.db"),
                      "LOG_CONVERSATIONS": True})
    client = app.test_client()
    client.post("/api/chat", json={"message": "pertanyaan yang belum dikenali", "theme": "mindmate"})
    html = client.get("/admin/mindmate").get_data(as_text=True)
    assert "pertanyaan yang belum dikenali" in html
    assert "tidak dikenali" in html


def test_admin_key_melindungi_halaman_admin(tmp_path):
    app = create_app({"TESTING": True, "DATABASE": str(tmp_path / "admin-key.db"),
                      "ADMIN_KEY": "rahasia"})
    client = app.test_client()
    assert client.get("/admin/mindmate").status_code == 403
    assert client.get("/api/stats/mindmate").status_code == 403
    assert client.get("/admin/mindmate?key=rahasia").status_code == 200
