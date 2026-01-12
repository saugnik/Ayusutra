"""
Simple Database Viewer - ASCII only
"""

import sqlite3

conn = sqlite3.connect('ayursutra.db')
cursor = conn.cursor()

print("\n" + "=" * 80)
print("AYURSUTRA DATABASE STRUCTURE")
print("=" * 80)

# Get all tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
tables = [t[0] for t in cursor.fetchall()]

print(f"\nTotal Tables: {len(tables)}\n")

# Table summary
print("TABLE SUMMARY")
print("-" * 80)
print(f"{'Table Name':<30} {'Columns':<10} {'Rows':<10} {'Status'}")
print("-" * 80)

for table in tables:
    cursor.execute(f"PRAGMA table_info({table})")
    col_count = len(cursor.fetchall())
    
    cursor.execute(f"SELECT COUNT(*) FROM {table}")
    row_count = cursor.fetchone()[0]
    
    status = "HAS DATA" if row_count > 0 else "EMPTY"
    print(f"{table:<30} {col_count:<10} {row_count:<10} {status}")

print("\n" + "=" * 80)
print("DETAILED SCHEMAS")
print("=" * 80)

for table in tables:
    print(f"\nTABLE: {table.upper()}")
    print("-" * 80)
    
    # Get schema
    cursor.execute(f"PRAGMA table_info({table})")
    columns = cursor.fetchall()
    
    print(f"\nColumns ({len(columns)}):")
    for col in columns:
        col_id, col_name, col_type, not_null, default, pk = col
        
        constraints = []
        if pk:
            constraints.append("PRIMARY KEY")
        if not_null:
            constraints.append("NOT NULL")
        
        constraint_str = ", ".join(constraints) if constraints else ""
        print(f"  - {col_name:<25} {col_type:<15} {constraint_str}")
    
    # Row count
    cursor.execute(f"SELECT COUNT(*) FROM {table}")
    count = cursor.fetchone()[0]
    print(f"\nRows: {count}")
    
    # Sample data
    if count > 0:
        cursor.execute(f"SELECT * FROM {table} LIMIT 3")
        rows = cursor.fetchall()
        col_names = [col[1] for col in columns]
        
        print(f"\nSample Data:")
        for i, row in enumerate(rows, 1):
            print(f"\n  Row {i}:")
            for col_name, value in zip(col_names, row):
                val_str = str(value)[:50] if value else "NULL"
                print(f"    {col_name}: {val_str}")

print("\n" + "=" * 80)
print("DATABASE STATISTICS")
print("=" * 80)

total_rows = sum(cursor.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0] for t in tables)
tables_with_data = sum(1 for t in tables if cursor.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0] > 0)

print(f"\nTotal Tables:        {len(tables)}")
print(f"Total Rows:          {total_rows}")
print(f"Tables with Data:    {tables_with_data}")
print(f"Empty Tables:        {len(tables) - tables_with_data}")

print("\n" + "=" * 80 + "\n")

conn.close()
