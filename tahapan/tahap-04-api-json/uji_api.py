"""
Uji API Tahap 4 tanpa curl: kirim beberapa request ke server yang sedang berjalan.
Jalankan app.py dulu di terminal lain, lalu:  python uji_api.py
"""
import json
import urllib.error
import urllib.request

URL = "http://127.0.0.1:5000/api/chat"


def kirim(body):
    req = urllib.request.Request(URL, data=json.dumps(body).encode(), method="POST",
                                 headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req) as res:
            return res.status, json.loads(res.read())
    except urllib.error.HTTPError as e:          # kode 4xx/5xx
        return e.code, json.loads(e.read())


for body in [{"message": "halo"},
             {"message": "gmn cara bayar UKT"},
             {"message": "harga bensin berapa"},
             {"message": ""}]:
    status, data = kirim(body)
    print(f"POST {body} -> {status}")
    print("   ", json.dumps(data, ensure_ascii=False), "\n")
