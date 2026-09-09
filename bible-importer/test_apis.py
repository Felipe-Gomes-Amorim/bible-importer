import requests

# Tenta acessar via diferentes endpoints possíveis

urls = [
    # Endpoint direto de chunk
    "https://catholiclibrary.org/library/view?docId=Fathers-EN/Jerome.PrefacesVulgate.en.html&chunk.id=00000001&format=json",
    # API XTF
    "https://catholiclibrary.org/library/api/v1/documents/Fathers-EN/Jerome.PrefacesVulgate.en.html/chunks/00000001",
    # Raw content
    "https://catholiclibrary.org/Fathers-EN/Jerome.PrefacesVulgate.en.html",
    # Possível endpoint de download
    "https://catholiclibrary.org/library/download?docId=Fathers-EN/Jerome.PrefacesVulgate.en.html",
]

headers = {"User-Agent": "Mozilla/5.0"}

for url in urls:
    print(f"\nTentando: {url}")
    try:
        r = requests.get(url, timeout=10, headers=headers)
        print(f"  Status: {r.status_code}")
        if r.status_code == 200:
            # Mostra primeiros 300 chars
            if 'xml' in r.headers.get('content-type', '').lower() or 'text' in r.headers.get('content-type', '').lower():
                print(f"  Content-Type: {r.headers.get('content-type')}")
                print(f"  Amostra: {r.text[:300]}...")
            else:
                print(f"  Content-Type: {r.headers.get('content-type')}")
    except Exception as e:
        print(f"  Erro: {e}")

# Tenta via CCEL original
print("\n" + "="*70)
print("Testando CCEL original (ccel.org):")
ccel_urls = [
    "https://ccel.org/ccel/pearse/morefathers/files/jerome_prologue_genesis.html",
    "https://ccel.org/ccel/jerome/prologue_vulgate_genesis.html",
]

for url in ccel_urls:
    print(f"\nTentando: {url}")
    try:
        r = requests.get(url, timeout=10, headers=headers)
        print(f"  Status: {r.status_code}")
        if r.status_code == 200:
            print(f"  ✓ Encontrado!")
            print(f"  Primeiros 500 chars: {r.text[:500]}...")
    except Exception as e:
        print(f"  Erro: {e}")
