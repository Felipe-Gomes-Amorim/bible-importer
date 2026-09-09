import sqlite3

DB_PATH = "output/bible.db"
conn = sqlite3.connect(DB_PATH)

print("Versículos NT sem grego por livro:\n")
missing = conn.execute("""
    SELECT book, COUNT(*) as n FROM verses
    WHERE book IN ('MAT','MRK','LUK','JHN','ACT','ROM',
                   '1CO','2CO','GAL','EPH','PHP','COL',
                   '1TH','2TH','1TI','2TI','TIT','PHM',
                   'HEB','JAS','1PE','2PE','1JN','2JN',
                   '3JN','JUD','REV')
    AND grc IS NULL
    GROUP BY book ORDER BY n DESC
""").fetchall()

for book, n in missing:
    # Total de versículos daquele livro
    total = conn.execute(f"SELECT COUNT(*) FROM verses WHERE book=?", (book,)).fetchone()[0]
    pct = 100 * n / total
    print(f"  {book}: {n}/{total} ({pct:.1f}%) sem grego")

print("\n" + "="*60)
print("Análise de especificidade:\n")

# Ver exemplos de versículos faltando
for book, _ in missing[:5]:
    missing_verses = conn.execute(f"""
        SELECT chapter, verse FROM verses 
        WHERE book=? AND grc IS NULL
        ORDER BY chapter, verse
        LIMIT 5
    """, (book,)).fetchall()
    
    print(f"\n{book} - Exemplos de versículos faltando:")
    for ch, vs in missing_verses:
        print(f"    {book} {ch}:{vs}")

conn.close()
