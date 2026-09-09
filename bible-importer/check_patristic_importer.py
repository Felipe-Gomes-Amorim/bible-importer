#!/usr/bin/env python3
import sqlite3
import os

db_path = 'output/bible.db'
if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Lista tabelas
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    print('TABELAS NO BIBLE-IMPORTER:')
    for table in tables:
        print(f'  - {table[0]}')
    
    # Verifica patristic_refs
    try:
        cursor.execute("SELECT COUNT(*) FROM patristic_refs")
        count = cursor.fetchone()[0]
        print(f'\nTABELA patristic_refs: {count} registros')
        
        # Mostra schema
        cursor.execute('PRAGMA table_info(patristic_refs)')
        columns = cursor.fetchall()
        print('\nSCHEMA (colunas):')
        for col in columns:
            print(f'  - {col[1]}: {col[2]}')
        
        # Exemplos de dados por livro
        cursor.execute("SELECT DISTINCT book FROM patristic_refs ORDER BY book")
        books = cursor.fetchall()
        print(f'\nLivros com referências patrísticas ({len(books)}):')
        for book in books[:5]:
            print(f'  - {book[0]}')
        if len(books) > 5:
            print(f'  ... e mais {len(books) - 5}')
            
    except Exception as e:
        print(f'\nTABELA patristic_refs: NÃO EXISTE')
        print(f'Erro: {e}')
    
    conn.close()
else:
    print(f'Arquivo não encontrado: {db_path}')
