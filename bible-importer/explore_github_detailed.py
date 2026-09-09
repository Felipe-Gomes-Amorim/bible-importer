#!/usr/bin/env python3
"""Exploração mais detalhada da estrutura LXX do GitHub."""

import requests

def explore(path):
    """Explora uma pasta do GitHub."""
    url = f"https://api.github.com/repos/eliranwong/LXX-Rahlfs-1935/contents/{path}".rstrip('/')
    print(f"\n{'='*70}")
    print(f"📂 {path}")
    print('='*70)
    
    try:
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            items = r.json() if isinstance(r.json(), list) else [r.json()]
            for item in items[:100]:
                name = item.get('name', '')
                dtype = item.get('type', '')
                size_kb = item.get('size', 0) / 1024
                
                if dtype == 'dir':
                    print(f"  📁 {name}/")
                else:
                    if size_kb > 1000:
                        print(f"  📄 {name} ({size_kb/1024:.1f} MB)")
                    else:
                        print(f"  📄 {name} ({size_kb:.1f} KB)")
        else:
            print(f"  Erro: {r.status_code}")
    except Exception as e:
        print(f"  Erro: {e}")

# Explora as pastas principais
explore("11_end-users_files/MyBible")
explore("11_end-users_files/e-Sword")

# Tenta ver o README
print("\n" + "="*70)
print("README.md - 11_end-users_files:")
print("="*70)
try:
    r = requests.get("https://raw.githubusercontent.com/eliranwong/LXX-Rahlfs-1935/master/11_end-users_files/README.md", timeout=10)
    if r.status_code == 200:
        print(r.text)
except Exception as e:
    print(f"Erro: {e}")
