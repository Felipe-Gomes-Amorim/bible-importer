import json

# Debug: verificar o que vem do JSON
with open('bible_databases/sources/la/Vulgate/Vulgate.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Procurar 1 Samuel (index 8)
book = data['books'][8]
print(f"Book: {book['name']}")

for i, chapter_obj in enumerate(book['chapters'][:2]):  # Primeiros 2 capítulos
    print(f"\nChapter object: {chapter_obj}")
    chapter = chapter_obj.get("chapter")
    print(f"  chapter value: {chapter}, type: {type(chapter)}")
    
    for verse_obj in chapter_obj['verses'][:2]:  # Primeiros 2 versos
        verse = verse_obj.get("verse")
        print(f"    verse value: {verse}, type: {type(verse)}")
