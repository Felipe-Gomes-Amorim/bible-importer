#!/usr/bin/env python3
"""
Parser para LXX (Septuaginta em grego).

Extrai dados do banco SQLite do Eliran Wong no GitHub e converte
para o formato (book_osis, chapter, verse) → texto grego.
"""

import sqlite3
import requests
import tempfile
import os
import re
from typing import Dict, Tuple

# Mapeia book_number (MyBible) para código OSIS
BOOK_NUMBER_TO_OSIS = {
    10: "GEN",    # Genesis
    20: "EXO",    # Exodus
    30: "LEV",    # Leviticus
    40: "NUM",    # Numbers
    50: "DEU",    # Deuteronomy
    60: "JOS",    # Joshua B (adaptado para JOS)
    70: "JDG",    # Judges B (adaptado para JDG)
    80: "RUT",    # Ruth
    90: "1SA",    # 1 Samuel (1 Kingdoms)
    100: "2SA",   # 2 Samuel (2 Kingdoms)
    110: "1KI",   # 1 Kings (3 Kingdoms)
    120: "2KI",   # 2 Kings (4 Kingdoms)
    130: "1CH",   # 1 Chronicles
    140: "2CH",   # 2 Chronicles
    150: "EZR",   # Ezra (Esdras B/II: 1-10)
    160: "NEH",   # Nehemiah (Esdras B/II: 11-23)
    190: "EST",   # Esther (with additions)
    220: "JOB",   # Job
    230: "PSA",   # Psalms
    240: "PRO",   # Proverbs
    250: "ECC",   # Ecclesiastes (Preacher)
    260: "SNG",   # Canticle (Song of Solomon)
    290: "ISA",   # Isaiah
    300: "JER",   # Jeremiah
    310: "LAM",   # Lamentations (Threni)
    330: "EZK",   # Ezekiel
    340: "DAN",   # Daniel LXX
    350: "HOS",   # Hosea
    360: "JOL",   # Joel
    370: "AMO",   # Amos
    380: "OBA",   # Obadiah
    390: "JON",   # Jonah
    400: "MIC",   # Micah
    410: "NAH",   # Nahum
    420: "HAB",   # Habakkuk
    430: "ZEP",   # Zephaniah
    440: "HAG",   # Haggai
    450: "ZEC",   # Zechariah
    460: "MAL",   # Malachi
    # Deuterocanônicos
    165: "1ES",   # Esdras A/I
    170: "TOB",   # Tobit BA
    180: "JDT",   # Judith
    232: "PSS",   # Psalms of Solomon (não é OSIS padrão)
    462: "1MC",   # I Maccabees
    464: "2MC",   # II Maccabees
    466: "3MC",   # III Maccabees
    467: "4MC",   # IV Maccabees
    270: "WIS",   # Wisdom of Solomon
    280: "SIR",   # Wisdom of Sirach
    315: "EJR",   # Epistle of Jeremiah
    320: "BAR",   # Baruch
    325: "SUS",   # Susanna LXX
    345: "BEL",   # Bel LXX
    800: "ODE",   # Odes
}

def clean_lxx_text(text: str) -> str:
    """
    Remove markup XML/metadados do texto da LXX.
    
    O texto original contém tags como:
    - <S>704639</S><m>lxx.P</m> (metadados)
    - Keep apenas as palavras gregas
    """
    if not text:
        return text
    
    # Remove tags <S>...</S> (números de dicionário)
    text = re.sub(r'<S>[^<]*</S>', '', text)
    
    # Remove tags <m>...</m> (códigos morfológicos)
    text = re.sub(r'<m>[^<]*</m>', '', text)
    
    # Remove outras tags XML que possam estar lá
    text = re.sub(r'<[^>]+>', '', text)
    
    # Limpa espaços múltiplos
    text = re.sub(r'\s+', ' ', text)
    
    return text.strip()

