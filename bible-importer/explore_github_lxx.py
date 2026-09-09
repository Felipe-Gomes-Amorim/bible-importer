#!/usr/bin/env python3
"""
Explora a estrutura da LXX do repositório GitHub de Eliran Wong.
"""

import requests
import json

def explore_github_folder(owner="eliranwong", repo="LXX-Rahlfs-1935", folder="11_end-users_files"):
    """Explora uma pasta específica do GitHub recursivamente."""
    
    def list_contents(path=""):
        """Lista o conteúdo de uma pasta recursivamente."""
        url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}".rstrip('/')
        print(f"\nAcessando: {url}")
        
        try:
            r = requests.get(url, timeout=10)
            if r.status_code == 200:
                items = r.json()
                if isinstance(items, list):
                    for item in items[:50]:  # Limita a 50 itens
                        name = item['name']
                        dtype = item['type']
                        size_kb = item.get('size', 0) / 1024
                        
                        if dtype == 'dir':
                            print(f"  📁 {name}/")
                        else:
                            print(f"  📄 {name} ({size_kb:.1f} KB)")
                            # Se for um arquivo pequeno, mostra a URL de raw content
                            if size_kb < 500:
                                print(f"     URL: {item['download_url']}")
                else:
                    print(f"    Item individual: {items.get('name')}")
            else:
                print(f"  Erro: {r.status_code}")
                print(f"  Resposta: {r.text[:200]}")
        except Exception as e:
            print(f"  Erro: {e}")
    
    print("="*70)
    print(f"Explorando: {owner}/{repo}")
    print("="*70)
    
    # Explora a pasta raiz
    print(f"\n📂 Pasta: /{folder}")
    list_contents(folder)
    
    # Explora algumas subpastas importantes
    for subfolder in [
        "11_end-users_files",
        "11_end-users_files/Bible",
        "11_end-users_files/Bible/LXX",
    ]:
        try:
            print(f"\n📂 Subpasta: /{subfolder}")
            list_contents(subfolder)
        except:
            pass

def download_sample_file(url):
    """Tenta baixar um arquivo de exemplo para inspecionar."""
    print(f"\n{'='*70}")
    print(f"Tentando baixar arquivo de exemplo...")
    print(f"{'='*70}")
    
    try:
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            print(f"✓ Sucesso! {len(r.text)} caracteres")
            print(f"\nPrimeiras 1000 caracteres:")
            print(r.text[:1000])
        else:
            print(f"✗ Erro: {r.status_code}")
    except Exception as e:
        print(f"✗ Erro: {e}")

if __name__ == "__main__":
    # Explora a estrutura
    explore_github_folder()
    
    # Se encontrar um arquivo de exemplo, tenta baixá-lo
    print(f"\n{'='*70}")
    print("Próximos passos:")
    print("- Explorar estrutura de dados da LXX")
    print("- Criar parser com base na estrutura encontrada")
    print("- Integrar ao banco de dados")
    print("="*70)
