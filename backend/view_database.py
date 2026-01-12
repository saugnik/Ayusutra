"""
Interactive Database Viewer for AyurSutra
Shows complete database structure with detailed schema and data
"""

import sqlite3
import json
from datetime import datetime

def format_value(value):
    """Format value for display"""
    if value is None:
        return "NULL"
    if isinstance(value, str) and len(value) > 60:
        return value[:57] + "..."
    return str(value)

def show_database():
    conn = sqlite3.connect('ayursutra.db')
    cursor = conn.cursor()
    
    print("\n" + "=" * 100)
    print(" " * 35 + "🗄️  AYURSUTRA DATABASE")
    print("=" * 100)
    
    # Get all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
    tables = [t[0] for t in cursor.fetchall()]
    
    print(f"\n📊 Database Overview")
    print("-" * 100)
    print(f"Total Tables: {len(tables)}")
    print(f"Database File: ayursutra.db")
    print(f"Database Type: SQLite")
    
    # Summary table
    print(f"\n📋 Table Summary")
    print("-" * 100)
    print(f"{'Table Name':<30} {'Columns':<10} {'Rows':<10} {'Status':<20}")
    print("-" * 100)
    
    for table in tables:
        cursor.execute(f"PRAGMA table_info({table})")
        col_count = len(cursor.fetchall())
        
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        row_count = cursor.fetchone()[0]
        
        status = "✅ Has Data" if row_count > 0 else "⚪ Empty"
        print(f"{table:<30} {col_count:<10} {row_count:<10} {status:<20}")
    
    # Detailed view for each table
    print("\n" + "=" * 100)
    print(" " * 35 + "📖 DETAILED TABLE SCHEMAS")
    print("=" * 100)
    
    for table in tables:
        print(f"\n{'─' * 100}")
        print(f"📋 TABLE: {table.upper()}")
        print('─' * 100)
        
        # Get schema
        cursor.execute(f"PRAGMA table_info({table})")
        columns = cursor.fetchall()
        
        print(f"\n🔧 Schema ({len(columns)} columns):")
        print(f"{'Column Name':<25} {'Type':<15} {'Constraints':<30}")
        print("-" * 70)
        
        for col in columns:
            col_id, col_name, col_type, not_null, default, pk = col
            
            constraints = []
            if pk:
                constraints.append("PRIMARY KEY")
            if not_null:
                constraints.append("NOT NULL")
            if default:
                constraints.append(f"DEFAULT {default}")
            
            constraint_str = ", ".join(constraints) if constraints else "-"
            print(f"{col_name:<25} {col_type:<15} {constraint_str:<30}")
        
        # Get row count
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]
        
        print(f"\n📊 Data: {count} rows")
        
        # Show sample data if exists
        if count > 0:
            cursor.execute(f"SELECT * FROM {table} LIMIT 5")
            rows = cursor.fetchall()
            col_names = [col[1] for col in columns]
            
            print(f"\n📄 Sample Data (showing {min(count, 5)} of {count} rows):")
            print("-" * 100)
            
            for i, row in enumerate(rows, 1):
                print(f"\n  🔹 Row {i}:")
                for col_name, value in zip(col_names, row):
                    formatted_value = format_value(value)
                    print(f"     {col_name:<20}: {formatted_value}")
        else:
            print("     ⚪ No data in this table yet")
    
    # Database statistics
    print("\n" + "=" * 100)
    print(" " * 35 + "📈 DATABASE STATISTICS")
    print("=" * 100)
    
    total_rows = 0
    for table in tables:
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        total_rows += cursor.fetchone()[0]
    
    print(f"\nTotal Tables:        {len(tables)}")
    print(f"Total Rows:          {total_rows}")
    print(f"Tables with Data:    {sum(1 for t in tables if cursor.execute(f'SELECT COUNT(*) FROM {t}').fetchone()[0] > 0)}")
    print(f"Empty Tables:        {sum(1 for t in tables if cursor.execute(f'SELECT COUNT(*) FROM {t}').fetchone()[0] == 0)}")
    
    # Key relationships
    print(f"\n🔗 Key Relationships:")
    print("-" * 100)
    print("users → patients (one-to-one)")
    print("users → practitioners (one-to-one)")
    print("users → admins (one-to-one)")
    print("patients → appointments (one-to-many)")
    print("practitioners → appointments (one-to-many)")
    print("appointments → therapy_sessions (one-to-one)")
    print("appointments → feedback (one-to-one)")
    
    print("\n" + "=" * 100)
    print(" " * 30 + "✅ Database Inspection Complete!")
    print("=" * 100 + "\n")
    
    conn.close()

if __name__ == "__main__":
    try:
        show_database()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
