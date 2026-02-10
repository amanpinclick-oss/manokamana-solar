# db.py
import sqlite3
import os
from contextlib import contextmanager

DB_PATH = "data/store.db"

@contextmanager
def conn():
    c = sqlite3.connect(DB_PATH)
    try:
        yield c
        c.commit()
    finally:
        c.close()

def init_db():
    if not os.path.exists("data"):
        os.makedirs("data")
        
    with conn() as c:
        # Task queue table
        c.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            agent TEXT NOT NULL,
            payload TEXT NOT NULL,
            status TEXT DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        
        # SEO metrics table
        c.execute("""
        CREATE TABLE IF NOT EXISTS seo_metrics (
            query TEXT PRIMARY KEY,
            clicks INTEGER,
            impressions INTEGER,
            ctr REAL,
            position REAL,
            last_updated TIMESTAMP
        )
        """)
        
        # Leads storage table
        c.execute("""
        CREATE TABLE IF NOT EXISTS leads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            phone TEXT,
            type TEXT,                -- Industrial / Commercial
            intent_score REAL,
            source TEXT,              -- website / whatsapp / linkedin
            status TEXT DEFAULT 'new',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        print("Database initialized successfully.")

if __name__ == "__main__":
    init_db()
