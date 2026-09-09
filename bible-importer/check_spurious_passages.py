import sqlite3

conn = sqlite3.connect('output/bible.db')

# João 7:53-8:11 (Mulher apanhada em adultério) - passagem espúria
print("=" * 70)
print("PASSAGEM ESPÚRIA: Mulher apanhada em adultério (João 7:53-8:11)")
print("Não apareça no SBLGNT (texto crítico) mas SIM na Vulgata Latina")
print("=" * 70)

for v in range(53, 54):
    row = conn.execute('SELECT pt, lat, grc FROM verses WHERE book=? AND chapter=? AND verse=?', 
                       ('JHN', 7, v)).fetchone()
    if row:
        print(f'\nJHN 7:{v}')
        print(f"  PT:  {row[0][:60] if row[0] else '[FALTA]'}...")
        print(f"  LAT: {row[1][:60] if row[1] else '[FALTA]'}...")
        print(f"  GRC: {row[2] if row[2] else '✂ [FALTA - ESPERADO: passagem espúria!]'}")

for v in range(1, 4):
    row = conn.execute('SELECT pt, lat, grc FROM verses WHERE book=? AND chapter=? AND verse=?',
                       ('JHN', 8, v)).fetchone()
    if row:
        print(f'\nJHN 8:{v}')
        print(f"  PT:  {row[0][:60] if row[0] else '[FALTA]'}...")
        print(f"  LAT: {row[1][:60] if row[1] else '[FALTA]'}...")
        print(f"  GRC: {row[2] if row[2] else '✂ [FALTA - ESPERADO: passagem espúria!]'}")

# Marcos 16:9-20 - Também espúrio
print("\n" + "=" * 70)
print("PASSAGEM ESPÚRIA: Final longo de Marcos (16:9-20)")
print("=" * 70)

for v in range(9, 21):
    row = conn.execute('SELECT pt, lat, grc FROM verses WHERE book=? AND chapter=? AND verse=?',
                       ('MRK', 16, v)).fetchone()
    if row:
        has_grc = "✓" if row[2] else "✂"
        print(f"MRK 16:{v:2} {has_grc}")

conn.close()
