#!/usr/bin/env python3
import requests

url = "https://api.github.com/repos/eliranwong/LXX-Rahlfs-1935/contents/11_end-users_files/MyBible/Bibles"

try:
    r = requests.get(url, timeout=10)
    if r.status_code == 200:
        items = r.json() if isinstance(r.json(), list) else [r.json()]
        print(f"Encontrados {len(items)} itens:\n")
        for item in items:
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
        print(f"Erro: {r.status_code}")
except Exception as e:
    print(f"Erro: {e}")
