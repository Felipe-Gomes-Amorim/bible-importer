#!/usr/bin/env python3
"""
Explora fontes de LXX do Internet Archive e GitHub para integração ao banco.
"""

import requests
import json

# IDs do Internet Archive para as 3 fontes de LXX
IA_ITEMS = {
    "theoldtestamenti00unknuoft": "Swete Vol 1",
    "oldtestamenting02swet": "Swete Vol 2", 
    "oldtestgreek00unknuoft": "Rahlfs"
}

GITHUB_LXX_URL = "https://github.com/eliranwong/LXX-Rahlfs-1935"

def explore_ia_item(item_id):
    """Explora metadados de um item do Internet Archive."""
    print(f"\n{'='*60}")
    print(f"Explorando: {item_id}")
    print(f"{'='*60}")
    
    try:
        # API do Internet Archive retorna metadados em JSON
        metadata_url = f"https://archive.org/metadata/{item_id}"
        print(f"Buscando metadados...")
        
        r = requests.get(metadata_url, timeout=10)
        r.raise_for_status()
        
        metadata = r.json()
        
        # Informações gerais
        if 'metadata' in metadata:
            meta = metadata['metadata']
            print(f"Título: {meta.get('title', 'N/A')}")
            print(f"Criador: {meta.get('creator', 'N/A')}")
        
        # Arquivos disponíveis
        print("\nArquivos disponíveis:")
        if 'files' in metadata:
            files = metadata['files']
            
            # Trata como lista
            if isinstance(files, list):
                for finfo in files[:30]:  # Primeiros 30
                    fname = finfo.get('name', '')
                    if fname and not fname.startswith('_'):
                        size_mb = int(finfo.get('size', 0)) / (1024*1024)
                        fmt = finfo.get('format', 'unknown').lower()
                        print(f"  - {fname} ({size_mb:.1f} MB)")
                        if any(x in fmt for x in ['text', 'txt', 'xml', 'utf']):
                            url = f"https://archive.org/download/{item_id}/{fname}"
                            print(f"    ✓ TEXTO: {url}")
        
        return True
        
    except Exception as e:
        print(f"Erro: {e}")
        return False

def explore_github_lxx(url):
    """Explora o repositório GitHub de LXX."""
    print(f"\n{'='*60}")
    print(f"GitHub: {url}")
    print(f"{'='*60}")
    
    try:
        owner, repo = "eliranwong", "LXX-Rahlfs-1935"
        
        # Tenta acessar a API do GitHub
        api_url = f"https://api.github.com/repos/{owner}/{repo}"
        r = requests.get(api_url, timeout=10)
        
        if r.status_code == 200:
            info = r.json()
            print(f"Descrição: {info.get('description', 'N/A')}")
        
        # Tenta listar arquivos
        contents_url = f"https://api.github.com/repos/{owner}/{repo}/contents"
        r = requests.get(contents_url, timeout=10)
        
        if r.status_code == 200:
            contents = r.json()
            print(f"\nArquivos/pastas ({len(contents)} itens):")
            for item in contents[:20]:
                print(f"  - {item['name']} ({'dir' if item['type'] == 'dir' else 'file'})")
        else:
            print(f"Erro: {r.status_code}")
            
    except Exception as e:
        print(f"Erro: {e}")

def main():
    print("\n" + "="*60)
    print("EXPLORANDO FONTES DE LXX")
    print("="*60)
    
    # Explora cada item do Internet Archive
    for item_id, label in IA_ITEMS.items():
        print(f"\n>>> {label}")
        explore_ia_item(item_id)
    
    # Explora repositório GitHub
    explore_github_lxx(GITHUB_LXX_URL)
    
    print("\n" + "="*60)
    print("Exploração concluída!")
    print("="*60)

if __name__ == "__main__":
    main()
