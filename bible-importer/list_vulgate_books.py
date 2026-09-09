import json

with open('bible_databases/sources/la/Vulgate/Vulgate.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Listar todos os livros
print("Todos os livros no Vulgate.json:")
for i, book in enumerate(data['books']):
    name = book.get('name', 'N/A')
    chapters = len(book.get('chapters', []))
    print(f"{i:2d}: {name:30s} ({chapters} chapters)")
