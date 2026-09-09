import requests
import json
import re

url = "https://catholiclibrary.org/library/view?docId=Fathers-EN/Jerome.PrefacesVulgate.en.html&chunk.id=00000001"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

r = requests.get(url, timeout=15, headers=headers)

# Procura por JSON data em script tags
patterns = [
    r'window\.__data\s*=\s*({.*?});',
    r'var\s+data\s*=\s*({.*?});',
    r'<script[^>]*>({.*?})</script>',
    r'"chunk\.id"\s*:\s*"([^"]*)"',
]

print("Procurando dados JSON embedados...\n")

# Procura por padrões específicos de catholiclibrary
matches = re.findall(r'data-c1id="([^"]*)"', r.text)
if matches:
    print(f"✓ Encontrado data-c1id: {matches[0]}")

# Procura por chunk ID
chunk_matches = re.findall(r'chunk\.id=([^&\s"\']*)', r.text)
if chunk_matches:
    print(f"✓ Encontrado chunk.id: {chunk_matches}")

# Procura por qualquer script com JSON
script_tags = re.findall(r'<script[^>]*>(.*?)</script>', r.text, re.DOTALL)
print(f"\nScript tags encontradas: {len(script_tags)}")

for i, script in enumerate(script_tags[:3]):
    if len(script) < 100:
        print(f"  Script {i+1}: {script[:100]}...")
    else:
        # Procura por JSON
        if '{' in script and '}' in script:
            print(f"  Script {i+1}: Contém JSON (tamanho: {len(script)})")
            # Tenta extrair JSON
            try:
                json_match = re.search(r'\{.*\}', script, re.DOTALL)
                if json_match:
                    data = json.loads(json_match.group())
                    print(f"    JSON válido encontrado!")
                    print(f"    Chaves: {list(data.keys())[:10]}")
            except:
                pass

print("\nProcurando por URLs de API...")
api_matches = re.findall(r'https?://[^\s"\'<>]+', r.text)
for api in set(api_matches):
    if 'api' in api.lower() or 'data' in api.lower() or 'json' in api.lower():
        print(f"  {api}")
