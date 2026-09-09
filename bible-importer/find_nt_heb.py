import sqlite3

conn = sqlite3.connect('output/bible.db')

# Procurar duplicatas de versículos
print("Versículos que têm hebraico mas são do NT:\n")
nt_books = ('MAT', 'MRK', 'LUK', 'JHN', 'ACT', 'ROM', '1CO', '2CO', 'GAL', 
            'EPH', 'PHP', 'COL', '1TH', '2TH', '1TI', '2TI', 'TIT', 'PHM',
            'HEB', 'JAS', '1PE', '2PE', '1JN', '2JN', '3JN', 'JUD', 'REV')

result = conn.execute(f"""
    SELECT book, chapter, verse FROM verses 
    WHERE book IN ({','.join('?' * len(nt_books))})
    AND heb IS NOT NULL
    LIMIT 20
""", nt_books).fetchall()

for book, ch, vs in result:
    heb_content = conn.execute("SELECT heb FROM verses WHERE book=? AND chapter=? AND verse=?",
                                (book, ch, vs)).fetchone()[0]
    print(f"{book} {ch}:{vs} → {heb_content[:50]}...")

print(f"\nTotal de versículos NT com hebraico: {len(result)}")

# Verificar PSA 1:1 também
print("\n" + "="*70)
print("PSA 1:1 (esperado ter hebraico):")
psa = conn.execute("SELECT heb FROM verses WHERE book='PSA' AND chapter=1 AND verse=1").fetchone()
print(f"  {psa[0][:100] if psa[0] else '[VAZIO]'}...")

conn.close()
