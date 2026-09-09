import sqlite3

conn = sqlite3.connect('output/bible.db')
result = conn.execute("SELECT heb FROM verses WHERE book='MAT' AND chapter=1 AND verse=1").fetchone()

print("MAT 1:1 hebraico:", result)
if result[0]:
    print("\nPROBLEMA ENCONTRADO!")
    print("Conteúdo:", result[0][:150])
    print("\nIsto não deveria estar aqui (Mateus é NT, não AT).")
else:
    print("\nOK - retornou None como esperado")

conn.close()
