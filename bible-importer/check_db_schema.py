import sqlite3

conn = sqlite3.connect('output/bible.db')
cursor = conn.cursor()

# Check all tables
cursor.execute("SELECT sql FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()

print("TABELAS DO BANCO:")
print("=" * 60)
for t in tables:
    print(t[0])
    print()

# Check sample data
print("\nAMOSTRA DE DADOS (verses):")
cursor.execute("SELECT * FROM verses LIMIT 2")
rows = cursor.fetchall()
for row in rows:
    print(row)

# Check columns
cursor.execute("PRAGMA table_info(verses)")
cols = cursor.fetchall()
print("\nCOLUNAS DA TABELA verses:")
for col in cols:
    print(f"  {col[1]}: {col[2]}")

conn.close()
