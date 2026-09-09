import xml.etree.ElementTree as ET
import os
from typing import Dict, Tuple

# Namespaces usados nos XMLs
OSIS_NS = "http://www.bibletechnologies.net/2003/OSIS/namespace"

# Livros com partes em Aramaico
ARAMAIC_RANGES = {
    "DAN": [(2, 4, 7, 28)],      # Daniel 2:4 – 7:28
    "EZR": [(4, 8, 6, 18), (7, 12, 7, 26)],  # Esdras 4:8–6:18, 7:12-26
}

def is_aramaic_verse(book: str, chapter: int, verse: int) -> bool:
    """Verifica se um versículo é aramaico baseado em ranges conhecidos."""
    if book not in ARAMAIC_RANGES:
        return False
    
    for start_c, start_v, end_c, end_v in ARAMAIC_RANGES[book]:
        # Versículo dentro do range?
        if chapter > start_c and chapter < end_c:
            return True
        if chapter == start_c and verse >= start_v:
            return True
        if chapter == end_c and verse <= end_v:
            return True
        if chapter == start_c and chapter == end_c:
            return verse >= start_v and verse <= end_v
    
    return False

def load(directory: str) -> Tuple[Dict[Tuple[str, int, int], str], Dict[Tuple[str, int, int], str]]:
    """
    Carrega hebraico e aramaico de arquivos XML do OSHB.
    Retorna ({heb}, {aram})
    """
    heb, aram = {}, {}
    
    if not os.path.exists(directory):
        print(f"Aviso: Diretório {directory} não encontrado")
        return heb, aram
    
    for filename in os.listdir(directory):
        if not filename.endswith(".xml"):
            continue
        
        try:
            filepath = os.path.join(directory, filename)
            tree = ET.parse(filepath)
            root = tree.getroot()
            
            # Busca por todos os elementos "verse" com namespace
            for verse_elem in root.iter(f"{{{OSIS_NS}}}verse"):
                osisID = verse_elem.get("osisID", "")
                if not osisID:
                    continue
                
                # osisID = "1Chr.1.1"
                parts = osisID.split(".")
                if len(parts) < 3:
                    continue
                
                book_raw = parts[0]
                c_str = parts[1]
                v_str = parts[2]
                
                # Mapeia nomes para OSIS
                # 1Chr → 1CH, Genesis → GEN, etc.
                book_map = {
                    "Genesis": "GEN", "Exodus": "EXO", "Leviticus": "LEV",
                    "Numbers": "NUM", "Deuteronomy": "DEU", "Joshua": "JOS",
                    "Judges": "JDG", "Ruth": "RUT", "1Samuel": "1SA", "2Samuel": "2SA",
                    "1Kings": "1KI", "2Kings": "2KI", "1Chronicles": "1CH",
                    "2Chronicles": "2CH", "Ezra": "EZR", "Nehemiah": "NEH",
                    "Esther": "EST", "Job": "JOB", "Psalms": "PSA", "Proverbs": "PRO",
                    "Ecclesiastes": "ECC", "SongOfSongs": "SNG", "Isaiah": "ISA",
                    "Jeremiah": "JER", "Lamentations": "LAM", "Ezekiel": "EZK",
                    "Daniel": "DAN", "Hosea": "HOS", "Joel": "JOL", "Amos": "AMO",
                    "Obadiah": "OBA", "Jonah": "JON", "Micah": "MIC", "Nahum": "NAH",
                    "Habakkuk": "HAB", "Zephaniah": "ZEP", "Haggai": "HAG",
                    "Zechariah": "ZEC", "Malachi": "MAL",
                    # Abreviações
                    "1Chr": "1CH", "2Chr": "2CH", "1Sam": "1SA", "2Sam": "2SA",
                    "1Kgs": "1KI", "2Kgs": "2KI", "1Ki": "1KI", "2Ki": "2KI",
                    "Judg": "JDG", "Ps": "PSA",
                }
                
                book_code = book_map.get(book_raw, book_raw.upper()[:3])
                
                try:
                    c, v = int(c_str), int(v_str)
                except ValueError:
                    continue
                
                # Concatena todas as palavras do versículo
                words = []
                for elem in verse_elem.iter():
                    if elem.text and elem.text.strip():
                        words.append(elem.text.strip())
                text = " ".join(words)
                
                if not text:
                    continue
                
                key = (book_code, c, v)
                
                # Decide se é hebraico ou aramaico
                if is_aramaic_verse(book_code, c, v):
                    aram[key] = text
                else:
                    heb[key] = text
        
        except Exception as e:
            print(f"Erro ao processar {filename}: {e}")
    
    return heb, aram
