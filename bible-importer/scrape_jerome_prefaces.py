#!/usr/bin/env python3
"""
Scraper de prefácios de Jerônimo do CCEL (Christian Classics Ethereal Library).
Fonte simples, sem JavaScript, fácil de parsear.
"""

import requests
from bs4 import BeautifulSoup
import sqlite3
import time

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
BASE = "https://www.ccel.org/ccel/pearse/morefathers/files"

# (url_slug, book_osis, título)
PREFACES = [
    ("jerome_preface_genesis",         "GEN", "Prologue to Genesis"),
    ("jerome_preface_joshua",          "JOS", "Prologue to Joshua"),
    ("jerome_preface_kings",           "1SA", "Helmeted Introduction to Kings"),
    ("jerome_preface_chronicles",      "1CH", "Prologue to Chronicles"),
    ("jerome_preface_ezra",            "EZR", "Prologue to Ezra"),
    ("jerome_preface_tobit",           "TOB", "Prologue to Tobit"),
    ("jerome_preface_judith",          "JDT", "Prologue to Judith"),
    ("jerome_preface_esther",          "EST", "Prologue to Esther"),
    ("jerome_preface_job",             "JOB", "Prologue to Job"),
    ("jerome_preface_psalms_lxx",      "PSA", "Prologue to Psalms (LXX)"),
    ("jerome_preface_psalms_hebrew",   "PSA", "Prologue to Psalms (Hebrew)"),
    ("jerome_preface_solomon",         "PRO", "Prologue to the Books of Solomon"),
    ("jerome_preface_isaiah",          "ISA", "Prologue to Isaiah"),
    ("jerome_preface_jeremiah",        "JER", "Prologue to Jeremiah"),
    ("jerome_preface_ezekiel",         "EZK", "Prologue to Ezekiel"),
    ("jerome_preface_daniel",          "DAN", "Prologue to Daniel"),
    ("jerome_preface_prophets",        "HOS", "Prologue to the Twelve Prophets"),
    ("jerome_preface_gospels",         "MAT", "Letter to Pope Damasus: Preface to the Gospels"),
    ("jerome_preface_pauls_letters",   "ROM", "Preface to Paul's Letters"),
]

def fetch_preface(slug, retries=3):
    """Faz fetch e parse de um prefácio individual com retry."""
    url = f"{BASE}/{slug}.htm"
    
    for attempt in range(retries):
        try:
            r = requests.get(url, timeout=20, headers=HEADERS)
            r.encoding = 'utf-8'
            
            if r.status_code == 429:
                wait_time = 30 * (attempt + 1)
                print(f"    429 — aguardando {wait_time}s (tentativa {attempt+1}/{retries})...", end=" ")
                time.sleep(wait_time)
                continue
            
            if r.status_code == 503:
                wait_time = 10 * (attempt + 1)
                print(f"    503 — aguardando {wait_time}s (tentativa {attempt+1}/{retries})...", end=" ")
                time.sleep(wait_time)
                continue
            
            if r.status_code != 200:
                print(f"    HTTP {r.status_code}")
                return None, url
            
            # Sucesso
            break
                
        except requests.exceptions.Timeout:
            print(f"    Timeout (tentativa {attempt+1}/{retries})...", end=" ")
            if attempt < retries - 1:
                time.sleep(5)
            else:
                return None, url
        except Exception as e:
            print(f"    Erro: {str(e)[:50]}...", end=" ")
            if attempt < retries - 1:
                time.sleep(5)
            else:
                return None, url

    soup = BeautifulSoup(r.text, 'html.parser')

    # Remove navegação (imagens de prev/next/toc)
    for img in soup.find_all('img'):
        img.decompose()

    # Extrai body
    body = soup.find('body')
    if not body:
        return None, url

    # Extrai texto corrido — preserva parágrafos
    paragraphs = []
    for tag in body.find_all(['p', 'h1', 'h2', 'h3', 'blockquote']):
        text = tag.get_text(separator=' ', strip=True)
        
        # Filtra navegação e metadados
        if any(skip in text for skip in [
            'Previous Page', 'Table Of Contents', 'Next Page',
            'Early Church Fathers', 'public domain', 'translated by',
            'Kevin introduced', 'unicode', 'CCEL Home'
        ]):
            continue
        
        if len(text) > 30:
            paragraphs.append(text)

    content_eng = '\n\n'.join(paragraphs)
    return content_eng, url
def create_table(conn):
    conn.execute("""
        CREATE TABLE IF NOT EXISTS book_prefaces (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            book        TEXT NOT NULL,
            author      TEXT NOT NULL DEFAULT 'Jerome',
            title       TEXT,
            content_lat TEXT,
            content_eng TEXT,
            source_url  TEXT
        )
    """)
    conn.commit()

def main():
    print("="*70)
    print("Scraper de Prefácios de Jerônimo (CCEL)")
    print("="*70)
    
    conn = sqlite3.connect("output/bible.db")
    create_table(conn)

    # Verifica quais já foram carregadas para evitar duplicatas
    cursor = conn.execute("SELECT book FROM book_prefaces WHERE content_eng IS NOT NULL")
    already_loaded = set(row[0] for row in cursor.fetchall())
    
    print(f"\n{len(already_loaded)} prefácios já carregados: {', '.join(sorted(already_loaded))}")
    
    pending = [(s, b, t) for s, b, t in PREFACES if b not in already_loaded]
    
    if not pending:
        print("\nTodos os prefácios já foram carregados!")
        conn.close()
        return

    total = 0
    failed = []
    
    print(f"\nCarregando {len(pending)} prefácios restantes...\n")
    
    for i, (slug, book_osis, title) in enumerate(pending, 1):
        print(f"[{i:2}/{len(pending)}] {book_osis:4} — {title[:45]:<45}...", end=" ", flush=True)
        
        try:
            content_eng, url = fetch_preface(slug, retries=3)

            if content_eng:
                conn.execute("""
                    INSERT OR REPLACE INTO book_prefaces
                        (book, author, title, content_eng, source_url)
                    VALUES (?, 'Jerome', ?, ?, ?)
                """, (book_osis, title, content_eng, url))
                conn.commit()
                print(f"✓ {len(content_eng):>6} chars")
                total += 1
            else:
                print(f"✗ vazio")
                failed.append(book_osis)

        except KeyboardInterrupt:
            print("\n\n⚠ Interrupção do usuário")
            break
        except Exception as e:
            print(f"✗ erro: {e}")
            failed.append(book_osis)

        # Rate limiting com backoff progressivo
        if i < len(pending):
            time.sleep(3)

    print(f"\n{'='*70}")
    print(f"Resumo:")
    print(f"  Novos prefácios: {total}")
    if failed:
        print(f"  Falhados: {', '.join(failed)}")
    
    # Validação final
    print(f"\n{'='*70}")
    print("Estado final do banco:\n")
    
    rows = conn.execute("""
        SELECT book, title, length(content_eng)
        FROM book_prefaces
        ORDER BY book
    """).fetchall()
    
    total_chars = 0
    for book, title, length_eng in rows:
        status = "✓" if length_eng > 0 else "✗"
        print(f"  {status} {book:4}  {title[:40]:<40}  {length_eng if length_eng else 0:>7} chars")
        if length_eng:
            total_chars += length_eng

    print(f"\nTotal: {total_chars:,} caracteres em {len(rows)} prefácios")
    
    conn.close()
    print(f"{'='*70}\n")

if __name__ == "__main__":
    main()
