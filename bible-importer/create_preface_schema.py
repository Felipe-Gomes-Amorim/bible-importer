#!/usr/bin/env python3
"""
Schema para prefácios e notas patrísticas.
"""

import sqlite3
import os

DB_PATH = "output/bible.db"

def create_prefaces_table(conn):
    """Cria tabelas para prefácios e citações patrísticas."""
    
    # Tabela de prefácios (específicos de livros)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS book_prefaces (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            book        TEXT NOT NULL,      -- OSIS code: 'GEN', 'MAT', etc.
            author      TEXT NOT NULL,      -- 'Jerome', 'Augustine', etc.
            title       TEXT,               -- 'Prologue to Genesis'
            content_lat TEXT,               -- Latin original
            content_eng TEXT,               -- English (bridge)
            source_url  TEXT,
            created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(book, author),
            FOREIGN KEY (book) REFERENCES verses(book)
        )
    """)
    
    # Tabela de citações patrísticas (específicas de versículos)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS patristic_citations (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            book        TEXT NOT NULL,
            chapter     INTEGER NOT NULL,
            verse       INTEGER NOT NULL,
            father      TEXT NOT NULL,      -- 'Augustine', 'Aquinas', etc.
            work        TEXT,               -- 'Commentary on Genesis'
            citation    TEXT,               -- Trecho citado
            source_url  TEXT,
            created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (book, chapter, verse) REFERENCES verses(book, chapter, verse)
        )
    """)
    
    conn.commit()
    print("✓ Tabelas criadas: book_prefaces, patristic_citations")

if __name__ == "__main__":
    conn = sqlite3.connect(DB_PATH)
    create_prefaces_table(conn)
    conn.close()
    
    print("\nSchema de prefácios e citações adicionado ao bible.db")
