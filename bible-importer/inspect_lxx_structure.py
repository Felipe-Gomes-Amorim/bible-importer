#!/usr/bin/env python3
"""
Inspeciona a estrutura do CSV e SQLite da LXX do GitHub.
"""

import requests
import csv
from io import StringIO

print("="*70)
print("Inspecionando estrutura da LXX")
print("="*70)

# Baixa o arquivo books_main.csv primeiro (é pequeno)
print("\n1. Baixando books_main.csv...")
url_books = "https://raw.githubusercontent.com/eliranwong/LXX-Rahlfs-1935/master/11_end-users_files/MyBible/Bibles/books_main.csv"

try:
    r = requests.get(url_books, timeout=10)
    if r.status_code == 200:
        print("✓ Sucesso!\n")
        print("Conteúdo completo de books_main.csv:")
        print("-" * 70)
        print(r.text)
        print("-" * 70)
except Exception as e:
    print(f"✗ Erro: {e}")

# Verifica o arquivo CSV principal
print("\n2. Inspecionando LXX_final_main.csv...")
url_lxx = "https://raw.githubusercontent.com/eliranwong/LXX-Rahlfs-1935/master/11_end-users_files/MyBible/Bibles/LXX_final_main.csv"

try:
    r_head = requests.head(url_lxx, timeout=5)
    print(f"Status HTTP: {r_head.status_code}")
    print(f"Tamanho: {int(r_head.headers.get('content-length', 0)) / (1024*1024):.1f} MB")
    print(f"Tipo de conteúdo: {r_head.headers.get('content-type', 'desconhecido')}")
except Exception as e:
    print(f"✗ Erro: {e}")

# Verifica SQLite
print("\n3. Verificando arquivo LXX1.SQLite3...")
url_sqlite = "https://raw.githubusercontent.com/eliranwong/LXX-Rahlfs-1935/master/11_end-users_files/MyBible/Bibles/LXX1.SQLite3"

try:
    r_head = requests.head(url_sqlite, timeout=5)
    print(f"Status HTTP: {r_head.status_code}")
    print(f"Tamanho: {int(r_head.headers.get('content-length', 0)) / (1024*1024):.1f} MB")
except Exception as e:
    print(f"✗ Erro: {e}")

print("\n" + "="*70)
print("Conclusão:")
print("- books_main.csv: Mapeia códigos de livros")
print("- LXX_final_main.csv: Contém os textos (34 MB)")
print("- LXX1.SQLite3: Banco de dados SQLite estruturado (36 MB)")
print("\nMelhor estratégia:")
print("1. Usar SQLite para carregar direto")
print("2. Ou parsear o CSV grande")
print("="*70)
