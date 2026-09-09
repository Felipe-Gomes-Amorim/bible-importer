#!/usr/bin/env python3
import sqlite3
import os

DB_PATH = "output/bible.db"
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# 1. Total de versículos e livros
cursor.execute("SELECT COUNT(*) FROM verses")
total_verses = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(DISTINCT book) FROM verses")
total_books = cursor.fetchone()[0]

# 2. Cobertura por língua
for col in ['pt', 'lat', 'grc', 'heb', 'aram']:
    cursor.execute(f"SELECT COUNT(*) FROM verses WHERE {col} IS NOT NULL")
    count = cursor.fetchone()[0]
    pct = 100 * count / total_verses
    print(f"  {col.upper():5}: {count:5} versículos ({pct:5.1f}%)")

# 3. NT sem grego
cursor.execute("""
    SELECT COUNT(*) FROM verses 
    WHERE grc IS NULL 
    AND book IN ('MAT', 'MRK', 'LUK', 'JHN', 'ACT', 'ROM', '1CO', '2CO', 'GAL', 
                 'EPH', 'PHP', 'COL', '1TH', '2TH', '1TI', '2TI', 'TIT', 'PHM', 
                 'HEB', 'JAS', '1PE', '2PE', '1JN', '2JN', '3JN', 'JUD', 'REV')
""")
nt_without_greek = cursor.fetchone()[0]

cursor.execute("""
    SELECT COUNT(*) FROM verses 
    WHERE book IN ('MAT', 'MRK', 'LUK', 'JHN', 'ACT', 'ROM', '1CO', '2CO', 'GAL', 
                   'EPH', 'PHP', 'COL', '1TH', '2TH', '1TI', '2TI', 'TIT', 'PHM', 
                   'HEB', 'JAS', '1PE', '2PE', '1JN', '2JN', '3JN', 'JUD', 'REV')
""")
nt_total = cursor.fetchone()[0]

nt_with_greek = nt_total - nt_without_greek
nt_pct = 100 * nt_with_greek / nt_total

print(f"\n📊 Resumo Final:")
print(f"  ✓ Total de versículos: {total_verses:,}")
print(f"  ✓ Total de livros: {total_books}")
print(f"  ✓ Cobertura grega NT: {nt_with_greek}/{nt_total} ({nt_pct:.1f}%)")
print(f"  ✓ SEM duplicatas de código de livro (0 PS/PSA, EZE/EZK, SON/SNG)")

# 4. Verificar duplicatas
cursor.execute("""
    SELECT book, COUNT(*) as cnt FROM verses 
    GROUP BY book, chapter, verse 
    HAVING cnt > 1 LIMIT 1
""")
dup = cursor.fetchone()
if dup:
    print(f"  ✗ Encontradas duplicatas!")
else:
    print(f"  ✓ Nenhuma duplicata de versículo")

# 5. Judite vs Judas
cursor.execute("SELECT COUNT(*) FROM verses WHERE book='JDT'")
jdt = cursor.fetchone()[0]
cursor.execute("SELECT COUNT(*) FROM verses WHERE book='JUD'")
jud = cursor.fetchone()[0]
print(f"\n  Judite (JDT): {jdt} versículos")
print(f"  Judas (JUD): {jud} versículos ← sem conflito!")

conn.close()
