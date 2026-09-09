#!/usr/bin/env python3
"""
Script de validação da importação.
Verifica cobertura de cada língua e integridade dos dados.
"""

import sqlite3

DB_PATH = "output/bible.db"

def validate():
    """Realiza validações no banco de dados."""
    
    try:
        conn = sqlite3.connect(DB_PATH)
    except Exception as e:
        print(f"✗ Erro ao conectar ao banco: {e}")
        return

    print("=" * 60)
    print("Validação do banco de dados bíblico")
    print("=" * 60)
    
    # Total de versículos
    total = conn.execute("SELECT COUNT(*) FROM verses").fetchone()[0]
    print(f"\nTotal de versículos: {total}\n")
    
    # Cobertura por língua
    print("Cobertura por língua:")
    for col in ["pt", "lat", "grc", "heb", "aram"]:
        count = conn.execute(f"SELECT COUNT(*) FROM verses WHERE {col} IS NOT NULL").fetchone()[0]
        percent = (count / total * 100) if total > 0 else 0
        print(f"  {col.upper():5s}: {count:6d} versículos ({percent:5.1f}%)")
    
    # Versículos no NT sem grego (não deveria ter muitos)
    print("\n⚠ Controles de qualidade:")
    
    nt_books = ('MAT','MRK','LUK','JHN','ACT','ROM','1CO','2CO',
                'GAL','EPH','PHP','COL','1TH','2TH','1TI','2TI',
                'TIT','PHM','HEB','JAS','1PE','2PE','1JN','2JN','3JN','JUD','REV')
    
    nt_without_grc = conn.execute(f"""
        SELECT COUNT(*) FROM verses
        WHERE book IN ({','.join('?' * len(nt_books))})
        AND grc IS NULL
    """, nt_books).fetchone()[0]
    
    if nt_without_grc > 0:
        print(f"  ⚠ Versículos NT sem grego: {nt_without_grc}")
    else:
        print(f"  ✓ Todos os versículos NT têm grego")
    
    # Amostra de dados
    print("\n📖 Amostra de dados (Mateus 1:1):")
    row = conn.execute(
        "SELECT pt, lat, grc, heb FROM verses WHERE book='MAT' AND chapter=1 AND verse=1"
    ).fetchone()
    
    if row:
        pt, lat, grc, heb = row
        print(f"  PT:  {pt[:60]}..." if pt else "  PT:  <vazio>")
        print(f"  LAT: {lat[:60]}..." if lat else "  LAT: <vazio>")
        print(f"  GRC: {grc[:60]}..." if grc else "  GRC: <vazio>")
        print(f"  HEB: {heb[:60]}..." if heb else "  HEB: <vazio>")
    else:
        print("  ✗ Mateus 1:1 não encontrado")
    
    # Livros presentes
    print("\nLivros presentes:")
    books = conn.execute(
        "SELECT DISTINCT book FROM verses ORDER BY book"
    ).fetchall()
    books_list = [b[0] for b in books]
    print(f"  {', '.join(books_list)}")
    print(f"  Total: {len(books_list)} livros")
    
    conn.close()
    print("\n" + "=" * 60)

if __name__ == "__main__":
    validate()
