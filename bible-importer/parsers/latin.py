import sqlite3
from typing import Dict, Tuple

# Mapeamento: número do livro na Vulgata → código OSIS (todos os 66 livros)
VUL_TO_OSIS = {
    1:"GEN", 2:"EXO", 3:"LEV", 4:"NUM", 5:"DEU",
    6:"JOS", 7:"JDG", 8:"RUT", 9:"1SA", 10:"2SA",
    11:"1KI", 12:"2KI", 13:"1CH", 14:"2CH", 15:"EZR",
    16:"NEH", 17:"EST", 18:"JOB", 19:"PSA", 20:"PRO",
    21:"ECC", 22:"SNG", 23:"ISA", 24:"JER", 25:"LAM",
    26:"EZK", 27:"DAN", 28:"HOS", 29:"JOL", 30:"AMO",
    31:"OBA", 32:"JON", 33:"MIC", 34:"NAH", 35:"HAB",
    36:"ZEP", 37:"HAG", 38:"ZEC", 39:"MAL",
    40:"MAT", 41:"MRK", 42:"LUK", 43:"JHN", 44:"ACT",
    45:"ROM", 46:"1CO", 47:"2CO", 48:"GAL", 49:"EPH",
    50:"PHP", 51:"COL", 52:"1TH", 53:"2TH", 54:"1TI",
    55:"2TI", 56:"TIT", 57:"PHM", 58:"HEB", 59:"JAS",
    60:"1PE", 61:"2PE", 62:"1JN", 63:"2JN", 64:"3JN",
    65:"JUD", 66:"REV"
}

def load(path: str) -> Dict[Tuple[str, int, int], str]:
    """
    Carrega Vulgata de arquivo SQL.
    Retorna {(book_osis, chapter, verse): texto}
    """
    # Tenta conectar ao arquivo SQL
    try:
        conn = sqlite3.connect(path)
        rows = conn.execute("SELECT b, c, v, t FROM t_vul").fetchall()
        conn.close()
    except Exception as e:
        print(f"Aviso: Não foi possível ler Vulgata de {path}: {e}")
        return {}
    
    result = {}
    for b, c, v, t in rows:
        if b in VUL_TO_OSIS and t:
            key = (VUL_TO_OSIS[b], c, v)
            result[key] = t
    
    return result
