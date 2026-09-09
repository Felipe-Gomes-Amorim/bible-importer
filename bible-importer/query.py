#!/usr/bin/env python3
"""
Script de consulta interativa do banco bíblico.
Permite buscar versículos por referência (ex: MAT 1:1 ou JHN 3:16)
"""

import sqlite3
import sys

DB_PATH = "output/bible.db"

# Mapeamento amigável → OSIS
BOOK_SHORTCUTS = {
    # AT
    "gn": "GEN", "ex": "EXO", "lv": "LEV", "nm": "NUM", "dt": "DEU",
    "js": "JOS", "jz": "JDG", "rt": "RUT",
    "1sm": "1SA", "2sm": "2SA", "1rs": "1KI", "2rs": "2KI",
    "1cr": "1CH", "2cr": "2CH", "ed": "EZR", "ne": "NEH",
    "et": "EST", "job": "JOB", "sl": "PSA", "pv": "PRO",
    "ec": "ECC", "ct": "SNG", "is": "ISA", "jr": "JER",
    "lm": "LAM", "ez": "EZK", "dn": "DAN",
    "os": "HOS", "jl": "JOL", "am": "AMO", "ob": "OBA",
    "jon": "JON", "mq": "MIC", "na": "NAH", "hc": "HAB",
    "sf": "ZEP", "ag": "HAG", "zc": "ZEC", "ml": "MAL",
    # NT
    "mt": "MAT", "mc": "MRK", "lc": "LUK", "jn": "JHN", "at": "ACT",
    "rm": "ROM", "1co": "1CO", "2co": "2CO", "gl": "GAL",
    "ef": "EPH", "fp": "PHP", "cl": "COL", "1ts": "1TH", "2ts": "2TH",
    "1tm": "1TI", "2tm": "2TI", "tt": "TIT", "fm": "PHM",
    "hb": "HEB", "tg": "JAS", "1pd": "1PE", "2pd": "2PE",
    "1jo": "1JN", "2jo": "2JN", "3jo": "3JN", "jd": "JUD", "ap": "REV",
}

def normalize_book(book_str: str) -> str:
    """Converte abreviação amigável para OSIS."""
    book_lower = book_str.lower().strip()
    
    # Tenta busca direta
    if book_lower in BOOK_SHORTCUTS:
        return BOOK_SHORTCUTS[book_lower]
    
    # Tenta como OSIS direto (3 letras maiúsculas)
    if len(book_lower) == 3 or len(book_lower) == 4:
        osis = book_lower.upper()
        return osis
    
    return None

def query_verse(book_osis: str, chapter: int, verse: int):
    """Busca um versículo específico."""
    try:
        conn = sqlite3.connect(DB_PATH)
        row = conn.execute(
            "SELECT pt, lat, grc, heb, aram FROM verses WHERE book=? AND chapter=? AND verse=?",
            (book_osis, chapter, verse)
        ).fetchone()
        conn.close()
        
        if not row:
            return None
        
        return {
            "pt": row[0],
            "lat": row[1],
            "grc": row[2],
            "heb": row[3],
            "aram": row[4],
        }
    except Exception as e:
        print(f"✗ Erro: {e}")
        return None

def query_chapter(book_osis: str, chapter: int):
    """Busca todos os versículos de um capítulo."""
    try:
        conn = sqlite3.connect(DB_PATH)
        rows = conn.execute(
            "SELECT verse, pt FROM verses WHERE book=? AND chapter=? ORDER BY verse",
            (book_osis, chapter)
        ).fetchall()
        conn.close()
        return rows
    except Exception as e:
        print(f"✗ Erro: {e}")
        return []

def query_preface(book_osis: str):
    """Busca prefácio de Jerônimo para um livro."""
    try:
        conn = sqlite3.connect(DB_PATH)
        row = conn.execute(
            "SELECT title, content_eng FROM book_prefaces WHERE book=? AND author='Jerome'",
            (book_osis,)
        ).fetchone()
        conn.close()
        
        if not row:
            return None
        
        return {
            "title": row[0],
            "content": row[1],
        }
    except Exception as e:
        # Silencia erros (tabela pode não existir)
        return None

