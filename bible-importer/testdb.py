import sqlite3
conn = sqlite3.connect(r"C:\Users\felipe\Documents\biblia\bible-importer\output\bible.db")
print("ROM 8:", conn.execute("SELECT COUNT(*) FROM patristic_refs WHERE book='ROM' AND chapter=8").fetchone()[0])
print("Amostra:", conn.execute("SELECT book, chapter, verse, author FROM patristic_refs LIMIT 5").fetchall())
conn.close()