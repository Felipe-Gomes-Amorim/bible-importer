import json
import os
from typing import Dict, Tuple

# Mapeamento: nome do livro → código OSIS
# Nota: JSON usa numerais romanos (I, II, III) para alguns livros
BOOK_MAP = {
    "Genesis": "GEN", "Exodus": "EXO", "Leviticus": "LEV", "Numbers": "NUM",
    "Deuteronomy": "DEU", "Joshua": "JOS", "Judges": "JDG", "Ruth": "RUT",
    # Suporta ambos: numerais arábicos (1 Samuel) e romanos (I Samuel)
    "1 Samuel": "1SA", "I Samuel": "1SA", 
    "2 Samuel": "2SA", "II Samuel": "2SA",
    "1 Kings": "1KI", "I Kings": "1KI", 
    "2 Kings": "2KI", "II Kings": "2KI",
    "1 Chronicles": "1CH", "I Chronicles": "1CH", 
    "2 Chronicles": "2CH", "II Chronicles": "2CH", 
    "Ezra": "EZR", "Nehemiah": "NEH",
    "Esther": "EST", "Job": "JOB", "Psalms": "PSA", "Proverbs": "PRO",
    "Ecclesiastes": "ECC", "Song of Solomon": "SNG", "Isaiah": "ISA", "Jeremiah": "JER",
    "Lamentations": "LAM", "Ezekiel": "EZK", "Daniel": "DAN", "Hosea": "HOS",
    "Joel": "JOL", "Amos": "AMO", "Obadiah": "OBA", "Jonah": "JON",
    "Micah": "MIC", "Nahum": "NAH", "Habakkuk": "HAB", "Zephaniah": "ZEP",
    "Haggai": "HAG", "Zechariah": "ZEC", "Malachi": "MAL",
    # Deuterocanônicos
    "Tobit": "TOB", "Judith": "JDT", "Wisdom": "WIS", "Sirach": "SIR", "Baruch": "BAR",
    "I Maccabees": "1MA", "II Maccabees": "2MA",
    # Novo Testamento
    "Matthew": "MAT", "Mark": "MRK", "Luke": "LUK", "John": "JHN",
    "Acts": "ACT", "Romans": "ROM", 
    "I Corinthians": "1CO", "II Corinthians": "2CO",
    "Galatians": "GAL", "Ephesians": "EPH", "Philippians": "PHP", "Colossians": "COL",
    "I Thessalonians": "1TH", "II Thessalonians": "2TH", "I Timothy": "1TI",
    "II Timothy": "2TI", "Titus": "TIT", "Philemon": "PHM", "Hebrews": "HEB",
    "James": "JAS", "I Peter": "1PE", "II Peter": "2PE", "I John": "1JN",
    "II John": "2JN", "III John": "3JN", "Jude": "JUD", "Revelation of John": "REV",
}

def load(json_path: str) -> Dict[Tuple[str, int, int], str]:
    """
    Carrega latim (Vulgata) de JSON no formato bible_databases.
    Retorna {(book_osis, chapter, verse): texto}
    """
    result = {}
    
    if not os.path.exists(json_path):
        return result
    
    try:
        with open(json_path, encoding='utf-8') as f:
            data = json.load(f)
        
        if "books" not in data or not isinstance(data["books"], list):
            return result
        
        for book_obj in data["books"]:
            if not isinstance(book_obj, dict):
                continue
            
            book_name = book_obj.get("name")
            book_osis = BOOK_MAP.get(book_name)
            if not book_osis:
                continue
            
            chapters = book_obj.get("chapters", [])
            if not isinstance(chapters, list):
                continue
            
            for chapter_obj in chapters:
                if not isinstance(chapter_obj, dict):
                    continue
                
                chapter = chapter_obj.get("chapter")
                if chapter is None:
                    try:
                        chapter = int(chapter)
                    except (ValueError, TypeError):
                        continue
                
                verses = chapter_obj.get("verses", [])
                if not isinstance(verses, list):
                    continue
                
                for verse_obj in verses:
                    if not isinstance(verse_obj, dict):
                        continue
                    
                    verse = verse_obj.get("verse")
                    verse_text = verse_obj.get("text", "").strip()
                    
                    if verse is not None and verse_text:
                        try:
                            verse = int(verse)
                        except (ValueError, TypeError):
                            continue
                        
                        key = (book_osis, chapter, verse)
                        result[key] = verse_text
    
    except Exception as e:
        print(f"Erro ao ler latim: {e}")
    
    return result