def show_verse(book_osis: str, chapter: int, verse: int):
    """Exibe um versículo com formatação."""
    data = query_verse(book_osis, chapter, verse)
    if not data:
        print(f"\n✗ Versículo não encontrado: {book_osis} {chapter}:{verse}\n")
        return
    
    print(f"\n{'=' * 70}")
    print(f"{book_osis} {chapter}:{verse}")
    print(f"{'=' * 70}")
    
    for lang, text in [
        ("PORTUGUÊS", data["pt"]),
        ("LATIM", data["lat"]),
        ("GREGO", data["grc"]),
        ("HEBRAICO", data["heb"]),
        ("ARAMAICO", data["aram"]),
    ]:
        if text:
            print(f"\n{lang}:")
            print(f"  {text}")
    
    # Mostra prefácio se for o primeiro versículo do livro
    if chapter == 1 and verse == 1:
        preface = query_preface(book_osis)
        if preface:
            print(f"\n{'=' * 70}")
            print(f"PREFÁCIO DE JERÔNIMO: {preface['title']}")
            print(f"{'=' * 70}")
            print(f"\n{preface['content']}")
    
    print(f"\n{'=' * 70}\n")

def show_chapter(book_osis: str, chapter: int):
    """Exibe todos os versículos de um capítulo."""
    rows = query_chapter(book_osis, chapter)
    if not rows:
        print(f"\n✗ Capítulo não encontrado: {book_osis} {chapter}\n")
        return
    
    print(f"\n{'=' * 70}")
    print(f"{book_osis} {chapter}")
    print(f"{'=' * 70}\n")
    
    for verse, text in rows:
        if text:
            preview = text[:70] + "..." if len(text) > 70 else text
            print(f"{verse:3d}. {preview}")
    
    print(f"\n{'=' * 70}\n")

def interactive_mode():
    """Modo interativo."""
    print("\n" + "=" * 70)
    print("Consultor Bíblico Multilíngue")
    print("=" * 70)
    print("\nExemplos de uso:")
    print("  mat 1:1          → Mateus 1:1")
    print("  jn 3:16          → João 3:16")
    print("  mt 5              → Todo Mateus 5")
    print("  list             → Listar abreviações")
    print("  sair             → Sair")
    print()
    
    while True:
        try:
            user_input = input("📖 Buscar: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() == "sair":
                print("\nAté logo!\n")
                break
            
            if user_input.lower() == "list":
                print("\nAbreviações de livros:")
                for abbr, osis in sorted(BOOK_SHORTCUTS.items()):
                    print(f"  {abbr:6s} → {osis}")
                print()
                continue
            
            # Parse da entrada (ex: "mat 1:1" ou "mt 5")
            parts = user_input.split()
            if len(parts) < 2:
                print("❌ Formato: <livro> <capítulo>[:<versículo>]\n")
                continue
            
            book_str = parts[0]
            ref_str = parts[1]
            
            book_osis = normalize_book(book_str)
            if not book_osis:
                print(f"❌ Livro inválido: {book_str}\n")
                continue
            
            if ":" in ref_str:
                # Versículo específico
                try:
                    chapter, verse = map(int, ref_str.split(":"))
                    show_verse(book_osis, chapter, verse)
                except ValueError:
                    print("❌ Formato: capítulo:versículo (ex: 1:1)\n")
            else:
                # Capítulo completo
                try:
                    chapter = int(ref_str)
                    show_chapter(book_osis, chapter)
                except ValueError:
                    print("❌ Capítulo deve ser um número\n")
        
        except KeyboardInterrupt:
            print("\n\nAté logo!\n")
            break
        except Exception as e:
            print(f"\n❌ Erro: {e}\n")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Modo CLI: python query.py mat 1:1
        try:
            book_input = sys.argv[1]
            ref_input = sys.argv[2]
            
            book = normalize_book(book_input)
            if not book:
                print(f"❌ Livro inválido: {book_input}")
                sys.exit(1)
            
            if ":" in ref_input:
                c, v = map(int, ref_input.split(":"))
                show_verse(book, c, v)
            else:
                c = int(ref_input)
                show_chapter(book, c)
        except (ValueError, IndexError) as e:
            print(f"❌ Erro: {e}")
            print("Uso: python query.py <livro> <capítulo>[:<versículo>]")
            print("Ex:  python query.py mat 1:1")
            sys.exit(1)
    else:
        # Modo interativo
        interactive_mode()
