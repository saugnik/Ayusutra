"""
Database Inspection Script
Shows the structure and contents of the AyurSutra database
"""

import sqlite3
import os

db_path = 'ayursutra.db'

if not os.path.exists(db_path):
    print(f" Database file not found at: {db_path}")
    exit(1)

print("=" * 80)
print("🗄️  AYURSUTRA DATABASE INSPECTION")
print("=" * 80)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Get all tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
tables = cursor.fetchall()

print(f"\n📊 Total Tables: {len(tables)}\n")

for table in tables:
    table_name = table[0]
    print(f"\n{'=' * 80}")
    print(f"📋 TABLE: {table_name}")
    print('=' * 80)
    
    # Get table schema
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = cursor.fetchall()
    
    print("\n🔧 Schema:")
    for col in columns:
        col_id, col_name, col_type, not_null, default, pk = col
        pk_marker = " [PRIMARY KEY]" if pk else ""
        null_marker = " NOT NULL" if not_null else ""
        print(f"  - {col_name}: {col_type}{pk_marker}{null_marker}")
    
    # Get row count
    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
    count = cursor.fetchone()[0]
    print(f"\n📈 Row Count: {count}")
    
    # Show sample data if exists
    if count > 0:
        cursor.execute(f"SELECT * FROM {table_name} LIMIT 3")
        rows = cursor.fetchall()
        
        print(f"\n📄 Sample Data (first {min(count, 3)} rows):")
        col_names = [col[1] for col in columns]
        
        for i, row in enumerate(rows, 1):
            print(f"\n  Row {i}:")
            for col_name, value in zip(col_names, row):
                # Truncate long values
                str_value = str(value)
                if len(str_value) > 50:
                    str_value = str_value[:47] + "..."
                print(f"    {col_name}: {str_value}")

print("\n" + "=" * 80)
print("✅ Database inspection complete!")
print("=" * 80)

conn.close()
