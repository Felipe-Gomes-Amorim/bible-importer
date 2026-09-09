# Guia de Uso - LXX (Septuaginta)

## O que foi adicionado?

A **LXX (Septuaginta em grego)** do Antigo Testamento foi integrada ao banco de dados como uma tradução disponível em grego. Agora você tem:

### Cobertura de Texto Grego:
- **SBLGNT**: Novo Testamento (Mateus até Apocalipse) - 7.927 versículos
- **LXX**: Antigo Testamento (Genesis até Malachi) + deuterocanônicos - 28.861 versículos
- **Total**: 36.788 versículos em grego

### Livros Disponíveis em LXX:

#### Pentateuco (5 livros)
- Genesis (GEN): 1.531 versículos
- Exodus (EXO): 1.163 versículos
- Leviticus (LEV): 859 versículos
- Numbers (NUM): 1.287 versículos
- Deuteronomy (DEU): 959 versículos

#### Livros Históricos (12 livros)
- Joshua (JOS): 643 versículos
- Judges (JDG): 617 versículos
- Ruth (RUT): 85 versículos
- 1 Samuel (1SA): 772 versículos
- 2 Samuel (2SA): 695 versículos
- 1 Kings (1KI): 756 versículos
- 2 Kings (2KI): 719 versículos
- 1 Chronicles (1CH): 930 versículos
- 2 Chronicles (2CH): 821 versículos
- Ezra (EZR): 280 versículos
- Nehemiah (NEH): 392 versículos
- Esther (EST): 164 versículos

#### Livros Sapienciais (5 livros)
- Job (JOB): 1.069 versículos
- Psalms (PSA): 2.533 versículos
- Proverbs (PRO): 891 versículos
- Ecclesiastes (ECC): 222 versículos
- Song of Songs (SNG): 117 versículos

#### Profetas Maiores (5 livros)
- Isaiah (ISA): 1.289 versículos
- Jeremiah (JER): 1.298 versículos
- Lamentations (LAM): 151 versículos
- Ezekiel (EZK): 1.267 versículos
- Daniel (DAN): 406 versículos

#### Profetas Menores (12 livros)
- Hosea (HOS): 197 versículos
- Joel (JOL): 73 versículos
- Amos (AMO): 146 versículos
- Obadiah (OBA): 21 versículos
- Jonah (JON): 48 versículos
- Micah (MIC): 105 versículos
- Nahum (NAH): 47 versículos
- Habakkuk (HAB): 56 versículos
- Zephaniah (ZEP): 53 versículos
- Haggai (HAG): 38 versículos
- Zechariah (ZEC): 211 versículos
- Malachi (MAL): 55 versículos

#### Deuterocanônicos (8 livros)
- 1 Esdras (1ES): 434 versículos
- Tobit (TOB): 248 versículos
- Judith (JDT): 340 versículos
- Wisdom of Solomon (WIS): 435 versículos
- Wisdom of Sirach (SIR): 1.367 versículos
- Baruch (BAR): 141 versículos
- Epistle of Jeremiah (EJR): 73 versículos
- Susanna (SUS): 36 versículos
- Bel and the Dragon (BEL): 37 versículos
- 1 Maccabees (1MC): 924 versículos
- 2 Maccabees (2MC): 555 versículos
- 3 Maccabees (3MC): 228 versículos
- 4 Maccabees (4MC): 479 versículos
- Psalms of Solomon (PSS): 310 versículos
- Odes (ODE): 288 versículos

## Como Usar?

### 1. Executar Main para Gerar/Atualizar Banco

```bash
python main.py
```

Isto vai:
- Baixar automaticamente o banco SQLite da LXX do GitHub
- Consolidar com as outras traduções (Português, Latim, Hebraico, Aramaico)
- Criar banco `output/bible.db` com todos os dados

### 2. Consultar versículos com LXX

```bash
# Consulta interativa
python query.py

# Buscar versículo específico
python query.py gen 1:1     # Genesis 1:1
python query.py psa 23:1    # Psalm 23:1 - Salmo do Bom Pastor
python query.py isa 53:1    # Isaiah 53 - Profecia do Messias
python query.py mat 1:1     # Mateus 1:1 - Novo Testamento (grego SBLGNT)

# Consultar deuterocanônicos
python query.py tob 1:1     # Tobit 1:1
python query.py wis 1:1     # Wisdom 1:1
python query.py 1mc 1:1     # 1 Maccabees 1:1
```

### 3. Testar o Banco

```bash
python test_lxx.py
```

Isto vai mostrar estatísticas do banco e verificar alguns versículos.

## Exemplos de Saída

Quando você faz uma consulta, verá algo como:

```
======================================================================
GEN 1:1
======================================================================

PORTUGUES:
  No principio criou Deus os ceus e a terra.

LATIM:
  in principio creavit Deus caelum et terram

GREGO (LXX):
  en archei epoiesen ho theos ton ouranon kai ten gen

HEBRAICO:
  bereschith bara elohim et haschemajim wet haarets
```

## Fonte de Dados

- **LXX (Septuaginta)**: Rahlfs 1935 edition do repositório GitHub de Eliran Wong
  - https://github.com/eliranwong/LXX-Rahlfs-1935
  - Dados estruturados em SQLite com metadados morfológicos
  - Domínio público

## Estatísticas do Banco

- Total de versículos: 40.510
- Versículos com grego: 36.788
- Livros com grego: 81 (66 canônicos + 15 deuterocanônicos)
- LXX (AT): 28.861 versículos em 54 livros

## Arquivos Modificados/Criados

1. `parsers/lxx.py` - Parser para LXX (novo)
2. `main.py` - Integração da LXX na consolidação
3. `test_lxx.py` - Testes de funcionalidade (novo)
4. `explore_*.py` - Scripts de exploração (auxiliares)

## Notas Técnicas

- O banco SQLite é automaticamente baixado do GitHub quando necessário
- O texto grego é extraído com limpeza automática de markup XML
- A LXX tem prioridade sobre SBLGNT para livros do Antigo Testamento
- O carregamento utiliza retry automático para conexões instáveis
