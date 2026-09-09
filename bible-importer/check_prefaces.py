import sqlite3

conn = sqlite3.connect("output/bible.db")
cursor = conn.cursor()

# Verifica se a tabela foi criada
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='book_prefaces'")
table_exists = cursor.fetchone()

if not table_exists:
    print("✗ Tabela book_prefaces não encontrada")
else:
    print("✓ Tabela book_prefaces encontrada")
    
    # Conta registros
    cursor.execute("SELECT COUNT(*) FROM book_prefaces")
    count = cursor.fetchone()[0]
    print(f"  Total de prefácios: {count}")
    
    if count > 0:
        # Mostra primeiros registros
        cursor.execute("""
            SELECT book, title, length(content_eng), source_url
            FROM book_prefaces
            ORDER BY book
            LIMIT 20
        """)
        
        print("\n  Prefácios carregados:")
        for book, title, eng_len, url in cursor.fetchall():
            status = "✓" if eng_len > 0 else "✗"
            print(f"    {status} {book:4}  {title[:40]:<40}  {eng_len:>6} chars")

conn.close()
