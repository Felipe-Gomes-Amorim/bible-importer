import os
import re
from typing import Dict, Tuple

# Mapeia nome do arquivo .txt → código OSIS (formatos SBLGNT)
FILE_TO_OSIS = {
    # Formato: NN-XX-morphgnt.txt ou NN-XXx-morphgnt.txt
    "61-Mt-morphgnt.txt": "MAT",
    "62-Mk-morphgnt.txt": "MRK",
    "63-Lk-morphgnt.txt": "LUK",
    "64-Jn-morphgnt.txt": "JHN",
    "65-Ac-morphgnt.txt": "ACT",
    "66-Ro-morphgnt.txt": "ROM",
    "67-1Co-morphgnt.txt": "1CO",
    "68-2Co-morphgnt.txt": "2CO",
    "69-Ga-morphgnt.txt": "GAL",
    "70-Eph-morphgnt.txt": "EPH",
    "71-Php-morphgnt.txt": "PHP",
    "72-Col-morphgnt.txt": "COL",
    "73-1Th-morphgnt.txt": "1TH",
    "74-2Th-morphgnt.txt": "2TH",
    "75-1Ti-morphgnt.txt": "1TI",
    "76-2Ti-morphgnt.txt": "2TI",
    "77-Tit-morphgnt.txt": "TIT",
    "78-Phm-morphgnt.txt": "PHM",
    "79-Heb-morphgnt.txt": "HEB",
    "80-Jas-morphgnt.txt": "JAS",
    "81-1Pe-morphgnt.txt": "1PE",
    "82-2Pe-morphgnt.txt": "2PE",
    "83-1Jn-morphgnt.txt": "1JN",
    "84-2Jn-morphgnt.txt": "2JN",
    "85-3Jn-morphgnt.txt": "3JN",
    "86-Jud-morphgnt.txt": "JUD",
    "87-Re-morphgnt.txt": "REV",
}

def load(directory: str) -> Dict[Tuple[str, int, int], str]:
    """
    Carrega grego SBLGNT de arquivos .txt (formato morphgnt).
    Cada linha é: XXYYZZ POS MORPHOLOGY WORD1 WORD2 ...
    Onde XX=cap, YY=vers, ZZ=palavra sequencial
    Retorna {(book_osis, chapter, verse): texto}
    """
    result = {}
    
    for filename, book_code in FILE_TO_OSIS.items():
        filepath = os.path.join(directory, filename)
        if not os.path.exists(filepath):
            continue
        
        try:
            with open(filepath, encoding='utf-8') as f:
                verse_data = {}  # {(c, v): [words]}
                
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    
                    parts = line.split()
                    if len(parts) < 4:
                        continue
                    
                    ref_str = parts[0]
                    
                    # Extrai capítulo, versículo e posição da palavra
                    # Formato: XXYYZZ onde XX=livro, YY=capítulo, ZZ=versículo
                    try:
                        c = int(ref_str[2:4])
                        v = int(ref_str[4:6])
                    except (ValueError, IndexError):
                        continue
                    
                    # A palavra grega é o 4º campo (após ref, POS, morphology)
                    word = parts[3] if len(parts) > 3 else ""
                    
                    if not word:
                        continue
                    
                    key = (c, v)
                    if key not in verse_data:
                        verse_data[key] = []
                    verse_data[key].append(word)
                
                # Consolida versículos
                for (c, v), words in verse_data.items():
                    text = " ".join(words).strip()
                    if text:
                        result[(book_code, c, v)] = text
        
        except Exception as e:
            print(f"Erro ao ler {filename}: {e}")
    
    return result
