import sqlite3

conn = sqlite3.connect('output/bible.db')
cursor = conn.cursor()

# Verificar um versículo com referência patrística
print("=" * 70)
print("VERIFICAÇÃO: Versículos com referências patrísticas PRESERVADAS")
print("=" * 70)

cursor.execute("""
    SELECT v.book, v.chapter, v.verse, v.pt, p.author, p.work
    FROM verses v
    JOIN patristic_refs p ON v.book = p.book AND v.chapter = p.chapter 
    LIMIT 5
""")

rows = cursor.fetchall()
for book, chapter, verse, pt, author, work in rows:
    print(f"\n{book} {chapter}:{verse}")
    print(f"  PT (ARA): {pt[:80]}...")
    print(f"  Referência: {author} - {work}")

# Verificar versículos nos três idiomas
print("\n" + "=" * 70)
print("VERIFICAÇÃO: Versículo com 3 idiomas (PT + LAT + GRC)")
print("=" * 70)

cursor.execute("""
    SELECT book, chapter, verse, pt, lat, grc
    FROM verses
    WHERE pt IS NOT NULL AND lat IS NOT NULL AND grc IS NOT NULL
    LIMIT 1
""")

row = cursor.fetchone()
if row:
    book, chapter, verse, pt, lat, grc = row
    print(f"\n{book} {chapter}:{verse}")
    print(f"  PT (ARA): {pt}")
    print(f"  LAT: {lat}")
    print(f"  GRC: {grc}")

# Verificar um prefácio
print("\n" + "=" * 70)
print("VERIFICAÇÃO: Prefácios de Jerônimo PRESERVADOS")
print("=" * 70)

cursor.execute("SELECT book, author, title FROM book_prefaces LIMIT 3")
rows = cursor.fetchall()
for book, author, title in rows:
    print(f"\n{book}")
    print(f"  Autor: {author}")
    print(f"  Título: {title}")

conn.close()
