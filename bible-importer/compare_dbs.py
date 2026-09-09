import sqlite3

print('=== biblia-app/assets/bible.db ===')
try:
    conn = sqlite3.connect(r'..\biblia-app\assets\bible.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [t[0] for t in cursor.fetchall()]
    print(f'Tables: {tables}')
    
    # Verificar prefaces
    try:
        cursor.execute('SELECT COUNT(*) FROM book_prefaces')
        count = cursor.fetchone()[0]
        print(f'book_prefaces: {count} registros')
    except:
        print('book_prefaces: TABELA NÃO EXISTE')
    
    # Verificar patristic_refs
    try:
        cursor.execute('SELECT COUNT(*) FROM patristic_refs')
        count = cursor.fetchone()[0]
        print(f'patristic_refs: {count} registros')
    except:
        print('patristic_refs: TABELA NÃO EXISTE')
    
    conn.close()
except Exception as e:
    print(f'Erro: {e}')

print()
print('=== output/bible.db ===')
try:
    conn = sqlite3.connect(r'output\bible.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [t[0] for t in cursor.fetchall()]
    print(f'Tables: {tables}')
    
    # Verificar prefaces
    try:
        cursor.execute('SELECT COUNT(*) FROM book_prefaces')
        count = cursor.fetchone()[0]
        print(f'book_prefaces: {count} registros')
    except:
        print('book_prefaces: TABELA NÃO EXISTE')
    
    # Verificar patristic_refs
    try:
        cursor.execute('SELECT COUNT(*) FROM patristic_refs')
        count = cursor.fetchone()[0]
        print(f'patristic_refs: {count} registros')
    except:
        print('patristic_refs: TABELA NÃO EXISTE')
    
    conn.close()
except Exception as e:
    print(f'Erro: {e}')
