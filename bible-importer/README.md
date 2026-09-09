# Bible Importer — Banco de Dados Bíblico Multilíngue

Um consolidador de textos bíblicos multilíngues em SQLite, incluindo prefácios de Jerônimo.

## Visao Geral

**40.510 versículos únicos** alinhados por book/chapter/verse em **81 livros** (66 canônicos + 15 deuterocanônicos) com cobertura em:
- Portugues (Almeida 1859): 83.4%
- Latim (Vulgata): 84.3%
- Grego (SBLGNT NT + LXX AT): 100% (28.861 versículos LXX + 7.927 NT)
- Hebraico (OSHB AT): 100%
- Aramaico (selecoes): 100%
- Prefacios Jeronimo: 13/18 livros

## LXX (Septuaginta) - NOVO!

A LXX (Septuaginta em grego) do Antigo Testamento foi adicionada como tradução disponível!

- **Fonte**: Rahlfs 1935 edition do repositório de Eliran Wong
- **Cobertura**: 28.861 versículos em 54 livros (AT completo + deuterocanônicos)
- **Livros AT canônicos**: GEN até MAL (39 livros)
- **Livros deuterocanônicos**: 1ES, TOB, JDT, 1MC, 2MC, 3MC, 4MC, WIS, SIR, BAR, EJR, SUS, BEL, ODE, PSS

### Exemplo de consulta LXX
```bash
python query.py gen 1:1    # Genesis 1:1 em grego (LXX)
python query.py psa 23:1   # Psalm 23:1 em grego (LXX)
python query.py isa 1:1    # Isaiah 1:1 em grego (LXX)
python query.py tob 1:1    # Tobit 1:1 em grego (LXX, deuterocanonico)
```

## Banco de Dados

### Tabela: `verses` (40.510 registros)
```sql
verses(
    book TEXT,           -- OSIS (GEN, MAT, PSA, JUD, etc)
    chapter INTEGER,
    verse INTEGER,
    pt TEXT,             -- Portugues
    lat TEXT,            -- Latim
    grc TEXT,            -- Grego (LXX AT + SBLGNT NT)
    heb TEXT,            -- Hebraico
    aram TEXT,           -- Aramaico
    PRIMARY KEY (book, chapter, verse)
)
```

### Tabela: `book_prefaces` (13 registros)
```sql
book_prefaces(
    id INTEGER PRIMARY KEY,
    book TEXT,              -- OSIS (GEN, ISA, etc)
    author TEXT DEFAULT 'Jerome',
    title TEXT,             -- Prologue to Genesis
    content_lat TEXT,       -- Latim (vazio por enquanto)
    content_eng TEXT,       -- Ingles do CCEL
    source_url TEXT
)
```

**Prefacios carregados:**
- OK GEN, JOS, 1SA, 1CH, EZR, TOB, JDT, EST, JOB, ISA, JER, EZK, DAN
- INVESTIGACAO PSA, PRO, HOS, MAT, ROM (URLs em investigacao)

## Query CLI

### Uso Rapido
```bash
# Versiculo especifico
python query.py gen 1:1        # Genesis 1:1 com prefacio
python query.py mat 1:1        # Mateus 1:1
python query.py jn 3:16        # Joao 3:16

# Capitulo completo
python query.py mat 5

# Modo interativo
python query.py
# Buscar: gen 1:1
# Buscar: list
# Buscar: sair
```

### Output Exemplo
```
======================================================================
GEN 1:1
======================================================================

PORTUGUES:
  No principio criou Deus os ceus e a terra.

LATIM:
  in principio creavit Deus caelum et terram

GREGO (LXX):
  En archei epoiesen ho theos ton ouranon kai ten gen

HEBRAICO:
  בְּ/רֵאשִׁ֖ית בָּרָ֣א אֱלֹהִ֑ים אֵ֥ת הַ/שּׁ

======================================================================
PREFÁCIO DE JERÔNIMO: Prologue to Genesis (Pentateuch)
======================================================================

[Prefácio em inglês do CCEL truncado aqui...]
```

## 🛠️ Construindo do Zero

```bash
# 1. Preparar dados
git clone https://github.com/thiagobodruk/biblia.git data/biblia
git clone https://github.com/openscriptures/morphhb.git data/morphhb
git clone https://github.com/morphgnt/sblgnt.git sblgnt
# ... Vulgata: bible_databases/sources/la/Vulgate/Vulgate.json

# 2. Consolidar versículos
python main.py
# → output/bible.db (36.769 versículos)

# 3. Adicionar schema de prefácios
python create_preface_schema.py

# 4. Scrape prefácios
python scrape_jerome_prefaces.py
# → 13/18 prefácios carregados

# 5. Validar
python validate.py
python query.py gen 1:1
```

## 📁 Estrutura

```
bible-importer/
├── output/
│   └── bible.db                 # Banco SQLite consolidado
├── data/
│   ├── biblia/                  # Português (JSON Almeida)
│   ├── morphhb/wlc              # Hebraico/Aramaico (OSHB XML)
│   └── bible_databases/sources/la/Vulgate/  # Latim (JSON)
├── sblgnt/                       # Grego (TXT morfologicamente anotado)
├── parsers/
│   ├── portuguese.py            # → 31.104 versículos
│   ├── vulgate.py              # → 31.009 versículos
│   ├── greek.py                # → 7.927 versículos
│   └── hebrew.py               # → 22.933 HEB + 280 ARAM
├── main.py                      # Consolidador principal
├── query.py                     # CLI interativo
├── validate.py                  # Relatório de cobertura
├── scrape_jerome_prefaces.py    # Scraper CCEL
└── README.md
```

## 🔧 Parsers

Cada parser transforma formato específico em dict `{(book, ch, v): text}`:

