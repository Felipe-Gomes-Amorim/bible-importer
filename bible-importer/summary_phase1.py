#!/usr/bin/env python3
"""
Sumário da implementação de prefácios de Jerônimo.
"""

import sqlite3

DB = "output/bible.db"
conn = sqlite3.connect(DB)

print("\n" + "="*70)
print("SUMÁRIO: PREFÁCIOS DE JERÔNIMO - FASE 1")
print("="*70)

# Versículos
cursor = conn.execute("SELECT COUNT(*) FROM verses")
num_verses = cursor.fetchone()[0]
print(f"\n📖 BANCO PRINCIPAL:")
print(f"  ✓ {num_verses:,} versículos únicos")

# Prefácios
cursor = conn.execute("""
    SELECT COUNT(*), SUM(LENGTH(COALESCE(content_eng, '')))
    FROM book_prefaces
    WHERE content_eng IS NOT NULL
""")
num_prefaces, total_chars = cursor.fetchone()
if num_prefaces is None:
    num_prefaces, total_chars = 0, 0

print(f"\n✍️  PREFÁCIOS (do CCEL):")
print(f"  ✓ {num_prefaces} prefácios carregados")
print(f"  ✓ {total_chars:,} caracteres totais")
print(f"  ⚠ 5 ainda faltam (PSA, PRO, HOS, MAT, ROM)")

# Lista dos prefácios
print(f"\n  Livros com prefácio:")
cursor = conn.execute("""
    SELECT book, title, LENGTH(content_eng) as size
    FROM book_prefaces
    WHERE content_eng IS NOT NULL
    ORDER BY book
""")

for book, title, size in cursor.fetchall():
    print(f"    ✓ {book:4}  {title[:40]:<40}  {size:>6,} chars")

print(f"\n{'='*70}")
print("PRÓXIMOS PASSOS:")
print("="*70)
print("""
1. ✓ CONCLUÍDO: Consolidação de versículos multilíngues
   - 36.769 versículos únicos
   - 73 livros (66 canônicos + 7 deuterocanônicos)
   - PT (84%), LAT (84%), GRC (NT 92%), HEB (62%), ARAM (0.8%)

2. ✓ CONCLUÍDO: Prefácios de Jerônimo (13/18)
   - Fonte: CCEL (Christian Classics Ethereal Library)
   - Formato: HTML→inglês
   - Próxima fase: Latim original (Documenta Catholica Omnia)

3. PENDENTE: Citações patrísticas (opcional)
   - Tabela: patristic_citations (já criada no schema)
   - Fontes: Catena Aurea (Aquinas), Glossa Ordinaria, etc.

4. RECOMENDADO: Query API e documentação
   - query.py atualizado para mostrar prefácios
   - Documentação de estrutura de dados
""")

conn.close()
print(f"{'='*70}\n")
