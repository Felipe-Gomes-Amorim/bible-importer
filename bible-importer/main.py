#!/usr/bin/env python3
"""
Consolidador de textos bíblicos multilíngues em SQLite.

Importa português, latim, grego (SBLGNT NT + LXX AT), hebraico e aramaico
de múltiplas fontes e consolida em um único banco de dados bible.db.
"""

import sqlite3
import os
from pathlib import Path
from parsers import portuguese, vulgate, greek, hebrew, lxx

DB_PATH = "output/bible.db"

# Normalização de códigos OSIS duplicados entre fontes
NORMALIZE = {
    "PS":  "PSA",   # Salmos
    "EZE": "EZK",   # Ezequiel
    "SON": "SNG",   # Cânticos
}

def create_schema(conn):
    """Cria o schema do banco de dados."""
    conn.execute("""
        CREATE TABLE IF NOT EXISTS verses (
            book    TEXT    NOT NULL,
            chapter INTEGER NOT NULL,
            verse   INTEGER NOT NULL,
            pt      TEXT,
            lat     TEXT,
            grc     TEXT,
            heb     TEXT,
            aram    TEXT,
            PRIMARY KEY (book, chapter, verse)
        )
    """)
    conn.commit()

def main():
    """Função principal de consolidação."""
    
    # Cria diretório de output se não existir
    os.makedirs("output", exist_ok=True)
    
    # Remove banco anterior se existir (reinicia do zero)
    if os.path.exists(DB_PATH):
        print(f"Removendo {DB_PATH} anterior...")
        os.remove(DB_PATH)
    
    conn = sqlite3.connect(DB_PATH)
    create_schema(conn)

    print("=" * 60)
    print("Iniciando importação de textos bíblicos")
    print("=" * 60)
    
    # Português
    print("\n[1/5] Carregando português (Almeida)...")
    pt_path = "data/biblia/json/aa.json"
    if os.path.exists(pt_path):
        pt = portuguese.load(pt_path)
        print(f"      OK {len(pt)} versículos")
    else:
        print(f"      ERRO Arquivo não encontrado: {pt_path}")
        print("      Clone: git clone https://github.com/thiagobodruk/biblia.git")
        pt = {}

    # Latim
    print("\n[2/5] Carregando latim (Vulgata)...")
    lat_path = "bible_databases/sources/la/Vulgate/Vulgate.json"
    if os.path.exists(lat_path):
        lat = vulgate.load(lat_path)
        print(f"      OK {len(lat)} versículos")
    else:
        print(f"      ERRO Arquivo não encontrado: {lat_path}")
        lat = {}

    # Grego
    print("\n[3/5] Carregando grego (SBLGNT NT)...")
    grc_dir = "sblgnt"
    if os.path.exists(grc_dir):
        grc = greek.load(grc_dir)
        print(f"      OK {len(grc)} versículos")
    else:
        print(f"      ERRO Diretório não encontrado: {grc_dir}")
        print("      Clone: git clone https://github.com/morphgnt/sblgnt.git")
        grc = {}
    
    # LXX (Septuaginta em grego - Antigo Testamento)
    print("\n[3.5/5] Carregando grego LXX (Antigo Testamento)...")
    try:
        lxx_data = lxx.load()
        print(f"      OK {len(lxx_data)} versículos")
        # Mescla LXX com SBLGNT (LXX tem AT, SBLGNT tem NT)
        # Se houver conflito, LXX tem prioridade (é mais completo para o AT)
        grc.update(lxx_data)
        print(f"      Total grego consolidado: {len(grc)} versículos")
    except Exception as e:
        print(f"      Aviso: Nao foi possivel carregar LXX: {e}")
        print(f"      Continuando com SBLGNT apenas...")

    # Hebraico/Aramaico
    print("\n[4/5] Carregando hebraico/aramaico (OSHB)...")
    heb_dir = "data/morphhb/wlc"
    if os.path.exists(heb_dir):
        heb, aram = hebrew.load(heb_dir)
        print(f"      OK {len(heb)} versículos hebraico")
        print(f"      OK {len(aram)} versículos aramaico")
    else:
        print(f"      ERRO Diretório não encontrado: {heb_dir}")
        print("      Clone: git clone https://github.com/openscriptures/morphhb.git")
        heb, aram = {}, {}

    # Consolidação com normalização de códigos OSIS
    print("\n[5/5] Consolidando no banco de dados...")
    
    # Normaliza todas as chaves para eliminar duplicatas
    def normalize_key(key):
        """Normaliza código OSIS na chave"""
        book, chap, vers = key
        book = NORMALIZE.get(book, book)
        return (book, chap, vers)
    
    # Une todos os conjuntos com normalização
    all_keys = set()
    for dict_data in [pt, lat, grc, heb, aram]:
        for key in dict_data.keys():
            all_keys.add(normalize_key(key))
    
    print(f"      Total de versículos únicos: {len(all_keys)}")

    rows = []
    for book, chap, vers in sorted(all_keys):
        # Tenta buscar com chave normalizada
        pt_text = pt.get((book, chap, vers))
        lat_text = lat.get((book, chap, vers))
        grc_text = grc.get((book, chap, vers))
        heb_text = heb.get((book, chap, vers))
        aram_text = aram.get((book, chap, vers))
        
        # Fallback: se não encontrou E este livro foi normalizado, tenta com chave original
        # APENAS se o livro atual é um dos que foram normalizados
        if not pt_text and book in NORMALIZE.values():
            orig_book = [k for k, v in NORMALIZE.items() if v == book][0]
            pt_text = pt.get((orig_book, chap, vers))
        
        if not lat_text and book in NORMALIZE.values():
            orig_book = [k for k, v in NORMALIZE.items() if v == book][0]
            lat_text = lat.get((orig_book, chap, vers))
        
        if not grc_text and book in NORMALIZE.values():
            orig_book = [k for k, v in NORMALIZE.items() if v == book][0]
            grc_text = grc.get((orig_book, chap, vers))
        
        if not heb_text and book in NORMALIZE.values():
            orig_book = [k for k, v in NORMALIZE.items() if v == book][0]
            heb_text = heb.get((orig_book, chap, vers))
        
        if not aram_text and book in NORMALIZE.values():
            orig_book = [k for k, v in NORMALIZE.items() if v == book][0]
            aram_text = aram.get((orig_book, chap, vers))
        
        rows.append((book, chap, vers, pt_text, lat_text, grc_text, heb_text, aram_text))

    conn.executemany(
        "INSERT OR REPLACE INTO verses VALUES (?,?,?,?,?,?,?,?)",
        rows
    )
    conn.commit()
    conn.close()
    
    print(f"\nOK Concluido. {len(rows)} versículos gravados em {DB_PATH}")
    print("=" * 60)

if __name__ == "__main__":
    main()
