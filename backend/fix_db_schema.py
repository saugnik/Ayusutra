
import sqlite3
import sys

def fix_database():
    print("Checking database schema...")
    try:
        conn = sqlite3.connect('ayursutra.db')
        cursor = conn.cursor()
        
        # 1. Fix ai_conversations table
        print("\nChecking ai_conversations table...")
        cursor.execute("PRAGMA table_info(ai_conversations)")
        columns = [info[1] for info in cursor.fetchall()]
        
        if 'title' not in columns:
            print("Adding 'title' column to ai_conversations...")
            cursor.execute("ALTER TABLE ai_conversations ADD COLUMN title VARCHAR(255)")
        else:
            print("'title' column already exists.")

        # 2. Fix practitioners table
        print("\nChecking practitioners table...")
        cursor.execute("PRAGMA table_info(practitioners)")
        columns = [info[1] for info in cursor.fetchall()]
        
        if 'latitude' not in columns:
            print("Adding 'latitude' column to practitioners...")
            cursor.execute("ALTER TABLE practitioners ADD COLUMN latitude FLOAT")
        else:
            print("'latitude' column already exists.")
            
        if 'longitude' not in columns:
            print("Adding 'longitude' column to practitioners...")
            cursor.execute("ALTER TABLE practitioners ADD COLUMN longitude FLOAT")
        else:
            print("'longitude' column already exists.")

        if 'availability_schedule' not in columns:
            print("Adding 'availability_schedule' column to practitioners...")
            cursor.execute("ALTER TABLE practitioners ADD COLUMN availability_schedule JSON")
        else:
             print("'availability_schedule' column already exists.")

        conn.commit()
        print("\nDatabase schema fixed successfully!")
        conn.close()
        
    except Exception as e:
        print(f"\nError fixing database: {e}")
        sys.exit(1)

if __name__ == "__main__":
    fix_database()
