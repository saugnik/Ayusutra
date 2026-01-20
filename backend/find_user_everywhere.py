
import sqlite3
import os

def check_databases():
    user_email = "saugnikaich123@gmail.com"
    files = [
        "ayursutra.db",
        "ayursutra_v2.db",
        "backend/ayursutra.db",
        "backend/ayursutra_v2.db"
    ]
    
    found = False
    print(f"Searching for {user_email} in all database files...\n")
    
    for db_file in files:
        if not os.path.exists(db_file):
            print(f"[MISSING] {db_file}")
            continue
            
        try:
            conn = sqlite3.connect(db_file)
            cursor = conn.cursor()
            cursor.execute("SELECT id, email, role, is_active FROM users WHERE email=?", (user_email,))
            user = cursor.fetchone()
            
            if user:
                print(f"[FOUND] in {db_file}")
                print(f"  ID: {user[0]}")
                print(f"  Role: {user[2]}")
                print(f"  Active: {user[3]}")
                found = True
            else:
                print(f"[NOT FOUND] in {db_file}")
                
            conn.close()
        except Exception as e:
            print(f"[ERROR] {db_file}: {e}")
            
    if not found:
        print("\nUser not found in any of the checked databases.")

if __name__ == "__main__":
    check_databases()
