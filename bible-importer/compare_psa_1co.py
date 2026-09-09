import sqlite3

conn = sqlite3.connect('output/bible.db')

# Ver exatamente o que há em 1CO 1:1-5
print("1CO 1:1-5 no DB:")
for v in range(1, 6):
    row = conn.execute("SELECT book, pt, lat, heb FROM verses WHERE book='1CO' AND chapter=1 AND verse=?", (v,)).fetchone()
    if row:
        book, pt, lat, heb = row
        print(f"\n1CO 1:{v}")
        print(f"  PT:  {pt[:50] if pt else '[NULL]'}...")
        print(f"  LAT: {lat[:50] if lat else '[NULL]'}...")
        print(f"  HEB: {heb[:50] if heb else '[NULL]'}...")

# Ver o que há em PSA 1:1-5
print("\n" + "="*70)
print("PSA 1:1-5 no DB:")
for v in range(1, 6):
    row = conn.execute("SELECT book, pt, lat, heb FROM verses WHERE book='PSA' AND chapter=1 AND verse=?", (v,)).fetchone()
    if row:
        book, pt, lat, heb = row
        print(f"\nPSA 1:{v}")
        print(f"  PT:  {pt[:50] if pt else '[NULL]'}...")
        print(f"  LAT: {lat[:50] if lat else '[NULL]'}...")
        print(f"  HEB: {heb[:50] if heb else '[NULL]'}...")

conn.close()
