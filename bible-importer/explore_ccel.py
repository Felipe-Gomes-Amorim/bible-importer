import requests
from bs4 import BeautifulSoup
import time

url = "https://catholiclibrary.org/library/view?docId=Fathers-EN/Jerome.PrefacesVulgate.en.html&chunk.id=00000001"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

print("Conectando ao catholiclibrary.org...")
try:
    r = requests.get(url, timeout=15, headers=headers)
    print(f"Status: {r.status_code}")
    
    if r.status_code == 200:
        soup = BeautifulSoup(r.text, 'html.parser')
        
        # Procura por elementos principais
        print("\nElementos encontrados:")
        print(f"  Title: {soup.title.string if soup.title else 'N/A'}")
        
        # Procura por divs com conteúdo
        main_content = soup.find('div', class_=['main-content', 'content', 'body'])
        if main_content:
            print(f"  Main content div: encontrado")
            print(f"    Primeiros 500 chars: {str(main_content)[:500]}...")
        else:
            print(f"  Main content: não encontrado")
            
        # Procura por spans, paragrafos, etc
        p_tags = soup.find_all('p')
        print(f"  Parágrafos: {len(p_tags)}")
        if p_tags:
            print(f"    Primeiro parágrafo: {p_tags[0].get_text()[:100]}...")
        
        # Procura por estrutura HTML bruta
        print(f"\nPrimeiros 2000 chars do HTML:")
        print(r.text[:2000])
    else:
        print(f"Erro HTTP: {r.status_code}")
        
except Exception as e:
    print(f"Erro: {e}")
