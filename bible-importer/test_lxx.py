#!/usr/bin/env python3
"""
Testa a LXX carregada no banco de dados.
"""

import sqlite3
from pathlib import Path
import sys
import io

# Force UTF-8 output on Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

DB_PATH = "output/bible.db"

def test_lxx():
    """Testa alguns versículos da LXX."""
    
    if not Path(DB_PATH).exists():
        print(f"ERRO: Banco {DB_PATH} nao encontrado!")
        return
    
    print("="*70)
    print("Testando LXX no banco de dados")
    print("="*70)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Alguns livros da LXX para testar
    test_verses = [
        ("GEN", 1, 1),    # Genesis 1:1
        ("EXO", 1, 1),    # Exodus 1:1
        ("PSA", 23, 1),   # Psalm 23:1
        ("ISA", 1, 1),    # Isaiah 1:1
        ("JER", 1, 1),    # Jeremiah 1:1
        ("DAN", 1, 1),    # Daniel 1:1
        ("MAL", 1, 1),    # Malachi 1:1
        ("TOB", 1, 1),    # Tobit 1:1 (deuterocanônico)
        ("1MC", 1, 1),    # 1 Maccabees 1:1 (deuterocanônico)
        ("WIS", 1, 1),    # Wisdom of Solomon 1:1
    ]
    
    print(f"\nConsultando {len(test_verses)} versículos da LXX:\n")
    
    found = 0
    for book, chapter, verse in test_verses:
        cursor.execute("""
            SELECT pt, lat, grc, heb, aram 
            FROM verses 
            WHERE book = ? AND chapter = ? AND verse = ?
        """, (book, chapter, verse))
        
        result = cursor.fetchone()
        
        if result:
            pt, lat, grc, heb, aram = result
            found += 1
            
            print(f"[{book} {chapter}:{verse}]")
            
            if grc:
                print(f"  Grego (LXX): {grc[:80]}...")
            else:
                print(f"  Grego: [sem dados]")
            
            if pt:
                print(f"  Português: {pt[:80]}...")
            if lat:
                print(f"  Latim: {lat[:80]}...")
            
            print()
        else:
            print(f"[{book} {chapter}:{verse}] - NAO ENCONTRADO")
            print()
    
    conn.close()
    
    print("="*70)
    print(f"Resultado: {found}/{len(test_verses)} versículos encontrados")
    print("="*70)
    
    # Estatísticas
    print("\nEstatísticas do banco:")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Total de versículos
    cursor.execute("SELECT COUNT(*) FROM verses")
    total = cursor.fetchone()[0]
    print(f"  Total de versículos: {total}")
    
    # Versículos com grego
    cursor.execute("SELECT COUNT(*) FROM verses WHERE grc IS NOT NULL")
    grc_count = cursor.fetchone()[0]
    print(f"  Com grego: {grc_count}")
    
    # Livros com grego
    cursor.execute("SELECT COUNT(DISTINCT book) FROM verses WHERE grc IS NOT NULL")
    books_with_grc = cursor.fetchone()[0]
    print(f"  Livros com grego: {books_with_grc}")
    
    # Livros LXX (Antigo Testamento)
    lxx_books = ['GEN', 'EXO', 'LEV', 'NUM', 'DEU', 'JOS', 'JDG', 'RUT', 
                 '1SA', '2SA', '1KI', '2KI', '1CH', '2CH', 'EZR', 'NEH', 
                 'EST', 'JOB', 'PSA', 'PRO', 'ECC', 'SNG', 'ISA', 'JER', 
                 'LAM', 'EZK', 'DAN', 'HOS', 'JOL', 'AMO', 'OBA', 'JON', 
                 'MIC', 'NAH', 'HAB', 'ZEP', 'HAG', 'ZEC', 'MAL',
                 # Deuterocanônicos
                 '1ES', 'TOB', 'JDT', '1MC', '2MC', '3MC', '4MC', 'WIS', 
                 'SIR', 'BAR', 'EJR', 'SUS', 'BEL', 'ODE', 'PSS']
    
    placeholders = ','.join(['?' for _ in lxx_books])
    cursor.execute(f"""
        SELECT COUNT(*) FROM verses 
        WHERE grc IS NOT NULL AND book IN ({placeholders})
    """, lxx_books)
    lxx_grc_count = cursor.fetchone()[0]
    print(f"  LXX (AT) com grego: {lxx_grc_count}")
    
    conn.close()
    
    print("\nLXX carregada com sucesso!")
    print("Você pode consultar com: python query.py")

if __name__ == "__main__":
    test_lxx()
