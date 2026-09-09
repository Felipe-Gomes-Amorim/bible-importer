import json
with open('bible_databases/sources/la/Vulgate/Vulgate.json') as f:
    data = json.load(f)

for i in range(8, 14):
    book_name = data["books"][i]["name"]
    print(f'{i}: "{book_name}"')
