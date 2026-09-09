import json
with open('bible_databases/sources/la/Vulgate/Vulgate.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
    books = [b['name'] for b in data['books']]
    print(f'Livros na Vulgata: {len(books)}')
    
    print('\nDeuterocanônicos:')
    search_terms = ['Tobias', 'Judith', 'Macabeus', 'Wisdom', 'Sirach', 'Baruch']
    for term in search_terms:
        found = [b for b in books if term.lower() in b.lower()]
        if found:
            print(f'  {term:12}: {found}')
    
    print('\nTodos os livros:')
    for i, b in enumerate(books, 1):
        print(f'  {i:2}. {b}')
