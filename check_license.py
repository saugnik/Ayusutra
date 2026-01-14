
import sqlite3
import os

def check_duplicate():
    db_path = "backend/ayursutra.db"
    if not os.path.exists(db_path):
        print(f"Database not found at {db_path}")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print(f"Checking database: {db_path}")
    print("-" * 50)
    
    try:
        # Check conflicts for license '236512'
        cursor.execute("SELECT p.id, p.user_id, p.license_number, u.email, u.full_name FROM practitioners p JOIN users u ON p.user_id = u.id WHERE p.license_number = ?", ('236512',))
        conflict = cursor.fetchone()
        
        if conflict:
            print(f"CONFLICT FOUND!")
            print(f"Practitioner ID: {conflict[0]}")
            print(f"User ID: {conflict[1]}")
            print(f"License: {conflict[2]}")
            print(f"Email: {conflict[3]}")
            print(f"Name: {conflict[4]}")
            print("-" * 50)
            
            # Offer to delete if it's a test user?
            # For now just informational
        else:
            print("No practitioner found with license '236512'")

        # List all practitioners for context
        print("\nAll Practitioners:")
        cursor.execute("SELECT p.id, p.license_number, u.email FROM practitioners p JOIN users u ON p.user_id = u.id")
        rows = cursor.fetchall()
        for row in rows:
            print(f"ID: {row[0]}, License: {row[1]}, Email: {row[2]}")

    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    check_duplicate()
