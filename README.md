# Bíblia

Banco de dados bíblico multilíngue, pronto para uso, e as ferramentas usadas para construí-lo.

## Proposta

Este repositório não é um app — é a **base de dados** para construir um. A ideia é resolver uma vez
o trabalho chato de coletar, normalizar e alinhar texto bíblico em várias línguas (incluindo as
línguas originais) verso a verso, para que qualquer app possa simplesmente consultar um único
arquivo SQLite em vez de lidar com múltiplas fontes, formatos e numerações de versículo diferentes.

**Objetivo**: servir de fundação de dados para projetos de app bíblico — leitura, estudo comparado
entre traduções/línguas originais, busca, memorização, etc. — sem que cada projeto precise repetir a
etapa de coleta e consolidação das fontes.

## O que tem aqui

### [`bible-importer/`](bible-importer/)

O conteúdo principal do repositório. É um consolidador que junta textos bíblicos de várias fontes
públicas (português, latim, grego, hebraico e aramaico) em um único banco SQLite, alinhados
verso a verso por livro/capítulo/versículo (códigos OSIS).

- **40.510 versículos únicos** em 81 livros (66 canônicos + 15 deuterocanônicos)
- Português (Almeida 1859), Latim (Vulgata), Grego (SBLGNT + Septuaginta), Hebraico e Aramaico (OSHB)
- Inclui prefácios de Jerônimo para parte dos livros
- Scripts de consolidação (`main.py`), parsers por idioma (`parsers/`) e uma CLI de consulta (`query.py`)
- Banco pronto em [`bible-importer/output/bible.db`](bible-importer/output/bible.db) (SQLite, ~31 MB)

Veja o [README do bible-importer](bible-importer/README.md) para detalhes do schema, como reconstruir
o banco a partir das fontes originais, cobertura por idioma e licenças de cada fonte.

### `package.json` (raiz)

Stub inicial com dependência do React Native — reservado para um futuro app que consuma esse banco de dados.
Ainda não há código de aplicação.

## Como isso pode ser usado num app

O banco (`bible-importer/output/bible.db`) é um SQLite comum, com uma tabela `verses` já com todas
as línguas lado a lado por `(book, chapter, verse)`. Qualquer stack consegue ler direto:

- **App mobile (React Native, Flutter, etc.)**: embarcar o `.db` como asset e abrir com uma lib de
  SQLite local (ex.: `react-native-sqlite-storage`, `expo-sqlite`, `sqflite`) — sem precisar de backend.
- **Backend/API**: servir o mesmo `.db` via uma API REST/GraphQL fina, ou importar para Postgres/MySQL
  se for preciso escalar.
- **Web**: usar via `sql.js`/WASM direto no navegador, ou por trás de uma API.

Exemplos de consulta direta em SQL:

```sql
-- Um versículo em todas as línguas disponíveis
SELECT pt, lat, grc, heb, aram FROM verses WHERE book = 'GEN' AND chapter = 1 AND verse = 1;

-- Capítulo inteiro em português
SELECT verse, pt FROM verses WHERE book = 'JHN' AND chapter = 3 ORDER BY verse;

-- Prefácio de Jerônimo para um livro
SELECT title, content_eng FROM book_prefaces WHERE book = 'GEN';
```

Casos de uso possíveis a partir dessa base:

- **App de leitura** simples, com uma ou mais traduções
- **Estudo comparado**: mostrar português/latim/grego/hebraico lado a lado do mesmo versículo
- **Busca** por palavra/trecho em qualquer uma das línguas
- **Ferramentas de línguas originais**: apoio a quem estuda grego/hebraico bíblico, comparando com a tradução
- **Leitura com contexto histórico**: exibir os prefácios de Jerônimo junto ao livro correspondente

## Fontes de dados

As fontes originais (repositórios de terceiros) não ficam versionadas aqui — são clonadas à parte
dentro de `bible-importer/data/` e `bible-importer/sblgnt/` (veja o passo a passo em
[bible-importer/README.md](bible-importer/README.md#preparação)). Isso só é necessário para
reconstruir o banco do zero; para usar em um app basta o `bible.db` já pronto.

## Licenças

O conteúdo consolidado combina fontes em Domínio Público, CC0 e CC-BY-SA. Veja a tabela de fontes
e licenças no [README do bible-importer](bible-importer/README.md#-fontes-originais).
