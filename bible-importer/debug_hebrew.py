#!/usr/bin/env python3
"""Debug do parser de hebraico"""

from parsers import hebrew
import os

heb_dir = "data/morphhb/wlc"

print(f"\nDebugando hebraico em: {heb_dir}")
print("=" * 70)

heb, aram = hebrew.load(heb_dir)

print(f"\nHebraico carregado: {len(heb)} versículos")
print(f"Aramaico carregado: {len(aram)} versículos")

# Mostra alguns exemplos
print("\nPrimeiros 5 versículos hebraico:")
for key, text in list(heb.items())[:5]:
    book, ch, v = key
    preview = text[:60] if text else "<vazio>"
    print(f"  {book} {ch}:{v} → {preview}")

print("\nPrimeiros 5 versículos aramaico:")
for key, text in list(aram.items())[:5]:
    book, ch, v = key
    preview = text[:60] if text else "<vazio>"
    print(f"  {book} {ch}:{v} → {preview}")

# Tenta específico
print("\nBuscando GEN 1:1:")
if ("GEN", 1, 1) in heb:
    print(f"  ✓ Encontrado: {heb[('GEN', 1, 1)][:80]}")
else:
    print(f"  ✗ Não encontrado")
    print(f"    Chaves GEN disponíveis: {[k for k in heb.keys() if k[0] == 'GEN'][:3]}")
