"""
TAHAP 3 — Chatbot di terminal (belum ada web).

    python cli.py              # versi 2 (kemiripan)
    python cli.py --versi 1    # versi 1 (kata kunci persis)
    python cli.py --debug      # tampilkan 3 kandidat teratas (versi 2)
Ketik 'keluar' untuk berhenti.
"""
import argparse
from pathlib import Path

from engine_v1_kata_kunci import KeywordBot
from engine_v2_kemiripan import SimilarityBot, load_theme

parser = argparse.ArgumentParser()
parser.add_argument("--versi", type=int, choices=[1, 2], default=2)
parser.add_argument("--debug", action="store_true")
args = parser.parse_args()

theme = load_theme(Path(__file__).parent / "kampus.json")
bot = KeywordBot(theme) if args.versi == 1 else SimilarityBot(theme)
print(f"{theme['bot_name']} (versi {args.versi}): {theme['greeting']}\n")

while True:
    pesan = input("Anda: ").strip()
    if pesan.lower() == "keluar":
        break
    hasil = bot.reply(pesan)
    print(f"Bot : {hasil['reply']}")
    print(f"      [intent: {hasil['intent'] or 'tidak dikenali'} · skor {hasil['score']:.2f}]")
    if args.debug and args.versi == 2:
        for tag, pola, skor in bot.explain(pesan):
            print(f"      - {tag:<15} {skor:.2f}  pola: \"{pola}\"")
    print()
