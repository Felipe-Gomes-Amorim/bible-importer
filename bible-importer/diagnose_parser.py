import os
import sys

# Carrega dados diretamente dos parsers ANTES da consolidação
from parsers import hebrew, portuguese, vulgate, greek

print("="*70)
print("DIAGNÓSTICO: Verificando origem da duplicata")
print("="*70)

# Carrega hebraico
heb_path = "data/morphhb/wlc"
heb, aram = hebrew.load(heb_path)

# Procura por chaves estranhas
print("\nHebraico carregado do parser:")
print(f"  Total de versículos: {len(heb)}")

# Ver se tem 1CO em heb
heb_1co = [(k, v[:50]) for k, v in heb.items() if k[0] == '1CO']
print(f"\n  Versículos com chave '1CO': {len(heb_1co)}")

if heb_1co:
    print("  ✗ PROBLEMA ENCONTRADO - Parser hebraico tem dados para 1CO!")
    for (book, ch, v), text in heb_1co[:5]:
        print(f"    ({book}, {ch}, {v}): {text}...")
else:
    print("  ✓ OK - Parser hebraico não tem dados para 1CO")

# Procura PSA
heb_psa = [(k, v[:50]) for k, v in heb.items() if k[0] == 'PSA' and k[1:] == (1, slice(1, 6))]
heb_psa = [(k, v[:50]) for k, v in heb.items() if k[0] == 'PSA' and k[1] == 1 and 1 <= k[2] <= 5]
print(f"\n  Versículos PSA 1:1-5: {len(heb_psa)}")
for (book, ch, v), text in heb_psa[:5]:
    print(f"    ({book}, {ch}, {v}): {text}...")

# Procura por PS (antes de normalizar)
heb_ps = [(k, v[:50]) for k, v in heb.items() if k[0] == 'PS']
print(f"\n  Versículos com chave 'PS': {len(heb_ps)}")
if heb_ps:
    print("  ⚠ Encontradas chaves 'PS' (deveriam ser 'PSA')")
    for (book, ch, v), text in heb_ps[:3]:
        print(f"    ({book}, {ch}, {v}): {text}...")
