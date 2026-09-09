import requests
from bs4 import BeautifulSoup
import sqlite3
import time
import re

BOOKS = [
    ("matthew",        "MAT", 28),
    ("mark",           "MRK", 16),
    ("luke",           "LUK", 24),
    ("john",           "JHN", 21),
    ("acts",           "ACT", 28),
    ("romans",         "ROM", 16),
    ("1corinthians",   "1CO", 16),
    ("2corinthians",   "2CO", 13),
    ("galatians",      "GAL",  6),
    ("ephesians",      "EPH",  6),
    ("philippians",    "PHP",  4),
    ("colossians",     "COL",  4),
    ("1thessalonians", "1TH",  5),
    ("2thessalonians", "2TH",  3),
    ("1timothy",       "1TI",  6),
    ("2timothy",       "2TI",  4),
    ("titus",          "TIT",  3),
    ("philemon",       "PHM",  1),
    ("hebrews",        "HEB", 13),
    ("james",          "JAS",  5),
    ("1peter",         "1PE",  5),
    ("2peter",         "2PE",  3),
    ("1john",          "1JN",  5),
    ("2john",          "2JN",  1),
    ("3john",          "3JN",  1),
    ("jude",           "JUD",  1),
    ("revelation",     "REV", 22),
]

BASE_URL = "https://www.earlychristianwritings.com/e-catena"
HEADERS  = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

def scrape_chapter(book_name, book_osis, chapter):
    url = f"{BASE_URL}/{book_name}{chapter}.html"
    try:
        r = requests.get(url, timeout=15, headers=HEADERS)
        r.encoding = 'latin-1'
    except Exception as e:
        print(f"  Erro de conexão: {e}")
        return []

    if r.status_code == 429:
        print(f"  429 - bloqueado, aguardando 60s...")
        time.sleep(60)
        return scrape_chapter(book_name, book_osis, chapter)

    if r.status_code != 200:
        print(f"  HTTP {r.status_code}: {url}")
        return []

    soup = BeautifulSoup(r.text, 'html.parser')
    infolayer = soup.find(id='infolayer') or soup.find('body')
    results = []

    # Itera pelos filhos diretos procurando o par <p> + <blockquote>
    tags = infolayer.find_all(['p', 'blockquote'], recursive=True)

    i = 0
    while i < len(tags):
        tag = tags[i]

        if tag.name == 'p':
            # Extrai o terceiro <a> = nome da obra
            links = tag.find_all('a')
            if len(links) < 3:
                i += 1
                continue

            work = links[2].get_text(strip=True)

            # Extrai versículo do texto do <p>
            p_text = tag.get_text(strip=True)
            m = re.search(r'\d+:(\d+)', p_text)
            verse = int(m.group(1)) if m else None

            # Extrai autor: primeira palavra da obra, com ajustes
            tokens = work.split()
            skip = {"epistle", "letter", "first", "second", "third",
                    "the", "on", "against", "of", "in", "an"}
            author = work  # fallback
            for t in tokens:
                if t.lower() not in skip:
                    author = t
                    break

            # Próximo blockquote é a citação
            if i + 1 < len(tags) and tags[i + 1].name == 'blockquote':
                quote_raw = tags[i + 1].get_text(strip=True)
                quote = re.sub(r'\[\d+\]$', '', quote_raw).strip()

                if quote:
                    results.append({
                        "book":    book_osis,
                        "chapter": chapter,
                        "verse":   verse,
                        "author":  author,
                        "work":    work,
                        "quote":   quote,
                        "source":  "ante-nicene",
                        "url":     url,
                    })
                i += 2  # pula o blockquote já consumido
                continue

        i += 1

    return results

def create_table(conn):
    conn.execute("DROP TABLE IF EXISTS patristic_refs")
    conn.execute("""
        CREATE TABLE patristic_refs (
            id      INTEGER PRIMARY KEY AUTOINCREMENT,
            book    TEXT    NOT NULL,
            chapter INTEGER NOT NULL,
            verse   INTEGER,
            author  TEXT,
            work    TEXT,
            quote   TEXT,
            source  TEXT,
            url     TEXT
        )
    """)
    conn.execute("""
        CREATE INDEX IF NOT EXISTS idx_pat_ref
        ON patristic_refs (book, chapter, verse)
    """)
    conn.commit()
    print("Tabela recriada.")

def main():
    conn = sqlite3.connect("output/bible.db")
    create_table(conn)

    total = 0
    for book_name, book_osis, num_chapters in BOOKS:
        print(f"\n{book_osis}...")
        for chap in range(1, num_chapters + 1):
            entries = scrape_chapter(book_name, book_osis, chap)
            if entries:
                conn.executemany("""
                    INSERT INTO patristic_refs
                        (book, chapter, verse, author, work, quote, source, url)
                    VALUES
                        (:book, :chapter, :verse, :author, :work,
                         :quote, :source, :url)
                """, entries)
                conn.commit()
                print(f"  c{chap}: {len(entries)} referências")
                total += len(entries)
            time.sleep(4)  # respeitoso com o servidor

    print(f"\nConcluído. {total} referências patrísticas gravadas.")
    conn.close()

if __name__ == "__main__":
    main()