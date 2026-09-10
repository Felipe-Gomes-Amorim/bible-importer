# Bíblia

Repositório com um banco de dados bíblico multilíngue e as ferramentas usadas para construí-lo.

## O que tem aqui

### [`bible-importer/`](bible-importer/)

O conteúdo principal do repositório. É um consolidador que junta textos bíblicos de várias fontes
públicas (português, latim, grego, hebraico e aramaico) em um único banco SQLite, alinhados
verso a verso por livro/capítulo/versículo (códigos OSIS).

- **40.510 versículos únicos** em 81 livros (66 canônicos + 15 deuterocanônicos)
- Português (Almeida 1859), Latim (Vulgata), Grego (SBLGNT + Septuaginta), Hebraico e Aramaico (OSHB)
- Inclui prefácios de Jerônimo para parte dos livros
- Scripts de consolidação (`main.py`), parsers por idioma (`parsers/`) e uma CLI de consulta (`query.py`)

Veja o [README do bible-importer](bible-importer/README.md) para detalhes do schema, como reconstruir
o banco a partir das fontes originais, cobertura por idioma e licenças de cada fonte.

### `package.json` (raiz)

Stub inicial com dependência do React Native — reservado para um futuro app que consuma esse banco de dados.
Ainda não há código de aplicação.

## Fontes de dados

As fontes originais (repositórios de terceiros) não ficam versionadas aqui — são clonadas à parte
dentro de `bible-importer/data/` e `bible-importer/sblgnt/` (veja o passo a passo em
[bible-importer/README.md](bible-importer/README.md#preparação)).

## Licenças

O conteúdo consolidado combina fontes em Domínio Público, CC0 e CC-BY-SA. Veja a tabela de fontes
e licenças no [README do bible-importer](bible-importer/README.md#-fontes-originais).