def download_sqlite_lxx(retries=3) -> str:
    """
    Baixa o banco SQLite da LXX do GitHub com retry.
    Retorna o caminho do arquivo temporário.
    """
    url = "https://github.com/eliranwong/LXX-Rahlfs-1935/raw/master/11_end-users_files/MyBible/Bibles/LXX1.SQLite3"
    
    print("[LXX] Baixando banco de dados SQLite...")
    
    for attempt in range(retries):
        try:
            print(f"[LXX] Tentativa {attempt + 1}/{retries}...")
            
            # Aumenta timeout e adiciona headers
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            r = requests.get(url, timeout=300, headers=headers)  # 5 minutos de timeout
            r.raise_for_status()
            
            # Salva em arquivo temporário
            with tempfile.NamedTemporaryFile(delete=False, suffix='.sqlite3') as f:
                temp_db = f.name
                f.write(r.content)
            
            size_mb = len(r.content) / (1024*1024)
            print(f"[LXX] OK Banco baixado: {size_mb:.1f} MB")
            
            return temp_db
            
        except Exception as e:
            print(f"[LXX] ERRO (tentativa {attempt + 1}/{retries}): {type(e).__name__}")
            if attempt < retries - 1:
                import time
                wait_time = (attempt + 1) * 5  # 5, 10, 15 segundos
                print(f"[LXX] Aguardando {wait_time}s antes de retry...")
                time.sleep(wait_time)
            else:
                print(f"[LXX] ERRO final ao baixar: {e}")
                raise

def load(download=True) -> Dict[Tuple[str, int, int], str]:
    """
    Carrega a LXX em memória.
    
    Retorna: {(book_osis, chapter, verse): texto_grego}
    
    Args:
        download: Se True, baixa do GitHub. Se False, tenta usar arquivo local.
    """
    result = {}
    
    # Tenta usar arquivo local se existir
    local_db = "data/lxx/LXX1.SQLite3"
    if os.path.exists(local_db) and not download:
        print(f"[LXX] Usando banco local: {local_db}")
        db_path = local_db
    else:
        # Baixa do GitHub
        db_path = download_sqlite_lxx()
        cleanup_temp = True
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Consulta todos os versículos
        print("[LXX] Carregando versículos...")
        cursor.execute("""
            SELECT book_number, chapter, verse, text 
            FROM verses 
            ORDER BY book_number, chapter, verse
        """)
        
        count = 0
        for book_num, chapter, verse, text in cursor.fetchall():
            if not text or not text.strip():
                continue
            
            # Limpa o markup XML do texto
            text = clean_lxx_text(text)
            if not text:
                continue
            
            # Mapeia para OSIS
            book_osis = BOOK_NUMBER_TO_OSIS.get(int(book_num))
            if not book_osis:
                print(f"[LXX] Aviso: book_number {book_num} nao mapeado")
                continue
            
            key = (book_osis, int(chapter), int(verse))
            result[key] = text
            count += 1
        
        conn.close()
        
        # Conta por livro
        books_covered = {}
        for (book, c, v), text in result.items():
            if book not in books_covered:
                books_covered[book] = 0
            books_covered[book] += 1
        
        print(f"[LXX] OK Carregado {count} versículos em {len(books_covered)} livros")
        
        # Mostra resumo
        print(f"[LXX] Livros com cobertura:")
        for book in sorted(books_covered.keys()):
            print(f"      {book}: {books_covered[book]} versículos")
        
        return result
        
    except Exception as e:
        print(f"[LXX] ERRO ao carregar: {e}")
        raise
    finally:
        # Limpa arquivo temporário se foi baixado
        if download and os.path.exists(db_path):
            try:
                os.unlink(db_path)
            except:
                pass

if __name__ == "__main__":
    # Teste rápido
    print("Testando parser LXX...")
    lxx = load()
    
    # Mostra algumas amostras
    if lxx:
        print("\nAmostras:")
        for (book, c, v), text in list(lxx.items())[:10]:
            print(f"  {book} {c}:{v} = {text[:50]}...")
