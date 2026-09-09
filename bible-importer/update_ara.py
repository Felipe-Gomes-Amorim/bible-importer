#!/usr/bin/env python3
"""
Substitui a coluna 'pt' do banco com a versão ARA (Almeida Revista e Atualizada).
Mantém intactas as referências patrísticas, prefácios de Jerônimo e textos em latim/grego/hebraico.
"""

import sqlite3
import json
import os
from typing import Dict, Tuple

def load_ara(path: str) -> Dict[Tuple[str, int, int], str]:
    """
    Carrega ARA de JSON.
    Retorna {(book_osis, chapter, verse): texto}
    """
    with open(path, encoding='utf-8-sig') as f:
        data = json.load(f)
    
    # Mapeamento: índice do array → código OSIS
    book_codes = [
        "GEN","EXO","LEV","NUM","DEU","JOS","JDG","RUT",
        "1SA","2SA","1KI","2KI","1CH","2CH","EZR","NEH",
        "EST","JOB","PSA","PRO","ECC","SNG","ISA","JER",
        "LAM","EZK","DAN","HOS","JOL","AMO","OBA","JON",
        "MIC","NAH","HAB","ZEP","HAG","ZEC","MAL",
        "MAT","MRK","LUK","JHN","ACT","ROM","1CO","2CO",
        "GAL","EPH","PHP","COL","1TH","2TH","1TI","2TI",
        "TIT","PHM","HEB","JAS","1PE","2PE","1JN","2JN",
        "3JN","JUD","REV"
    ]
    
    result = {}
    for b_idx, book in enumerate(data):
        if b_idx >= len(book_codes):
            break
        book_code = book_codes[b_idx]
        
        # Estrutura: book pode ter "chapters" ou ser array direto
        chapters = book.get("chapters", book) if isinstance(book, dict) else book
        if isinstance(chapters, dict):
            chapters = chapters.get("chapters", [])
        
        for c_idx, chapter in enumerate(chapters, start=1):
            if isinstance(chapter, list):
                for v_idx, verse_text in enumerate(chapter, start=1):
                    if verse_text:
                        key = (book_code, c_idx, v_idx)
                        result[key] = verse_text
    
    return result

def main():
    db_path = "output/bible.db"
    ara_path = "ARA.json"
    
    if not os.path.exists(ara_path):
        print(f"ERRO: Arquivo {ara_path} não encontrado!")
        return
    
    if not os.path.exists(db_path):
        print(f"ERRO: Banco de dados {db_path} não encontrado!")
        return
    
    print("=" * 70)
    print("SUBSTITUINDO PORTUGUÊS PELO ARA")
    print("=" * 70)
    
    # Carregar ARA
    print("\n[1] Carregando ARA.json...")
    ara = load_ara(ara_path)
    print(f"    OK: {len(ara)} versículos carregados")
    
    # Conectar ao banco
    print("\n[2] Conectando ao banco de dados...")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Verificar quantos versículos existem
    cursor.execute("SELECT COUNT(*) FROM verses")
    total_verses = cursor.fetchone()[0]
    print(f"    OK: {total_verses} versículos no banco")
    
    # Atualizar coluna 'pt'
    print("\n[3] Atualizando coluna 'pt' com ARA...")
    updated = 0
    not_found = 0
    
    cursor.execute("SELECT book, chapter, verse FROM verses")
    all_verses = cursor.fetchall()
    
    for book, chapter, verse in all_verses:
        key = (book, chapter, verse)
        if key in ara:
            cursor.execute(
                "UPDATE verses SET pt = ? WHERE book = ? AND chapter = ? AND verse = ?",
                (ara[key], book, chapter, verse)
            )
            updated += 1
        else:
            not_found += 1
    
    conn.commit()
    
    print(f"    ✓ Atualizados: {updated} versículos")
    print(f"    ⚠ Não encontrados no ARA: {not_found} versículos (mantidos com versão anterior)")
    
    # Verificar integridade das referências patrísticas
    print("\n[4] Verificando referências patrísticas...")
    cursor.execute("SELECT COUNT(*) FROM patristic_refs")
    patristic_count = cursor.fetchone()[0]
    print(f"    ✓ Referências patrísticas preservadas: {patristic_count}")
    
    # Verificar prefácios
    print("\n[5] Verificando prefácios de Jerônimo...")
    cursor.execute("SELECT COUNT(*) FROM book_prefaces")
    prefaces_count = cursor.fetchone()[0]
    print(f"    ✓ Prefácios preservados: {prefaces_count}")
    
    # Verificar outros idiomas
    print("\n[6] Verificando outros idiomas...")
    cursor.execute("SELECT COUNT(*) FROM verses WHERE lat IS NOT NULL")
    lat_count = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM verses WHERE grc IS NOT NULL")
    grc_count = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM verses WHERE heb IS NOT NULL")
    heb_count = cursor.fetchone()[0]
    
    print(f"    ✓ Latim (Vulgata): {lat_count} versículos")
    print(f"    ✓ Grego (LXX/SBLGNT): {grc_count} versículos")
    print(f"    ✓ Hebraico: {heb_count} versículos")
    
    conn.close()
    
    print("\n" + "=" * 70)
    print("✓ SUBSTITUIÇÃO CONCLUÍDA COM SUCESSO!")
    print("=" * 70)
    print("\nResumo:")
    print(f"  • Português (ARA): {updated} versículos atualizados")
    print(f"  • Referências patrísticas: PRESERVADAS ({patristic_count})")
    print(f"  • Prefácios de Jerônimo: PRESERVADOS ({prefaces_count})")
    print(f"  • Latim/Grego/Hebraico: PRESERVADOS")

if __name__ == "__main__":
    main()
