import requests
from bs4 import BeautifulSoup

url = "https://catholiclibrary.org/library/view?docId=Fathers-EN/Jerome.PrefacesVulgate.en.html&chunk.id=00000001"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

r = requests.get(url, timeout=15, headers=headers)
soup = BeautifulSoup(r.text, 'html.parser')

# Procura por divs específicas
print("Procurando estrutura de conteúdo...\n")

# Tenta encontrar divs com class contendo 'content', 'text', 'main', 'body'
divs = soup.find_all('div', class_=True)
print(f"Total de divs: {len(divs)}")

# Procura por divs com classes interessantes
interesting_classes = set()
for div in divs:
    for cls in div.get('class', []):
        if any(x in cls.lower() for x in ['content', 'text', 'body', 'main', 'chunk']):
            interesting_classes.add(cls)

print(f"Classes interessantes encontradas:")
for cls in sorted(interesting_classes):
    print(f"  - {cls}")

# Procura específica por conteúdo de texto
text_divs = soup.find_all('div', class_='page-break')
if text_divs:
    print(f"\n✓ Encontrado 'page-break' divs: {len(text_divs)}")
    if text_divs[0]:
        content = text_divs[0].get_text()
        print(f"  Primeiro: {content[:200]}...")

# Tenta outro padrão
text_sections = soup.find_all('div', {'class': lambda x: x and 'xtf' in x})
if text_sections:
    print(f"\n✓ Encontrado 'xtf' sections: {len(text_sections)}")

# Procura por iframes
iframes = soup.find_all('iframe')
print(f"\nIframes: {len(iframes)}")
if iframes:
    for i, iframe in enumerate(iframes[:3]):
        print(f"  {i+1}. src={iframe.get('src')}")
