#!/usr/bin/env python3
"""
Scraper de prefácios de Jerônimo do catholiclibrary.org.
Usa Selenium para renderizar JavaScript e BeautifulSoup para parsing.
"""

import sys
import time

print("Verificando dependências...")

try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    print("✓ Selenium disponível")
except ImportError:
    print("✗ Selenium não encontrado. Instalando...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "selenium"])
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    print("✓ Selenium instalado")

try:
    from bs4 import BeautifulSoup
    print("✓ BeautifulSoup disponível")
except ImportError:
    print("✗ BeautifulSoup não encontrado")
    sys.exit(1)

# Mapeamento de chunk_id para livros
CHUNK_BOOK_MAP = {
    '00000001': ('GEN', 'Genesis'),
    '00000002': ('EXO', 'Exodus'),
    '00000003': ('LEV', 'Leviticus'),
    '00000004': ('NUM', 'Numbers'),
    '00000005': ('DEU', 'Deuteronomy'),
    '00000006': ('JOS', 'Joshua'),
    '00000007': ('JDG', 'Judges'),
    '00000008': ('RUT', 'Ruth'),
    '00000009': ('1SA', '1 Samuel'),
    '00000010': ('2SA', '2 Samuel'),
    '00000011': ('1KI', '1 Kings'),
    '00000012': ('2KI', '2 Kings'),
    '00000013': ('1CH', '1 Chronicles'),
    '00000014': ('2CH', '2 Chronicles'),
    '00000015': ('EZR', 'Ezra'),
    '00000016': ('NEH', 'Nehemiah'),
    '00000017': ('TOB', 'Tobit'),
    '00000018': ('JDT', 'Judith'),
    '00000019': ('EST', 'Esther'),
    '00000020': ('JOB', 'Job'),
    '00000021': ('PSA', 'Psalms'),
    '00000022': ('PRO', 'Proverbs'),
}

def scrape_preface_chunk(chunk_id):
    """Scrapes um prefácio individual usando Selenium."""
    
    url = f"https://catholiclibrary.org/library/view?docId=Fathers-EN/Jerome.PrefacesVulgate.en.html&chunk.id={chunk_id}"
    
    print(f"\n  Scraping chunk {chunk_id}...", end=" ")
    
    # Inicia webdriver (requer geckodriver ou chromedriver)
    try:
        # Tenta usar Firefox (mais common)
        driver = webdriver.Firefox()
    except:
        try:
            # Fallback para Chrome
            driver = webdriver.Chrome()
        except:
            print("✗ WebDriver não disponível (Firefox ou Chrome)")
            return None
    
    try:
        driver.get(url)
        
        # Aguarda carregamento do conteúdo (máximo 10 segundos)
        WebDriverWait(driver, 10).until(
            lambda d: d.find_elements(By.TAG_NAME, "p") and 
                      len(d.find_elements(By.TAG_NAME, "p")) > 0
        )
        
        time.sleep(1)  # Aguarda renderização extra
        
        # Parse com BeautifulSoup
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        # Extrai conteúdo (adaptado para a estrutura da página)
        content_divs = soup.find_all('div', class_=lambda x: x and 'content' in x.lower())
        
        if not content_divs:
            # Tenta extrar todo texto de parágrafos
            paragraphs = soup.find_all('p')
            content = '\n\n'.join([p.get_text() for p in paragraphs if p.get_text().strip()])
        else:
            content = '\n\n'.join([div.get_text() for div in content_divs])
        
        if content.strip():
            print("✓ Extraído")
            return content
        else:
            print("⚠ Vazio")
            return None
            
    except Exception as e:
        print(f"✗ Erro: {e}")
        return None
    finally:
        driver.quit()

def main():
    print("\nScraper de Prefácios de Jerônimo")
    print("="*70)
    print("\nAviso: Este scraper requer geckodriver (Firefox) ou chromedriver (Chrome)")
    print("Instalados e no PATH do sistema.")
    print("\nNota: O scraping longo pode ser lento. Para teste, vamos fazer apenas Genesis.")
    
    chunk_id = '00000001'  # Genesis
    if chunk_id in CHUNK_BOOK_MAP:
        osis_code, book_name = CHUNK_BOOK_MAP[chunk_id]
        print(f"\nTestando com {book_name} ({osis_code})...")
        
        content = scrape_preface_chunk(chunk_id)
        if content:
            print(f"\n✓ Prefácio de {book_name} extraído com sucesso!")
            print(f"  Tamanho: {len(content)} caracteres")
            print(f"\n  Primeiros 200 chars:\n  {content[:200]}...")

if __name__ == "__main__":
    main()
