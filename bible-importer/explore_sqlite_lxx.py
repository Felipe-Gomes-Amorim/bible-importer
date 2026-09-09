#!/usr/bin/env python3
"""
Explora a estrutura do banco SQLite da LXX e tenta extrair uma amostra.
"""

import sqlite3
import requests
import tempfile
import os

print("="*70)
print("Explorando banco SQLite da LXX")
print("="*70)

# URL do SQLite
url_sqlite = "https://github.com/eliranwong/LXX-Rahlfs-1935/raw/master/11_end-users_files/MyBible/Bibles/LXX1.SQLite3"

print(f"\n1. Baixando banco SQLite... ({os.path.expanduser('~')})")
print(f"   URL: {url_sqlite}")

try:
    # Baixa o arquivo para temp
    r = requests.get(url_sqlite, timeout=60)
    
    if r.status_code == 200:
        print(f"✓ Sucesso! Tamanho: {len(r.content) / (1024*1024):.1f} MB")
        
        # Salva em arquivo temporário
        with tempfile.NamedTemporaryFile(delete=False, suffix='.sqlite3') as f:
            temp_db = f.name
            f.write(r.content)
        
        print(f"   Arquivo temporário: {temp_db}")
        
        # Conecta ao banco
        conn = sqlite3.connect(temp_db)
        cursor = conn.cursor()
        
        # Lista as tabelas
        print("\n2. Tabelas do banco:")
        print("-" * 70)
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        for (table_name,) in tables:
            print(f"   - {table_name}")
            
            # Mostra schema de cada tabela
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()
            for col_id, col_name, col_type, notnull, default, pk in columns:
                print(f"     • {col_name} ({col_type})")
            
            # Conta registros
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = cursor.fetchone()[0]
            print(f"     Registros: {count}")
        
        # Tenta extrair uma amostra de dados
        print("\n3. Amostra de dados (primeiras 5 linhas):")
        print("-" * 70)
        
        # Se houver tabela 'bible', mostra a amostra
        try:
            cursor.execute("SELECT * FROM bible LIMIT 5")
            columns = [description[0] for description in cursor.description]
            print(f"Colunas: {', '.join(columns)}")
            for row in cursor.fetchall():
                print(f"  {row}")
        except:
            # Tenta outra tabela
            if tables:
                first_table = tables[0][0]
                print(f"Usando tabela: {first_table}")
                cursor.execute(f"SELECT * FROM {first_table} LIMIT 5")
                columns = [description[0] for description in cursor.description]
                print(f"Colunas: {', '.join(columns)}")
                for row in cursor.fetchall():
                    print(f"  {row}")
        
        conn.close()
        
        # Remove arquivo temporário
        os.unlink(temp_db)
        print("\n✓ Arquivo temporário removido")
        
    else:
        print(f"✗ Erro ao baixar: {r.status_code}")
        
except Exception as e:
    print(f"✗ Erro: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*70)
