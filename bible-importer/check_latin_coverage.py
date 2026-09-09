import sqlite3

conn = sqlite3.connect(r'output\bible.db')

books = ['1SA', '2SA', '1KI', '2KI', '1CH', '2CH']
for book in books:
    # Contar versos em latim
    count = conn.execute(f"SELECT COUNT(*) FROM verses WHERE book='{book}' AND lat IS NOT NULL AND lat != ''").fetchone()[0]
    total = conn.execute(f"SELECT COUNT(*) FROM verses WHERE book='{book}'").fetchone()[0]
    pct = (count / total * 100) if total > 0 else 0
    print(f'{book}: {count}/{total} versos com latim ({pct:.1f}%)')

# Comparar com outros livros
print("\nComparação com outros livros:")
samples = ['GEN', 'MAT', 'ROM', 'JOB', 'PSA']
for book in samples:
    count = conn.execute(f"SELECT COUNT(*) FROM verses WHERE book='{book}' AND lat IS NOT NULL AND lat != ''").fetchone()[0]
    total = conn.execute(f"SELECT COUNT(*) FROM verses WHERE book='{book}'").fetchone()[0]
    pct = (count / total * 100) if total > 0 else 0
    print(f'{book}: {count}/{total} versos com latim ({pct:.1f}%)')

conn.close()