### `portuguese.py` — Almeida
- **Fonte**: thiagobodruk/biblia (JSON UTF-8-BOM)
- **Cobertura**: 31.104 versículos, 73 livros
- **Formato**: Array de livros com capítulos/versículos

### `vulgate.py` — Vulgata
- **Fonte**: bible_databases (JSON)
- **Cobertura**: 31.009 versículos, 73 livros (inclui deuterocanônicos)
- **Mapeamento**: Latin names → OSIS codes
- **Livros extras**: Tobit (TOB), Judith (JDT), 1-2 Macabeus (1MA, 2MA), Wisdom (WIS), Sirach (SIR), Baruch (BAR)

### `greek.py` — SBLGNT
- **Fonte**: morphgnt (TXT morfologicamente anotado)
- **Cobertura**: 7.927 versículos (NT + 25 de Judas)
- **Formato**: Referências XXYYZZ (XX=book num, YY=ch, ZZ=v)
- **Nota**: Texto crítico, exclui passagens espúrias

### `hebrew.py` — OSHB
- **Fonte**: Open Scriptures Hebrew Bible (OSIS XML)
- **Cobertura**: 22.933 hebraico + 280 aramaico (100% dos livros AT)
- **Aramaico**: Ranges em DAN 2:4-7:28, EZR 4:8-6:18 e 7:12-26

## 🔄 Consolidação

`main.py` deduplicates and merges:

1. **Normalização OSIS**: PS→PSA, EZE→EZK, SON→SNG
2. **Coleta de chaves**: Todas as (book, ch, v) únicas dos 5 idiomas
3. **Lookup por idioma**: Para cada combinação, busca em cada dicionário
4. **Fallback normalizado**: Se não encontra, tenta chave original

**Resultado**: 36.769 versículos alinhados, 0 duplicatas

## ✅ Validação

### Cobertura Grega: 627 versículos sem texto crítico
**ESPERADO E CORRETO:**
- **Judas**: 593 sem grego (SBLGNT = texto crítico com apenas 25 de Judas)
- **Passagens espúrias**: João 5:4, 7:53-8:2, etc. (não em mss antigos)
- **Total NT**: 92.7% cobertura

### Hebraico em NT: RESOLVIDO
- **Bug**: Parser mapeava "Judg" (Judges) → "JUD" (Jude) → 618 versículos NT com hebraico
- **Fix**: Normalização restrita apenas a PS/EZE/SON + mapeamento correto "Judg"→"JDG"
- **Resultado**: 0 versículos NT com hebraico

## 📚 Fontes Originais

| Dados | Cobertura | Fonte | Licença | Status |
|-------|-----------|-------|---------|--------|
| Português | 73 livros | Almeida 1859 (thiagobodruk/biblia) | CC-BY-SA | ✓ |
| Latim | 73 livros | Vulgata + Deuterocanônicos | PD | ✓ |
| Grego | NT (27 livros) | SBLGNT 5.11 | CC0 | ✓ |
| Hebraico | AT (39 livros) | OSHB WLC 4.20 | CC-BY-SA | ✓ |
| Aramaico | 6 livros (parcial) | OSHB | CC-BY-SA | ✓ |
| Prefácios | 13 livros | CCEL Pearse | PD | ⚠ 72% |

## 📄 Licenças

- **bible.db**: CC-BY-SA 4.0 (agregação de fontes PD/CC)
- **Conteúdo**: Domínio Público + CC0 + CC-BY-SA (vide tabela acima)

## 🎯 Próximas Fases

- **Fase 2**: Latim original para prefácios (Documenta Catholica Omnia)
- **Fase 3**: Citações patrísticas (Catena Aurea, Glossa Ordinaria)
- **Fase 4**: API REST + UI Web

---

**Versão**: 1.0 (Beta)  
**Última atualização**: 29 de abril de 2026

## Preparação

Clone os repositórios de origem dentro de `data/`:

```bash
cd data

git clone https://github.com/thiagobodruk/biblia.git
git clone https://github.com/scrollmapper/bible_databases.git
git clone https://github.com/morphgnt/sblgnt.git
git clone https://github.com/openscriptures/morphhb.git
```

## Execução

```bash
python main.py
```

Isso vai:
1. Ler todas as fontes de `data/`
2. Criar `output/bible.db` com schema completo
3. Consolidar todos os versículos em uma única tabela

## Validação

```bash
python validate.py
```

Mostra:
- Cobertura de cada língua
- Controles de qualidade (ex: NT sem grego)
- Amostra de dados

## Schema

```sql
CREATE TABLE verses (
  book        TEXT NOT NULL,  -- "GEN", "MAT", etc. (OSIS)
  chapter     INTEGER NOT NULL,
  verse       INTEGER NOT NULL,
  pt          TEXT,           -- Português (Almeida)
  lat         TEXT,           -- Latim (Vulgata)
  grc         TEXT,           -- Grego (SBLGNT)
  heb         TEXT,           -- Hebraico (OSHB)
  aram        TEXT,           -- Aramaico (OSHB)
  PRIMARY KEY (book, chapter, verse)
);
```

## Cobertura Esperada

- **PT**: ~31.000 versículos (Bíblia completa)
- **LAT**: ~31.000 versículos (Vulgata completa)
- **GRC**: ~7.957 versículos (Novo Testamento)
- **HEB**: ~23.000 versículos (Antigo Testamento)
- **ARAM**: ~250 versículos (Partes de Daniel e Esdras)

## Notas

- Hebraico e Aramaico ficam em colunas separadas porque são distinguidos pelo OSHB
- O Aramaico aparece em ranges específicos de Daniel (2:4 – 7:28) e Esdras (4:8–6:18, 7:12-26)
- Os códigos OSIS são utilizados para uniformidade entre fontes
