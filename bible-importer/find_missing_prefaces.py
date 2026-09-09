import sqlite3
conn = sqlite3.connect("output/bible.db")
conn.execute("DROP TABLE IF EXISTS book_prefaces")
conn.commit()
conn.close()
print("Tabela removida — rode o scraper novamente para recriar com todos os 19 prefácios.")