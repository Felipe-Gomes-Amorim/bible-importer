from parsers import portuguese, vulgate, greek, hebrew
import sqlite3

# Carrega todos os dados
pt = portuguese.load("data/biblia/json/aa.json")
lat = vulgate.load("bible_databases/sources/la/Vulgate/Vulgate.json")
grc = greek.load("sblgnt")
heb, aram = hebrew.load("data/morphhb/wlc")

print("Dados carregados:")
print(f"  PT:   {len(pt)} versículos")
print(f"  LAT:  {len(lat)} versículos")
print(f"  GRC:  {len(grc)} versículos")
print(f"  HEB:  {len(heb)} versículos")
print(f"  ARAM: {len(aram)} versículos")

# Procura em heb por "PS"
ps_keys = [k for k in heb.keys() if k[0] == 'PS']
print(f"\nChaves 'PS' em heb: {len(ps_keys)}")

# Procura em lat por "1CO"
lat_1co = [k for k in lat.keys() if k[0] == '1CO']
print(f"Chaves '1CO' em lat: {len(lat_1co)}")

# Ver se há "1CO" em PT
pt_1co = [k for k in pt.keys() if k[0] == '1CO']
print(f"Chaves '1CO' em pt: {len(pt_1co)}")

# Simular a consolidação
NORMALIZE = {
    "PS": "PSA",
    "EZE": "EZK",
    "SON": "SNG",
}

def normalize_key(key):
    book, chap, vers = key
    book = NORMALIZE.get(book, book)
    return (book, chap, vers)

# Buscar todas as chaves
all_keys = set()
for dict_data in [pt, lat, grc, heb, aram]:
    for key in dict_data.keys():
        all_keys.add(normalize_key(key))

print(f"\nChaves únicos após normalização: {len(all_keys)}")

# Procurar (1CO, 1, 1)
target = ('1CO', 1, 1)
if target in all_keys:
    print(f"\n✓ {target} está em all_keys")
    
    # Buscar a origem
    print(f"\n  Origem em PT: {pt.get(target)}")
    print(f"  Origem em LAT: {lat.get(target)}")
    print(f"  Origem em GRC: {grc.get(target)}")
    print(f"  Origem em HEB: {heb.get(target)}")
    
    # Com a normalização invertida
    for norm_book, orig_book in [(k, v) for v, k in NORMALIZE.items()]:
        print(f"  HEB com fallback ({orig_book}, 1, 1): {heb.get((orig_book, 1, 1)) is not None}")
