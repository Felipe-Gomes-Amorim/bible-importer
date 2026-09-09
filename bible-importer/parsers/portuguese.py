import json
from typing import Dict, Tuple

def load(path: str) -> Dict[Tuple[str, int, int], str]:
    """
    Carrega português (Almeida) de JSON.
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
