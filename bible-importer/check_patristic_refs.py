import sqlite3

conn = sqlite3.connect('output/bible.db')
cur = conn.cursor()

# Verificar se a tabela existe
cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='patristic_refs'")
if cur.fetchone():
    cur.execute('SELECT COUNT(*) FROM patristic_refs')
    total = cur.fetchone()[0]
    print(f'Total de referências patrísticas: {total}')
    cur.execute('SELECT book, chapter, verse, author, work, quote FROM patristic_refs ORDER BY RANDOM() LIMIT 5')
    for row in cur.fetchall():
        print(row)
else:
    print('Tabela patristic_refs não encontrada!')

conn.close()
