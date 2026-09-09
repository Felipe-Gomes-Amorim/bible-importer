import json

with open('bible_databases/sources/la/Vulgate/Vulgate.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Mostrar estrutura do JSON
print("Estrutura do Vulgate.json:")
print(f"  'books' é uma lista com {len(data['books'])} livros")
if data['books']:
    first_book = data['books'][0]
    print(f"  Primeiro livro: {first_book.get('name', 'N/A')}")
    print(f"  Keys: {list(first_book.keys())}")
    if 'chapters' in first_book and first_book['chapters']:
        first_chapter = first_book['chapters'][0]
        print(f"    Chapter keys: {list(first_chapter.keys())}")
        if 'verses' in first_chapter and first_chapter['verses']:
            first_verse = first_chapter['verses'][0]
            print(f"      Verse keys: {list(first_verse.keys())}")
            print(f"      Sample verse: {first_verse}")

# Procurar Samuel 1
print("\nProcurando livros problemáticos:")
for i, book in enumerate(data['books']):
    name = book.get('name', '')
    if any(x in name for x in ['1 Samuel', '2 Samuel', '1 Kings', '2 Kings', '1 Chronicles', '2 Chronicles']):
        print(f"  Index {i}: {name}")
        if 'chapters' in book:
            print(f"    Chapters: {len(book['chapters'])}")
            if book['chapters'] and book['chapters'][0].get('verses'):
                print(f"    First chapter verses: {len(book['chapters'][0]['verses'])}")
