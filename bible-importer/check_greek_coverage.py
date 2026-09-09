#!/usr/bin/env python3
"""Investiga versículos do NT sem grego"""

import sqlite3

DB_PATH = "output/bible.db"

conn = sqlite3.connect(DB_PATH)

# Livros do NT
nt_books = ('MAT','MRK','LUK','JHN','ACT','ROM','1CO','2CO',
            'GAL','EPH','PHP','COL','1TH','2TH','1TI','2TI',
            'TIT','PHM','HEB','JAS','1PE','2PE','1JN','2JN','3JN','JUD','REV')

print("Versículos do NT sem grego por livro:\n")
missing = conn.execute(f"""
    SELECT book, COUNT(*) as n FROM verses
    WHERE book IN ({','.join('?' * len(nt_books))})
    AND grc IS NULL
    GROUP BY book ORDER BY n DESC
""", nt_books).fetchall()

total_missing = 0
for book, n in missing:
    print(f"  {book}: {n} versículos sem grego")
    total_missing += n

print(f"\nTotal sem grego: {total_missing}")

# Verificar cobertura por livro
print("\n\nCobertura de grego por livro do NT:\n")
coverage = conn.execute(f"""
    SELECT book, 
           COUNT(*) as total,
           COUNT(CASE WHEN grc IS NOT NULL THEN 1 END) as com_grego,
           ROUND(100.0 * COUNT(CASE WHEN grc IS NOT NULL THEN 1 END) / COUNT(*), 1) as percent
    FROM verses
    WHERE book IN ({','.join('?' * len(nt_books))})
    GROUP BY book
    ORDER BY percent ASC, book
""", nt_books).fetchall()

for book, total, com_grego, percent in coverage:
    status = "✓" if percent == 100 else "✗"
    print(f"  {status} {book:6s}: {com_grego:5d}/{total} ({percent:5.1f}%)")

conn.close()
