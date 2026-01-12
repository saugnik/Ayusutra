import sqlite3
import os

db_path = "ayursutra.db"

if not os.path.exists(db_path):
    print(f"Database file '{db_path}' does NOT exist!")
else:
    print(f"Database file '{db_path}' exists.")
    print(f"File size: {os.path.getsize(db_path)} bytes")
    
    # Connect and check tables
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Get list of tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    print(f"\nTables in database: {len(tables)}")
    for table in tables:
        print(f"  - {table[0]}")
        
        # Get table schema
        cursor.execute(f"PRAGMA table_info({table[0]});")
        columns = cursor.fetchall()
        print(f"    Columns: {len(columns)}")
        for col in columns:
            print(f"      - {col[1]} ({col[2]})")
    
    conn.close()
