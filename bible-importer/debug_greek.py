#!/usr/bin/env python3
import os
from parsers import greek

grc_dir = "sblgnt"
print(f"Testando grego em: {grc_dir}")
print(f"Existe? {os.path.exists(grc_dir)}")
print(f"É diretório? {os.path.isdir(grc_dir)}")

if os.path.exists(grc_dir):
    files = os.listdir(grc_dir)
    txt_files = [f for f in files if f.endswith('.txt')]
    print(f"Arquivos .txt encontrados: {len(txt_files)}")
    print(f"Primeiros: {txt_files[:3]}")
    
    grc = greek.load(grc_dir)
    print(f"\nGrego carregado: {len(grc)} versículos")
    
    if grc:
        sample_key = list(grc.keys())[0]
        print(f"Sample: {sample_key} → {grc[sample_key][:60]}")
