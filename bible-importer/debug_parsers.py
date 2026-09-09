#!/usr/bin/env python3
"""
Debug dos parsers — verifica cada fonte individualmente.
"""

import os
import sys

print("\n" + "=" * 70)
print("DEBUG DOS PARSERS")
print("=" * 70)

# 1. Português
print("\n[1] Português (JSON):")
pt_path = "data/biblia/json/aa.json"
if os.path.exists(pt_path):
    print(f"  ✓ Arquivo encontrado: {pt_path}")
    import json
    try:
        with open(pt_path, encoding='utf-8-sig') as f:
            data = json.load(f)
        print(f"  ✓ JSON válido, {len(data)} livros")
    except Exception as e:
        print(f"  ✗ Erro ao ler JSON: {e}")
else:
    print(f"  ✗ Arquivo NÃO encontrado: {pt_path}")
    print(f"    Clone: git clone https://github.com/thiagobodruk/biblia.git")

# 2. Latim
print("\n[2] Latim (Vulgata SQLite):")
lat_path = "data/bible_databases/sql/t_vul.sql"
if os.path.exists(lat_path):
    print(f"  ✓ Arquivo encontrado: {lat_path}")
    try:
        import sqlite3
        conn = sqlite3.connect(lat_path)
        tables = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table'"
        ).fetchall()
        print(f"  ✓ Tabelas: {[t[0] for t in tables]}")
        
        # Tenta query em t_vul
        if tables:
            count = conn.execute("SELECT COUNT(*) FROM t_vul").fetchone()[0]
            print(f"  ✓ t_vul tem {count} linhas")
            sample = conn.execute("SELECT b, c, v, t FROM t_vul LIMIT 1").fetchone()
            print(f"    Sample: b={sample[0]}, c={sample[1]}, v={sample[2]}, t={sample[3][:50]}...")
        conn.close()
    except Exception as e:
        print(f"  ✗ Erro: {e}")
else:
    print(f"  ✗ Arquivo NÃO encontrado: {lat_path}")
    print(f"    Clone: git clone https://github.com/scrollmapper/bible_databases.git")

# 3. Grego
print("\n[3] Grego (SBLGNT TXT):")
grc_dir = "data/sblgnt/data"
if os.path.exists(grc_dir):
    print(f"  ✓ Diretório encontrado: {grc_dir}")
    txt_files = [f for f in os.listdir(grc_dir) if f.endswith('.txt')]
    print(f"  ✓ {len(txt_files)} arquivos .txt encontrados")
    if txt_files:
        sample_file = os.path.join(grc_dir, txt_files[0])
        with open(sample_file, encoding='utf-8') as f:
            first_line = f.readline()
        print(f"    Primeiro arquivo: {txt_files[0]}")
        print(f"    Primeira linha: {first_line[:70]}")
else:
    print(f"  ✗ Diretório NÃO encontrado: {grc_dir}")
    print(f"    Clone: git clone https://github.com/morphgnt/sblgnt.git")

# 4. Hebraico
print("\n[4] Hebraico (OSHB XML):")
heb_dir = "data/morphhb/wlc"
if os.path.exists(heb_dir):
    print(f"  ✓ Diretório encontrado: {heb_dir}")
    xml_files = [f for f in os.listdir(heb_dir) if f.endswith('.xml')]
    print(f"  ✓ {len(xml_files)} arquivos .xml encontrados")
    if xml_files:
        print(f"    Primeiros arquivos: {xml_files[:5]}")
else:
    print(f"  ✗ Diretório NÃO encontrado: {heb_dir}")
    print(f"    Clone: git clone https://github.com/openscriptures/morphhb.git")

print("\n" + "=" * 70 + "\n")
